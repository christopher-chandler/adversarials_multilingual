# Standard
from collections import Counter

# Pip
import spacy

# Custom
from adversaries.settings.messages.custom_error_messages import (
    CustomErrorMessages as Cem,
)

SPACY_MODELS = {
    "de": "de_core_news_sm",
    "en": "en_core_web_sm",
    "es": "es_core_news_sm",
    "fr": "fr_core_news_sm",
}

NOUNS = ("NOUN",)

VALID_LANGS = list(SPACY_MODELS.keys())


class MultiLingualSpacy(Cem):
    """
    A class for performing multilingual processing using SpaCy.

    This class allows for the processing of text documents or individual sentences
    in multiple languages using SpaCy, a natural language processing library.

    Attributes:
        language (str): The language code for the SpaCy model to be used.
        incoming_document (str): The path to the incoming document to be processed.

    Methods:
        preprocess_document(): Preprocesses the incoming document.
        spacy_multi_tagger(): Performs multi-tagging using SpaCy.
    """

    def __init__(self, language, incoming_document):
        """Initialize the MultiLingualSpacy object.

        Args:
            language (str): The language code for the SpaCy model.
            incoming_document (str): The path to the incoming document.
        """
        self.language = language
        self.incoming_document = incoming_document

    def preprocess_document(self):
        """Preprocesses the incoming document.

        Returns:
            list: A list of preprocessed sentences.
        """
        with open(
            self.incoming_document, mode="r", encoding="UTF-8"
        ) as incoming_document:
            lines = incoming_document.readlines()
            doc_sentences = [sentence.strip() for sentence in lines if sentence.strip()]
            return doc_sentences

    def spacy_multi_tagger(
        self,
        sentence="Hello World",
        process_document=False,
        return_spacy_results=False,
        return_only_tags=False,
        return_all_nouns=False,
        return_pos_count = False
    ) -> None:
        """Performs multi-tagging using Spacy.

        Args:
            sentence (str): The sentence to process.
            process_document (bool): Whether to process the entire document.
            return_spacy_results (bool): Whether to return the full SpaCy analysis results.
            return_only_tags (bool): Whether to return only the part-of-speech tags.
            return_all_nouns (bool): Whether to return all identified nouns.
            return_pos_count (bool): Whether to return count of all part of speech tags.

        Returns:
            None: Depending on the parameters, returns analysis results,
            part-of-speech tags, count, or nouns.
        """

        lang_chosen = SPACY_MODELS.get(self.language)

        does_not_exist = None

        if lang_chosen == does_not_exist:
            raise self.MultiLingualSpacyError(self.language, VALID_LANGS)

        else:

            if process_document:
                NLP_SPACY_CORPUS = "\n".join(self.preprocess_document())
            else:
                NLP_SPACY_CORPUS = sentence

            nlp = spacy.load(lang_chosen)
            doc = nlp(NLP_SPACY_CORPUS)
            spacy_analysis_results = dict()

            for token in doc:
                spacy_analysis_results[token.text] = {
                    "pos": token.pos_,
                    "dep": token.dep_,
                }

            part_of_speech = list()

            for token in spacy_analysis_results:
                pos = spacy_analysis_results.get(token).get("pos")
                part_of_speech.append((token, pos))

            if return_spacy_results:
                return spacy_analysis_results

            elif return_only_tags:
                return part_of_speech

            elif return_all_nouns:
                nouns = list()
                for n in part_of_speech:
                    word, pos = n
                    if pos in NOUNS:
                        nouns.append(word)
                return nouns

            elif return_pos_count:
                pos_count = [pos_tag[1] for pos_tag in part_of_speech]

                return Counter(pos_count)

if __name__ == "__main__":
    pass
