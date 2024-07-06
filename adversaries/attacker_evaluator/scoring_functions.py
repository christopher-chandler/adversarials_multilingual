"""
Funktionen für das Scoring der echten Antworten und der Adversarial Antworten
@author: Ronja Laarmann-Quante
"""

import csv

# Standard
import os
from typing import Tuple

# https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
# https://scikit-learn.org/stable/common_pitfalls.html

# Pip
import numpy as np
import pandas as pd
from pathlib import Path

from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import cohen_kappa_score, make_scorer
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import FunctionTransformer, MinMaxScaler


def construct_svm_scoring_model():
    """
    Constructs an SVM-based scoring model for text data.

    Returns:
        Pipeline: SVM-based scoring model pipeline.
    """
    ##########################################
    # Feature Extraction

    # see https://stackoverflow.com/questions/39121104/how-to-add-another-feature-length-of-text-to-current-bag-of-words-classificati
    # Antwortlänge (hier sehr simpel als Anzahl der Zeichen)
    def answer_length(x):
        # reshape(-1, 1) is nötig, damit das Array die richtige Form für die Weiterverarbeitung hat
        lengths = np.array([len(answer) for answer in x]).reshape(-1, 1)
        # re-scalen, damit Werte zwischen 0 und 1 liegen, so wie bei TF-IDF
        rescaled = MinMaxScaler().fit_transform(lengths)
        return rescaled

    answer_length_feature = FunctionTransformer(answer_length)

    # Wort- und Buchstaben-N-Gramme extrahieren
    char_tfidf = CountVectorizer(
        analyzer="char", ngram_range=(2, 5), max_features=10000
    )
    word_tfidf = CountVectorizer(
        analyzer="word", ngram_range=(1, 5), max_features=10000
    )

    features = FeatureUnion(
        [
            ("char", char_tfidf),
            ("word", word_tfidf),
            ("answer_length", answer_length_feature),
        ]
    )

    ##########################################
    # Pipeline bauen
    model = Pipeline([("features", features), ("clf", svm.SVC(random_state=123))])
    return model


def cross_validation_qwk(model: Pipeline, training_file: str) -> float:
    """
    Performs cross-validation using Quadratic Weighted Kappa (QWK) as the scoring metric.

    Args:
        model (Pipeline): Scoring model pipeline.
        training_file (str): Path to the training data file.

    Returns:
        float: Mean QWK score across all folds.
    """
    # Fun
    training_file = Path(training_file)
    # NAs must not be filtered, otherwise answer "None" is interpreted as NA value
    training_data = pd.read_csv(training_file, sep="\t", na_filter=False)

    X = training_data["text"]  # "Features"

    y = training_data["score"]  # Target variable

    cv = KFold(n_splits=10, shuffle=True, random_state=42)
    qwk_scorer = make_scorer(cohen_kappa_score, weights="quadratic")
    cv_scores = cross_val_score(model, X, y, cv=cv, scoring=qwk_scorer)
    return cv_scores.mean()


def arr_for_trained_model(
    model: Pipeline, training_file: str, adversarial_file: str
) -> Tuple[np.ndarray, float]:
    """
    Computes Adversarial Rejection Rate (ARR) for a trained scoring model.

    Args:
        model (Pipeline): Trained scoring model pipeline.
        training_file (str): Path to the training data file.
        adversarial_file (str): Path to the adversarial data file.

    Returns:
        tuple: Predicted scores for adversarial data and Adversarial Rejection Rate.
    """
    training_file = Path(training_file)
    training_data = pd.read_csv(training_file, sep="\t", na_filter=False)

    X = training_data["text"]  # "Features"
    y = training_data["score"]  # Target variable

    model.fit(X, y)  # auf ganzem Datenset trainieren

    ##########################################
    # Vorhersagen für Adversarials

    with open(adversarial_file, mode="r", encoding="latin-1") as f:
        content_burst_text = pd.read_csv(f, delimiter="\t")
        adversarials = content_burst_text["EssayText"]

    y_pred = model.predict(adversarials)

    ##########################################
    # Evaluieren mit Adversarial Rejection Rate
    arr = len([pred for pred in y_pred if pred == 0]) / len(y_pred)

    # Save ARR Scored results
    path, file = os.path.split(training_file)
    file = file.replace("ASAP", "ARR")
    save_file = f"results/arr_sentences_results/{file}"
    with open(save_file, mode="w+", encoding="utf-8") as out_file:
        csv_writer = csv.writer(out_file, delimiter="\t")

        for a, y in zip(adversarials.to_list(), y_pred):
            csv_writer.writerow((a, y))

    return y_pred, arr


if __name__ == "__main__":
    pass
