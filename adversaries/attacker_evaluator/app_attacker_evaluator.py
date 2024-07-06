# Standard
import csv
import os


# Pip
import typer
import pandas as pd

from matplotlib import pyplot as plt
from rich.console import Console
from rich.table import Table
from tqdm import tqdm

# Custom
from adversaries.settings.constants.constant_paths import GeneralPaths as Gp
from adversaries.settings.constants.natural_order_group import NaturalOrderGroup
from adversaries.settings.messages.message_keys import MessageKeys as Mk

from adversaries.attacker_evaluator import scoring_functions as sf
from adversaries.burst_attack.app_burst_attack import generate_content_burst
from adversaries.settings.logger.basic_logger import (
    catch_and_log_info,
    catch_and_log_error,
)

from adversaries.attacker_evaluator.arr_score_processor import (
    calculate_score_distribution,
    find_tsv_files,
    process_tsv_files,
    plot_score_distribution,
    save_results,
)
from adversaries.attacker_evaluator.noun_distribution_prompt import (
    visualize_noun_none_noun_results,
)

# Message Keys
general_keys = Mk.General
attk_keys = Mk.AttackerEvaluator

# Typer app
app_attack_evaluator = typer.Typer(
    no_args_is_help=True,
    name=attk_keys.APP_NAME.value,
    help=attk_keys.APP_NAME_HELP.value,
    add_completion=False,
    cls=NaturalOrderGroup,
)

CONSOLE = Console()
TABLE = Table("Key", "Value")


@app_attack_evaluator.command(
    name=attk_keys.SINGULAR_ARR.value,
    help=attk_keys.SINGULAR_ARR_HELP.value,
)
def generate_singular_arr(
    lang: str = typer.Option(
        attk_keys.SINGULAR_ARR_LANG_DEFAULT.value,
        attk_keys.SINGULAR_ARR_LANG_LONG.value,
        attk_keys.SINGULAR_ARR_LANG_SHORT.value,
        help=attk_keys.SINGULAR_ARR_LANG_HELP.value,
    ),
    prompt_num: str = typer.Option(
        attk_keys.SINGULAR_ARR_PROMPT_NUM_DEFAULT.value,
        attk_keys.SINGULAR_ARR_PROMPT_NUM_LONG.value,
        attk_keys.SINGULAR_ARR_PROMPT_NUM_SHORT.value,
        help=attk_keys.SINGULAR_ARR_PROMPT_NUM_HELP.value,
    ),
    echo_results: bool = typer.Option(
        general_keys.ECHO_DEFAULT.value,
        general_keys.ECHO_LONG.value,
        general_keys.ECHO_SHORT.value,
        help=general_keys.ECHO_HELP.value,
    ),
) -> None:
    """
    It generates the ARR for a specified language and prompt number
    This function takes in parameters for language, prompt number,
    and whether to echo results.

    Args:
        lang (str): The language in which the prompt is given.
        prompt_num (int): The number of the prompt to be used.
        echo_results (bool): Boolean indicating whether to echo the results.

    Returns:
        None
    """
    echo_msg = f"The following is being generate - Language: {lang}, Prompt Number: {prompt_num}"

    catch_and_log_info(custom_message=echo_msg, echo_msg=True)

    # die Dateien orig300 und orig werden als 'en' behandelt.
    english_file_variant = "en" in lang and lang != "en"

    if english_file_variant:
        content_burst_base_file = f"results/prompt_txt/Prompt{prompt_num}_en.txt"
    else:
        content_burst_base_file = f"results/prompt_txt/Prompt{prompt_num}_{lang}.txt"

    training_prompt = f"resources/data/monolingual_ASAP_data_with_scores/ASAP_{lang}_prompt{prompt_num}.tsv"
    adversarial = f"results/burst_attack_txt/Prompt{prompt_num}_{lang}_burst_result.tsv"

    # Es wird nicht getestet, ob die Adversarial-datei exisitiert,
    # da sie erst spaeter erzeugt wird

    try:
        if english_file_variant:
            add_on = lang.replace("en_", "")

            # Die orig300 und orig werden abgeschnitten damit Spacy nur "EN"
            # also die Sprache waehlt.
            lang = lang[:2]

            generate_content_burst(
                spacy_tagger_language=lang,  # check language,
                file_name=content_burst_base_file,
                extend_file_save_name=add_on,
            )
        else:
            generate_content_burst(
                file_name=content_burst_base_file,
                spacy_tagger_language=lang,
                extend_file_save_name="",
            )

    except Exception as e:

        error_msg = (
            f"Error: The combination lang: '{lang}' prompt_num: '{prompt_num}' is "
            "is not valid. \nThe languages 'en, fr, de, es' and "
            "prompt numbers '1, 2, 10' are valid."
            "Or\n"
            "There could be a problem with the encoding of the prompt files. "
            "Please check them."
        )
        catch_and_log_error(e, custom_message=error_msg, echo_msg=True,echo_traceback=True)
        raise SystemExit()

    # Hier wird jetzt ein Modell auf einem Prompt trainiert
    # und dann auf die Adversarials angewendet
    # Ganz wichtig: train_file und adversarial_file muessen sich auf den
    # gleichen Datensatz + Prompt beziehen!
    catch_and_log_info(custom_message=attk_keys.RATE_ATTACK.value, echo_msg=True)

    swm_model = sf.construct_svm_scoring_model()
    cross_valid_qwk = sf.cross_validation_qwk(swm_model, training_prompt)

    y_pred, arr = sf.arr_for_trained_model(swm_model, training_prompt, adversarial)
    PROMPT = os.path.basename(training_prompt).replace(".tsv", "")
    METHOD = "CONTENT_BURST"

    arr_data_results = {
        "METHOD": METHOD,
        "PROMPT": PROMPT,
        "PROMPT_NUMBER": prompt_num,
        "LANGUAGE": lang,
        "ARR": arr,
    }

    catch_and_log_info(custom_message=attk_keys.SAVE_ATTACK.value, echo_msg=True)

    with open(
        Gp.RESULT_SINGLE_ARR_SAVE.value,
        mode="w+",
        newline="",
    ) as save_file:
        fieldnames = ["METHOD", "LANGUAGE", "PROMPT", "PROMPT_NUMBER", "ARR"]
        csv_writer = csv.DictWriter(save_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerow(arr_data_results)

        for entry in arr_data_results:
            TABLE.add_row(entry, str(arr_data_results.get(entry)))

        if echo_results:
            CONSOLE.print(TABLE)
            typer.echo(Mk.General.SAVE_DATA.value)

    catch_and_log_info(custom_message=attk_keys.SAVE_ARR.value, echo_msg=True)

    return arr_data_results, cross_valid_qwk


@app_attack_evaluator.command(
    name=Mk.AttackerEvaluator.MULTI_ARR_NAME.value,
    help=Mk.AttackerEvaluator.MULTI_ARR_HELP.value,
)
def generate_multi_arr() -> None:
    """
    This generates the ARR for all the languages (en, es, fr, de) and saves the results.

    :return:
        None
    """
    LANGUAGE_CHOICES = ["en", "en_orig300", "en_orig", "es", "fr", "de"]
    #LANGUAGE_CHOICES = ["fr"]

    PROMPT_CHOICES = [1, 2, 10]

    # Header fuer Ergebniss-Datei
    ARR_HEADER = Gp.RESULT_ARR_HEADER.value

    with open(ARR_HEADER) as arr_header_file:
        csv_reader = csv.reader(arr_header_file)
        arr_header_data = [row for row in csv_reader][0]
        arr_evaluation_result = {
            header_entry: dict() for header_entry in arr_header_data
        }

    # Fortschrittsbalken aufstellen
    total_iterations = len(LANGUAGE_CHOICES) * len(PROMPT_CHOICES)
    progress_bar = tqdm(total=total_iterations, desc="Processing Multi-Arr")

    arr_result = dict()
    cross_valid_qwk_result = dict()

    arr_result[attk_keys.EVALUATION_METRIC.value] = (
        attk_keys.EVALUATION_METRIC_ARR.value
    )
    cross_valid_qwk_result[attk_keys.EVALUATION_METRIC.value] = (
        attk_keys.EVALUATION_METRIC_CROSS_VALID.value
    )

    # Alle Sprachen analysieren
    for num in PROMPT_CHOICES:
        for choice in LANGUAGE_CHOICES:
            # Die Adversarials des enstsprechenden Prompts austesten
            # Das Ergebniss als int zurueck geben.
            lang_arr_result, cross_valid_qwk = generate_singular_arr(
                choice, num, echo_results=False
            )

            lang_prompt_description = lang_arr_result.get("PROMPT").replace("ASAP_", "")
            arr_result[lang_prompt_description] = lang_arr_result.get("ARR")
            cross_valid_qwk_result[lang_prompt_description] = round(cross_valid_qwk, 2)

            # Ergebnisse zwischenspeichern
            arr_evaluation_result[lang_prompt_description] = lang_arr_result

            progress_bar.update(1)

    progress_bar.close()  # Close the progress bar when done

    # Die Ergebnisse speichern
    file_standard = Gp.RESULT_MULTI_ARR_SAVE.value
    file_pivoted = Gp.RESULT_MULTI_ARR_SAVE.value.replace(
        "arr_results", "pivoted_arr_results"
    )

    """ Example
    Standard output
    EVALUATION METRIC,en_prompt1,en_prompt2,en_prompt10
    ARR,0.999,1.0,0.999
    QWK,0.52,0.15,0.56
    """

    with open(file_standard, mode="w+", encoding="UTF-8", newline="") as save_arr_file:

        field_names = list(arr_result.keys())

        csvDictWriter = csv.DictWriter(save_arr_file, field_names)
        csvDictWriter.writeheader()

        csvDictWriter.writerow(arr_result)
        csvDictWriter.writerow(cross_valid_qwk_result)

    """ Example
    # Output - pivoted table 
    Language Prompt,ARR,QWK
    en_prompt1,0.999,0.52
    en_prompt2,1.0,0.15
    en_prompt10,0.999,0.56
    """
    prompt_files = list(arr_result.keys())

    arr_qwk_pivoted_data = {"EVALUATION METRIC": ["ARR", "QWK"]}

    for row in prompt_files:
        arr_qwk_pivoted_data[row.replace("_", " ")] = list()

    for row1, row2 in zip(arr_result, cross_valid_qwk_result):
        arr_qwk_pivoted_data[row1.replace("_", " ")].append(arr_result.get(row1))
        arr_qwk_pivoted_data[row2.replace("_", " ")].append(
            cross_valid_qwk_result.get(row2)
        )

    df = pd.DataFrame(arr_qwk_pivoted_data)

    # Pivot the DataFrame
    pivot_df = (
        df.set_index("EVALUATION METRIC")
        .T.reset_index()
        .rename(columns={"index": "Language Prompt"})
    )

    # Save to CSV
    pivot_df.to_csv(file_pivoted, index=False)


@app_attack_evaluator.command(
    name=Mk.AttackerEvaluator.VISUALIZE_ARR_NAME.value,
    help=Mk.AttackerEvaluator.VISUALIZE_ARR_HELP.value,
)
def visualize_arr_results():
    """
    Visualizes data from a CSV file containing languages and rejection rates.
    It also creates a digram for the noun/none-noun distribution
    Reads data from a CSV file, extracts languages and rejection rates,
    and creates a bar plot visualizing rejection rates for each language.

    Args:
        None

    Returns:
        None
    """

    def __create_chart(metric_label, prompt_label, metric_values, color="blue") -> None:
        """
        Creates a bar chart to visualize metric values.

        Args:
            metric_label (str): A string indicating the label for the metric being visualized.
            prompt_label (str): A string indicating the label for the prompt.
            metric_values (list): A list or array of numeric values representing the metric values.
            color (str, optional): A string specifying the color of the bars. Default is "blue".

        Returns:
            None
        """

        plt.figure()  # Create a new figure
        plt.bar(
            prompt_label, metric_values, color=color
        )  # Pass both x-coordinates and heights
        plt.xlabel(Mk.AttackerEvaluator.VISUALIZE_PLOT_LANGUAGES.value)
        plt.ylabel(
            f"{Mk.AttackerEvaluator.VISUALIZE_REJECTION_RATE.value} ({metric_label})"
        )
        plt.title(Mk.AttackerEvaluator.VISUALIZE_TITLE.value)

        legend_labels = list(color_mapping.keys())
        legend_colors = list(color_mapping.values())
        legend_patches = [
            plt.Rectangle((0, 0), 1, 1, facecolor=color, edgecolor="black")
            for color in legend_colors
        ]

        plt.legend(
            legend_patches,
            legend_labels,
            loc="lower left",
            bbox_to_anchor=(-0.1, -0.6),
            fancybox=True,
            shadow=True,
        )

        plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
        plt.tight_layout()  # Adjust layout to prevent cutting off labels
        title = Mk.AttackerEvaluator.VISUALIZE_FILE_NAME.value
        plt.savefig(f"{title}_{metric_label}.png")
        catch_and_log_info(custom_message=Mk.General.SAVE_DATA.value, echo_msg=True)

    data_file = Gp.RESULT_MULTI_ARR_SAVE.value

    ###################################################################################

    with open(data_file, mode="r") as csv_data:
        csv_reader = csv.reader(csv_data)
        data = list(csv_reader)

        labels = [i[0] for i in data][1:]
        prompt_labels = data[0][1:]
        arr_label, arr = labels[0], data[1:][0][1:]
        qwk_label, qwk = labels[1], data[2:][0][1:]

        arr_rates = [float(rate) for rate in arr]  # Convert rates to float
        qwk_rates = [float(rate) for rate in qwk]  # Convert rates to float

        ## Creating colors for the labels
        color_mapping = {
            "en": "darkblue",
            "es": "darkred",
            "fr": "darkorange",
            "de": "gold",
        }
        labels = [col.split("_")[0] for col in prompt_labels]
        colors = [
            color_mapping.get(label, "gray") for label in labels
        ]  # Default to gray if label not found in mapping

        __create_chart(arr_label, prompt_labels, arr_rates, color=colors)
        __create_chart(qwk_label, prompt_labels, qwk_rates, color=colors)

    catch_and_log_info(
        custom_message=Mk.AttackerEvaluator.VISUALIZE_ARR_HELP.value, echo_msg=True
    )

    visualize_noun_none_noun_results()
    catch_and_log_info(
        custom_message=Mk.AttackerEvaluator.VISUALIZE_NOUN_NONE_NOUN_RATIO.value,
        echo_msg=True,
    )


@app_attack_evaluator.command(
    name=attk_keys.GENERATE_EXCERPTS_NAME.value,
    help=attk_keys.GENERATE_EXCERPTS_HELP.value,
)
def generate_excerpts():
    """
    Excerpts are taken the from the generated content burst files to see
    which sentences were given which scores. The results are then saved in the
    arr_sentence_result_excerpt folder. Also, the total distribution of all of the scores
    is saved as a total sum. A visualization of this score distribution can be found in
    visualization folder.

    :return:
        None
    """
    tsv_files = find_tsv_files()
    prompt_results, count_results = process_tsv_files(tsv_files)
    save_results(prompt_results)
    score_distribution = calculate_score_distribution(count_results)
    plot_score_distribution(score_distribution)


if __name__ == "__main__":
    #app_attack_evaluator()
    generate_multi_arr()