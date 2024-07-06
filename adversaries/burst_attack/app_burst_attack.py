# Standard
# None

# Pip
import typer

# Custom
from adversaries.settings.constants.natural_order_group import NaturalOrderGroup
from adversaries.burst_attack.content_burst_generator import (
    ContentBurstGenerator as Cbg,
)

from adversaries.settings.constants.constant_paths import GeneralPaths as Gp
from adversaries.settings.logger.basic_logger import catch_and_log_info
from adversaries.settings.messages.message_keys import MessageKeys as Mk

general_keys = Mk.General
content_burst_keys = Mk.ContentBurstGenerator

app_burst_attack = typer.Typer(
    no_args_is_help=True,
    name=content_burst_keys.APP_NAME.value,
    add_completion=False,
    cls=NaturalOrderGroup,
)


@app_burst_attack.command(
    name=content_burst_keys.GENERATE_CONTENT_BURST.value,
    help=content_burst_keys.APP_NAME_HELP.value,
)
def generate_content_burst(
    file_name: str = typer.Option(
        Gp.RESULT_DEFAULT_BURST_BASE_TEXT.value,
        general_keys.FILE_NAME_LONG.value,
        general_keys.FILE_NAME_SHORT.value,
        help=general_keys.FILE_NAME_HELP.value,
    ),
    extend_file_save_name: str = typer.Option(
        content_burst_keys.EXTEND_FILE_SAVE_NAME_DEFAULT.value,
        content_burst_keys.EXTEND_FILE_SAVE_NAME_LONG.value,
        content_burst_keys.EXTEND_FILE_SAVE_NAME_SHORT.value,
        help=content_burst_keys.EXTEND_FILE_SAVE_NAME_HELP.value,
    ),
    spacy_tagger_language: str = typer.Option(
        content_burst_keys.SPACY_TAGGER_LANG_DEFAULT.value,
        content_burst_keys.SPACY_TAGGER_LANG_LONG.value,
        content_burst_keys.SPACY_TAGGER_LANG_SHORT.value,
        help=content_burst_keys.SPACY_TAGGER_LANG_HELP.value,
    ),
) -> None:
    """Generate content bursts for the respective prompt and language

    Args:
        file_name (str): The base text file to generate bursts from.
        extend_file_save_name (str): The name to extend the saved file with.
        spacy_tagger_language (str): The language for the SpaCy tagger.

    Returns:
        None
    """
    catch_and_log_info(
        custom_message=content_burst_keys.APP_NAME_HELP.value, echo_msg=True
    )

    # Generate content bursts
    generator = Cbg(language=spacy_tagger_language, prompt_text=file_name)

    # Save content bursts
    bursts = generator.save_bursts(extend_file_save_name=extend_file_save_name)

    catch_and_log_info(
        custom_message=content_burst_keys.BURST_COMPLETE.value, echo_msg=True
    )
    return bursts


if __name__ == "__main__":
    app_burst_attack()
