# Standard
import csv
import os
import re

from glob import glob

# Pip
import matplotlib.pyplot as plt

# Custom
from adversaries.settings.constants.constant_paths import GeneralPaths as Gp
from adversaries.settings.messages.message_keys import MessageKeys as Mk
from adversaries.settings.logger.basic_logger import catch_and_log_info

attk_keys = Mk.AttackerEvaluator


def find_tsv_files():
    """
    This function retrieves a list of TSV files from the specified directory path.

    Returns:
        list: A list containing the paths to all found TSV files.
    """

    file = Gp.RESULT_ARR_SENTENCE_RESULTS.value
    results = glob(f"{file}/*.tsv")

    catch_and_log_info(custom_message=attk_keys.TSV_FILES.value, echo_msg=True)

    return results


def process_tsv_files(files) -> tuple:
    """
    This function processes a list of TSV files, extracting prompt and score data.

    Args:
        files (list): A list containing the paths to TSV files.

    Returns:
        tuple: A tuple containing two dictionaries, `prompt_results` and `count_results`.
            - prompt_results (dict): A dictionary where keys are file paths and values are
                dictionaries mapping scores (0-3) to lists of corresponding sentences.
            - count_results (dict): A dictionary where keys are file paths and values are
                dictionaries mapping scores (0-3) to lists containing the number of sentences
                for each score.
    """

    pattern = re.compile("[^\w\s]")
    prompt_results = {}
    count_results = {}

    for tsv_file in files:
        prompt_results[tsv_file] = {str(i): [] for i in range(4)}
        count_results[tsv_file] = {str(i): [] for i in range(4)}

        with open(tsv_file, mode="r", encoding="utf-8") as file:
            csv_reader = csv.reader(file, delimiter="\t")
            sentences = list(csv_reader)

            # Basically, from each content burst file, two sentences are collected
            # and stored in a separate file
            for row in sentences:
                sentence, score = row

                count_results[tsv_file][score].append(sentence)
                # Ignore sentences with numbers
                if pattern.search(sentence) is None:

                    # Only add two sentences from each file to the excerpt file
                    if len(prompt_results[tsv_file][score]) < 2:
                        prompt_results[tsv_file][score].append(sentence)

    catch_and_log_info(
        custom_message=attk_keys.TSV_FILES_PROCESSED.value, echo_msg=True
    )

    return prompt_results, count_results


def save_results(prompt_results: dict) -> None:
    """
    This function saves prompt and score data to CSV files.

    Args:
        prompt_results (dict): A dictionary where keys are file paths and values are
            dictionaries mapping scores (0-3) to lists of corresponding sentences.
    """

    for slice_index in range(4):
        with open(
            f"{Gp.RESULT_ARR_SENTENCE_RESULT_EXCERPT.value}/arr_excerpt_score_{slice_index}.csv",
            mode="w+",
            encoding="utf-8",
        ) as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(("Example Id", "Prompt Type", f"Score {slice_index}"))
            for prompt_file, prompt_data in prompt_results.items():
                file_path, file_name = os.path.split(prompt_file)
                values = list(prompt_data.values())
                prompt_name = (
                    file_name.split(".")[0].replace("_", " ").replace("ARR", "").strip()
                )
                if len(values[slice_index]) > 0:
                    for id, sen in enumerate(values[slice_index], start=1):
                        csv_writer.writerow((id, prompt_name, sen))
                else:
                    csv_writer.writerow(("/", prompt_name, "/"))

    catch_and_log_info(custom_message=attk_keys.SAVE_PROMPT_DATA.value, echo_msg=True)


def calculate_score_distribution(count_results: dict) -> tuple:
    """
    This function calculates the distribution of scores across all processed files.

    Args:
        count_results (dict): A dictionary where keys are file paths and values are
            dictionaries mapping scores (0-3) to lists containing the number of sentences
            for each score.

    Returns:
        tuple: A tuple containing four integers representing the counts of sentences with
            scores 0, 1, 2, and 3, respectively.
    """

    zero_count = one_count = two_count = three_count = 0

    for file_results in count_results.values():
        zero_count += len(file_results["0"])
        one_count += len(file_results["1"])
        two_count += len(file_results["2"])
        three_count += len(file_results["3"])

    catch_and_log_info(
        custom_message=attk_keys.SAVE_SCORE_DISTRUBITON_COUNT.value, echo_msg=True
    )

    return zero_count, one_count, two_count, three_count


def plot_score_distribution(counts: tuple) -> None:
    """
    This function creates a bar chart to visualize the distribution of scores.

    Args:
        counts (tuple): A tuple containing four integers representing the counts of sentences
            with scores 0, 1, 2, and 3, respectively.
    """

    values = list(counts)

    labels = ["zero", "one", "two", "three"]

    plt.bar(labels, values, color=["blue", "orange", "green", "red"])
    plt.yscale("log")
    plt.xlabel("Scores")
    plt.ylabel("Counts (log scale)")
    plt.title("Score Distribution (log scale)")
    plt.savefig(f"{Gp.VISUALIZE_ARR_SCORE_DISTRIBUTION.value}/score_distribution.png")

    catch_and_log_info(
        custom_message=attk_keys.SAVE_SCORE_DISTRUBITON_PLOT.value,
        echo_msg=True,
    )


if __name__ == "__main__":
    tsv_files = find_tsv_files()
    prompt_results, count_results = process_tsv_files(tsv_files)
    save_results(prompt_results)
    score_distribution = calculate_score_distribution(count_results)
    plot_score_distribution(score_distribution)
