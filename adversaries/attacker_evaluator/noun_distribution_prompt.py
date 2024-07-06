# Standard
import csv
import os

from glob import glob

# Pip
import matplotlib.pyplot as plt
import numpy as np

from tqdm import tqdm


# Custom
from adversaries.settings.constants.constant_paths import GeneralPaths as Gp
from adversaries.docs_processor.multilingual_spacy import MultiLingualSpacy as Mls
from adversaries.settings.logger.basic_logger import (
    catch_and_log_info,
    catch_and_log_error,
)
from adversaries.settings.messages.message_keys import MessageKeys as Mk

attk_keys = Mk.AttackerEvaluator


def uniform_path_key_abs_file_path(glob_files: list) -> dict:
    """
    Takes a list of file paths obtained with glob and returns a dictionary.

    Args:
        glob_files (list): List of file paths obtained with the `glob` function.

    Returns:
        dict: A dictionary where keys are filenames and values are tuples
        containing language and absolute file path.
    """

    path_file = dict()

    for prompt in glob_files:
        _, file_name = os.path.split(prompt)
        lang = file_name[-6:-4]
        path_file[file_name] = lang, prompt

    catch_and_log_info(
        custom_message=attk_keys.PROMPT_FILES_COLLECTED.value, echo_msg=True
    )

    return path_file


def sum_pos_counts(pos_values: dict) -> dict:
    """
    Calculates total and non-noun POS counts from a dictionary of POS counts.

    Args:
        pos_values (dict): A dictionary containing POS counts as key-value pairs.

    Returns:
        dict: A dictionary containing counts for NOUN, NONE_NOUN (all other POS),
        and TOTAL.
    """

    none_noun_count = 0
    total_word_count = 0

    for part_of_speech in pos_values:

        if part_of_speech != "NOUN":
            none_noun_count += pos_values.get(part_of_speech)

        total_word_count += pos_values.get(part_of_speech)

    part_of_speech_counts = {
        "NOUN": pos_values.get("NOUN"),
        "NONE_NOUN": none_noun_count,
        "TOTAL": total_word_count,
    }

    catch_and_log_info(custom_message=attk_keys.CALCULATING_POS.value, echo_msg=False)

    return part_of_speech_counts


def get_pos_count(incoming_files: dict) -> dict:
    """
    Gets part-of-speech (POS) counts for each prompt in a dictionary of file paths.

    Args:
        incoming_files (dict): A dictionary where keys are filenames and
        values are tuples containing language and absolute file path.

    Returns:
        dict: A dictionary where keys are prompt names (without extension or
         underscores) and values are dictionaries containing NOUN, NONE_NOUN,
          and TOTAL counts.
    """

    prompt_pos_count = dict()
    total_files = len(incoming_files)

    with tqdm(total=total_files, desc=attk_keys.PROMPT_FILES.value) as pbar:
        for file, (lang, file_path) in incoming_files.items():
            try:
                mulit_spacy = Mls(language=lang, incoming_document=file_path)

                tags = mulit_spacy.spacy_multi_tagger(
                    return_pos_count=True, process_document=True
                )

                spacy_pos_count = sum_pos_counts(tags)
                file = file.replace(".txt", "").replace("_", " ")
                prompt_pos_count[file] = spacy_pos_count
                pbar.update(1)  # Update progress bar for each file processed

            except Exception as e:
                catch_and_log_error(
                    e, f"Error processing file '{file_path}': {str(e)}", echo_msg=True
                )

    return prompt_pos_count


def save_fig(noun_none_noun_ratio_data: dict):
    """
    Saves a figure visualizing the ratio of NOUN and NONE_NOUN POS counts for each prompt.

    Args:
        noun_none_noun_ratio_data (dict): A dictionary where keys are prompt names
        and values are dictionaries containing NOUN, NONE_NOUN, and TOTAL counts.
    """

    categories = ["NOUN", "NONE_NOUN"]
    bar_width = 0.35
    index = np.arange(len(noun_none_noun_ratio_data))

    fig, ax = plt.subplots(figsize=(12, 6))

    # Plotting bars for each prompt
    total_counts = []
    for i, (filename, counts) in enumerate(noun_none_noun_ratio_data.items()):
        ypos = index[i]
        counts_values = [counts[cat] for cat in categories]
        total_count = sum(counts_values)
        total_counts.append(total_count)

        ax.barh(ypos, counts_values[0], bar_width, label="NOUN", color="blue")
        ax.barh(
            ypos,
            counts_values[1],
            bar_width,
            left=counts_values[0],
            label="NONE_NOUN",
            color="red",
        )

    ax.set_ylabel("Prompts")
    ax.set_xlabel("Counts")
    ax.set_title("Counts of NOUN and NONE_NOUN by Prompt")
    ax.set_yticks(index)
    ax.set_yticklabels(noun_none_noun_ratio_data.keys(), rotation=45, ha="right")

    # Show only two labels in the legend
    ax.legend(categories, title="Categories")

    plt.tight_layout()

    try:
        plt.savefig(
            f"{Gp.VISUALIZE_ARR_SCORE_DISTRIBUTION.value}/noun_none_noun_ratio.png"
        )
        catch_and_log_info(
            custom_message=attk_keys.FIGURE_RATIO.value,
            echo_msg=True,
        )
    except Exception as e:
        catch_and_log_error(e, f"Error saving figure: {str(e)}", echo_msg=True)


def write_csv_data(pos_data: dict):
    """
    Writes POS counts for each prompt to a CSV file.

    Args:
        pos_data (dict): A dictionary where keys are prompt names and
        values are dictionaries containing NOUN, NONE_NOUN, and TOTAL counts.
    """

    csv_filename = f"{Gp.RESULT_NOUN_NONE_DIST.value}/noun_none_noun_ratio.csv"
    try:
        with open(csv_filename, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)

            # Write header
            csv_writer.writerow(["Prompt", "NOUN", "NONE_NOUN", "TOTAL"])

            # Write data rows
            for prompt, counts in sorted(pos_data.items(), reverse=True):
                total_count = counts["NOUN"] + counts["NONE_NOUN"]
                csv_writer.writerow(
                    [
                        prompt,
                        counts["NOUN"],
                        counts["NONE_NOUN"],
                        total_count,
                    ]
                )

        catch_and_log_info(
            custom_message=f"{attk_keys.CALCULATION_COMPLETE.value} {csv_filename}",
            echo_msg=True,
        )
    except Exception as e:
        catch_and_log_error(e, f"Error writing CSV file: {str(e)}", echo_msg=True)


def visualize_noun_none_noun_results():
    """
    Visualizes and saves the distribution of NOUN and NONE_NOUN POS counts for all prompts.

    This function performs the following steps:
        1. Finds all prompt text files using `glob`.
        2. Creates a dictionary mapping filenames to language and absolute file paths.
        3. Calls `get_pos_count` to get POS counts for each prompt.
        4. Calls `save_fig` to generate and save a figure showing the NOUN/NONE_NOUN ratio.
        5. Calls `write_csv_data` to write POS counts to a CSV file.
    """
    catch_and_log_info(custom_message=f"Generating NOUN/NONE-NOUN ratio", echo_msg=True)
    prompt_text = sorted(glob("results/prompt_txt/*.*"))
    prompt_files = uniform_path_key_abs_file_path(prompt_text)
    prompt_pos = get_pos_count(prompt_files)
    save_fig(prompt_pos)
    write_csv_data(prompt_pos)
    catch_and_log_info(custom_message=attk_keys.RATIO_PROCESS_DONE.value, echo_msg=True)


if __name__ == "__main__":
    visualize_noun_none_noun_results()
