# Standard
import glob
import os

# Pip
import typer

# Custom
from adversaries.settings.constants.natural_order_group import NaturalOrderGroup
from adversaries.settings.messages.message_keys import MessageKeys as Mk
from adversaries.settings.constants.constant_paths import GeneralPaths as Gp
from adversaries.docs_processor.app_docs_processor import app_docs_processor
from adversaries.burst_attack.app_burst_attack import app_burst_attack
from adversaries.attacker_evaluator.app_attacker_evaluator import app_attack_evaluator
from adversaries.settings.logger.basic_logger import (
    catch_and_log_error,
    catch_and_log_info,
)

# Message keys
main_keys = Mk.MainApp
general_keys = Mk.General

# Apps
main_app = typer.Typer(
    name=main_keys.APP_NAME,
    help=main_keys.APP_NAME_HELP,
    no_args_is_help=True,
    add_completion=False,
    cls=NaturalOrderGroup,
)
main_app.add_typer(app_docs_processor, help=Mk.DocProcessor.APP_NAME_HELP.value)
main_app.add_typer(app_burst_attack, help=Mk.ContentBurstGenerator.APP_NAME_HELP.value)
main_app.add_typer(app_attack_evaluator, help=Mk.AttackerEvaluator.APP_NAME_HELP.value)


@main_app.command(
    help=main_keys.EMPTY_DIRECTORY.value, name=main_keys.EMPTY_DIRECTORY_HELP.value
)
def empty_chosen_directory(
    trg_dir: str = typer.Option(
        Gp.LOG_DIR.LOG_DIR.value,
        main_keys.EMPTY_DIRECTORY_TRG_LONG.value,
        main_keys.EMPTY_DIRECTORY_TRG_SHORT.value,
        help=main_keys.EMPTY_DIRECTORY_TRG_HELP.value,
    ),
    file_type: str = typer.Option(
        general_keys.FILE_TYPE_LOG.value,
        general_keys.FILE_TYPE_LONG.value,
        general_keys.FILE_TYPE_SHORT.value,
        help=main_keys.FILE_TYPE_HELP.value,
    ),
) -> None:
    """
    Deletes the files in a selected directory.

    Args:
        trg_dir (str): Directory to be emptied.
        file_type (str): File type located in the target directory to be deleted.
    Returns:
        None
    """

    if file_type == "all":
        file_type = "*"

    file_directory = f"{trg_dir}/*.{file_type}"

    files_to_be_deleted = glob.glob(file_directory)

    folder_path = os.path.exists(trg_dir)

    if len(files_to_be_deleted) > 0 and folder_path is True:
        for file in files_to_be_deleted:
            os.remove(file)

        catch_and_log_info(
            custom_message=f"The files '{file_directory}' have been deleted.",
            echo_msg=True,
        )

    elif len(files_to_be_deleted) == 0 and folder_path is True:
        catch_and_log_info(
            custom_message=f"The folder '{trg_dir}' is already empty.", echo_msg=True
        )

    else:
        catch_and_log_info(custom_message=f"An unknown error occurred.", echo_msg=True)


if __name__ == "__main__":

    # Create log
    LOG_EXISTS = os.path.exists("log")
    if not LOG_EXISTS:
        os.mkdir("log")
        open("log/hello_world.log", mode="w+").write("Hello, I am a log file!")

    try:
        main_app()
        catch_and_log_info(custom_message=main_keys.MAIN_APP_START.value)
    except Exception as e:
        msg = Mk.MainApp.MAIN_APP_FATAL_ERROR.value
        catch_and_log_error(error=e, custom_message=msg, kill_if_fatal_error=True)
