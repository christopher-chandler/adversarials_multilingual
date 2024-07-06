# Standard
from enum import Enum

# Pip
# None

# Standard
# None


class MessageKeys:
    """
    Here the names and messages, which are output by the program,
    are stored centrally.
    """

    class General(Enum):
        FILE_TYPE_LOG = "log"
        FILE_NAME_LONG = "--file_name"
        FILE_NAME_SHORT = "-name"
        FILE_NAME_HELP = "The name of the file to be passed."

        FILE_TYPE_LONG = "--file_type"
        FILE_TYPE_SHORT = "-type"

        SAVE_DIR_LONG = "--save-directory"

        SAVE_RESULTS_LONG = "--save-results"
        SAVE_DIR_SHORT = "-save"
        SAVE_RESULTS_HELP = "The name of the result file"
        SAVE_DATA = "The results have been saved."
        SAVE_DIR_HELP = "The directory where the results will be saved."

        ECHO_DEFAULT = False
        ECHO_LONG = "--echo"
        ECHO_SHORT = "-e"
        ECHO_HELP = "The results should be shown in the console."

        DISABLE_QWK = False
        DISABLE_QWK_LONG = "--quadratically_weighted_kappa"
        DISABLE_QWK_SHORT = "-qwk"
        DISABLE_QWK_HELP = "Activate Quadratically Weighted Kappa output"

        # Errors
        MISSING_HOME_DIR = "The home directory was not properly specified."
        GENERAL_ERROR = "An error occurred."
        FILE_MISSING = "The file does not exist."

    class MainApp(Enum):
        APP_NAME = "Content Burst Generator"
        APP_NAME_HELP = "The main app of Content Burst Generator"

        EMPTY_DIRECTORY = "Empty a selected directory"
        EMPTY_DIRECTORY_HELP = "empty_directory"

        EMPTY_DIRECTORY_TRG_LONG = "--target_directory"
        EMPTY_DIRECTORY_TRG_SHORT = "-target"
        EMPTY_DIRECTORY_TRG_HELP = "The directory that is to be emptied"

        FILE_TYPE_HELP = (
            "The files to be deleted. 'all' deletes "
            "\nall files in the specified directory "
        )

        MAIN_APP_START = "The main application has been started."
        MAIN_APP_FATAL_ERROR = (
            "A problem occurred within the main application. "
            "Please check the log file. "
        )

    class AttackerEvaluator(Enum):

        APP_NAME = "attack_evaluator"
        APP_NAME_HELP = "Evaluate how successful the adversaries were."

        SINGULAR_ARR = "singular"
        SINGULAR_ARR_HELP = "Generate ARR for a language"
        SINGULAR_ARR_LANG_DEFAULT = "en"
        SINGULAR_ARR_LANG_LONG = "--language"
        SINGULAR_ARR_LANG_SHORT = "-ln"
        SINGULAR_ARR_LANG_HELP = "The language to be evaluated."

        SINGULAR_ARR_PROMPT_NUM_DEFAULT = "1"
        SINGULAR_ARR_PROMPT_NUM_LONG = "--prompt_num"
        SINGULAR_ARR_PROMPT_NUM_SHORT = "-pn"
        SINGULAR_ARR_PROMPT_NUM_HELP = "The prompt text to be evaluated."

        RATE_ATTACK = "Rate adversarial attack"
        SAVE_ATTACK = "Save adversarial attack results"
        SAVE_ARR = "The ARR rate has been generated and saved."

        EVALUATION_METRIC = "EVALUATION METRIC"
        EVALUATION_METRIC_ARR = "ARR"
        EVALUATION_METRIC_CROSS_VALID = "QWK"

        MULTI_ARR_NAME = "multiple"
        MULTI_ARR_HELP = "Generate ARR for all languages"

        VISUALIZE_ARR_NAME = "visualize"
        VISUALIZE_ARR_HELP = "Generate ARR, QWK and Noun distribution visualization for all languages"
        VISUALIZE_PLOT_LANGUAGES = "Languages"
        VISUALIZE_REJECTION_RATE = "Rejection Rate"
        VISUALIZE_TITLE = "Adversarial Rejection Rate Based on Noun Content Bursts"
        VISUALIZE_FILE_NAME = "results/visualization/content_bursts_arr_results"

        VISUALIZE_NOUN_NONE_NOUN_RATIO = "Diagram for noun/none-noun saved"
        PROMPT_FILES_COLLECTED = "Prompt files found and collected."
        CALCULATING_POS = "Calculating POS counts for each prompt."
        PROMPT_FILES = "Processing Prompt Files"
        FIGURE_RATIO = "Successfully saved figure with NOUN/NONE_NOUN POS count ratio."
        CALCULATION_COMPLETE = "Successfully wrote POS counts to CSV file:"

        RATIO_PROCESS_DONE = "Process complete and results saved"

        GENERATE_EXCERPTS_NAME = "generate_excerpts"
        GENERATE_EXCERPTS_HELP = (
            "generate score excerpts of the ARR results using the TSV burst files"
        )
        TSV_FILES = "The Content burst TSV files found."
        TSV_FILES_PROCESSED = (
            "The excerpts have been generated and score distribution counted."
        )
        SAVE_PROMPT_DATA = "Prompt and score data saved to CSV files."
        SAVE_SCORE_DISTRUBITON_COUNT = (
            "The score distrubtion of the content bursts saved."
        )
        SAVE_SCORE_DISTRUBITON_PLOT = (
            "The score distribution plot saved as score_distribution.png"
        )

    class ContentBurstGenerator(Enum):
        APP_NAME = "burst_attack"
        APP_NAME_HELP = "Automatically generate adversarials based on nouns"

        GENERATE_CONTENT_BURST = "generate_burst"

        SPACY_TAGGER_LANG_DEFAULT = "en"
        SPACY_TAGGER_LANG_LONG = "--language"
        SPACY_TAGGER_LANG_SHORT = "-ln"
        SPACY_TAGGER_LANG_HELP = (
            "The language of the prompts that is used for the Spacy tagger"
        )

        EXTEND_FILE_SAVE_NAME_DEFAULT = ""
        EXTEND_FILE_SAVE_NAME_LONG = "--extend_file_save_name"
        EXTEND_FILE_SAVE_NAME_SHORT = "-extended"
        EXTEND_FILE_SAVE_NAME_HELP = (
            "makes the file name more descriptive by extending its name."
        )

        BURST_COMPLETE = "The adversarial bursts have been generated and saved."

    class DocProcessor(Enum):
        APP_NAME = "docs_processor"
        APP_NAME_HELP = "Process documents in order to extract prompts"
        EXTRACT_TEXT_FROM_PROMPTS = "extract_prompt_text"
        EXTRACT_TEXT_FROM_PROMPTS_HELP = "Extract text from the .doc prompt files"
        EXTRACT_TEXT_COMPLETE = (
            "The text from the prompts has been extracted and saved."
        )
