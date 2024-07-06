# Standard
import os
from glob import glob

from enum import Enum

# Pip
# None

# Custom
from adversaries.settings.logger.basic_logger import catch_and_log_error
from adversaries.settings.messages.message_keys import MessageKeys
from settings_manager import get_config_data


class GeneralPaths(Enum):

    # DIR
    MAIN_DIR = get_config_data().get("CONFIG_HOME_DIR")

    LOG_DIR = "log"
    PROMPT_DIR = "resources/data/Prompts/"

    # results
    RESULT_PROMPT_TXT = "results/prompt_txt"

    # Burst attack
    RESULT_ARR_SENTENCE_RESULTS = "results/arr_sentences_results"
    RESULT_ARR_SENTENCE_RESULT_EXCERPT = "results/arr_sentence_result_excerpt"
    RESULT_DEFAULT_BURST_BASE_TEXT = "results/prompt_txt/Prompt1_de.txt"
    RESULT_BURST_ATTACK_RESULT = f"results/burst_attack_txt"
    RESULT_ARR_HEADER = "results/adversarial_rejection_rates/arr.csv"
    RESULT_NOUN_NONE_DIST = "results/noun_none_noun_distribution"


    RESULT_SINGLE_ARR_SAVE = "results/adversarial_rejection_rates/single_save_file.csv"
    RESULT_MULTI_ARR_SAVE = (
        "results/adversarial_rejection_rates/content_bursts_arr_results.csv"
    )
    VISUALIZE_ARR_SCORE_DISTRIBUTION = f"results/visualization/"
    # Evaluator
    RESUOURCES_EVALUATOR_DUMMY_TRAIN_ATTACK = (
        "resources/data/attacker_evaluator_test/ASAP_de_prompt1.csv"
    )
    RESOURCES_EVALUATOR_DUMMY_ADVERSARIAL_PROMPT = (
        "resources/data/attacker_evaluator_test/dummy_adversarial_de_prompt1.txt"
    )

    # Prompts
    ALL_PROMPTS = glob(f"{MAIN_DIR}/results/prompt_txt/*.*")
    ALL_TRAINING_ASAP = glob(
        f"{MAIN_DIR}/resources/data/monolingual_ASAP_data_with_scores/*.*"
    )


try:
    '''
    The root directory should be defined here,
    so that the following paths are also correct afterwards.
    '''
    os.chdir(GeneralPaths.MAIN_DIR.value)
except Exception as e:
    catch_and_log_error(
        error=e,
        custom_message=MessageKeys.General.MISSING_HOME_DIR.value,
        kill_if_fatal_error=True,
    )

if __name__ == "__main__":
    pass
