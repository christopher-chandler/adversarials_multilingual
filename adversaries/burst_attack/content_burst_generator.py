# Standard
import csv
import os.path

# Pip
import nltk
from numpy.random import choice, seed
from typing import List, Tuple

# Custom
from adversaries.docs_processor.multilingual_spacy import MultiLingualSpacy
from adversaries.settings.constants.constant_paths import GeneralPaths as Gp
from adversaries.settings.constants.constant_vars import CONTENT_BURST_SEED

"""
Based on the code: 
https://github.com/catalpa-cl/adversarials/blob/master/content_burst_generator.py
"""

# Fix results
seed(CONTENT_BURST_SEED)


class ContentBurstGenerator(MultiLingualSpacy):
    """
    A class to generate content burst adversarials based on given prompt text.
    It is extended by the class MultiLingualSpacy
    """

    def __init__(self, prompt_text: str, language: str, burst_amount: int = 1000):
        """
        Initializes the ContentBurstGenerator object.

        Args:
            prompt_text (str): The path to the prompt text file.
            language (str): The language of the prompt text.
            burst_amount (int, optional): The number of burst adversarials to generate
            (default is 1000).
        """
        super().__init__(language, prompt_text)
        self.prompt_text = prompt_text
        self.burst_amount = burst_amount

    @staticmethod
    def get_text(grams: List[str], frequency: List[float], avg_length: int) -> str:
        """
        Generates a content burst based on given grams, frequency, and average length.

        Args:
            grams (List[str]): List of grams.
            frequency (List[float]): Frequency of grams.
            avg_length (int): Average length of the burst.

        Returns:
            str: Generated content burst.
        """
        start = choice(grams)
        current_sentence = start
        current_length = len(start)
        while current_length < avg_length:
            next_gram = choice(a=grams, size=1, p=frequency)[0]
            if len(next_gram) == 1:
                continue
            current_sentence = (current_sentence + " " + next_gram).strip()
            current_length = len(current_sentence)

        return current_sentence

    def generate_content_burst(self) -> Tuple[List[str], List[float]]:
        """
        Generate content burst based on the prompt text.

        Returns:
            tuple: Tuple containing nouns and their frequency.
        """
        # preprocess_text = self.preprocess_document()
        bursts = self.spacy_multi_tagger(process_document=True, return_all_nouns=True)

        freq_dist = nltk.FreqDist(bursts)
        nouns = []
        frequency = []

        for word, count in freq_dist.items():
            nouns.append(word)
            frequency.append(count / sum(freq_dist.values()))

        return nouns, frequency

    def save_bursts(self, extend_file_save_name: str = "") -> str:
        """
        Generate and save burst adversarials to a tsv file.

        Args:
            extend_file_save_name (str, optional): Additional name to append to the
                saved file name (default is "").

        Returns:
            str: The first sentence of the generated burst adversarials.
        """

        nouns, frequency = self.generate_content_burst()
        file_name = os.path.basename(self.prompt_text)

        index = 0
        os.getcwd()

        save_name = file_name.replace(".txt", "")

        if extend_file_save_name:
            save_file_path = (
                f"{Gp.RESULT_BURST_ATTACK_RESULT.value}/"
                f"{save_name}_{extend_file_save_name}_burst_result.tsv"
            )
        else:
            save_file_path = (
                f"{Gp.RESULT_BURST_ATTACK_RESULT.value}/{save_name}_burst_result.tsv"
            )

        with open(
            save_file_path,
            "w+",
            encoding="utf-8",
        ) as file:
            csv_writer = csv.writer(file, delimiter="\t")

            header = "id", "EssaySet", "eassay_score", "essay_score", "EssayText"

            csv_writer.writerow(header)

            for i in range(self.burst_amount):
                sentence = self.get_text(nouns, frequency, 44)
                data_list = [
                    "10700" + "{0:03}".format(index),
                    self.prompt_text,
                    0,
                    0,
                    sentence,
                ]

                csv_writer.writerow(data_list)

                index += 1

        return sentence


if __name__ == "__main__":
    pass
