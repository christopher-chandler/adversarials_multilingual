# Standard
import os

# Pip
import typer
from tqdm import tqdm

# Custom
from adversaries.settings.constants.natural_order_group import NaturalOrderGroup
from adversaries.docs_processor.docx_prompt_to_text import DocxPromptToText
from adversaries.settings.constants.constant_paths import GeneralPaths as Gp
from adversaries.settings.logger.basic_logger import catch_and_log_info
from adversaries.settings.messages.message_keys import MessageKeys as Mk

doc_processor_keys = Mk.DocProcessor

# App
app_docs_processor = typer.Typer(
    no_args_is_help=True,
    name=doc_processor_keys.APP_NAME.value,
    help=doc_processor_keys.APP_NAME_HELP.value,
    add_completion=False,
    cls=NaturalOrderGroup,
)


@app_docs_processor.command(
    name=doc_processor_keys.EXTRACT_TEXT_FROM_PROMPTS.value,
    help=doc_processor_keys.EXTRACT_TEXT_FROM_PROMPTS_HELP.value,
)
def extract_text_from_all_prompts() -> None:
    """
    Extract text from all prompt files in the specified directory.

    This function walks through the prompt directory specified in the GeneralPaths,
    extracting text from all .docx files found. It utilizes the DocxPromptToText class
    to perform the conversion from .docx to .txt format.

    :return:
        None
    """
    catch_and_log_info(
        custom_message=doc_processor_keys.EXTRACT_TEXT_FROM_PROMPTS_HELP.value,
        echo_msg=True,
    )

    prompt_data_dir = list(os.walk(Gp.PROMPT_DIR.value))[1:]

    for folder in prompt_data_dir:
        f_dir, _, files = folder

        for docx_file in tqdm(sorted(files), desc=f"Processing files {f_dir}"):
            absolute_file = f"{f_dir}/{docx_file}"

            if ".docx" in docx_file:
                prompt = DocxPromptToText(absolute_file)
                docx_to_text = docx_file.replace(".docx", ".txt")
                extracted_text = f"{Gp.RESULT_PROMPT_TXT.value}/{docx_to_text}"
                prompt.docx_to_text(save_name=extracted_text)

    catch_and_log_info(
        custom_message=doc_processor_keys.EXTRACT_TEXT_COMPLETE.value, echo_msg=True
    )


if __name__ == "__main__":
    extract_text_from_all_prompts()
