# Standard
import logging
import os
import traceback

# Pip
import typer

# Custom
from adversaries.settings.constants.constant_vars import SIMPLE_TIMESTAMP

# create log file


def get_logger(log_level=logging.ERROR) -> logging.Logger:
    """
    Returns a configured logger.

    This is a helper function to create a configured logger
    that can be used to write errors and information
    to a log file.

    Args:
        log_level (int, optional): The desired log level.
            By default, it is logging.ERROR.

    Returns:
        logging.Logger: A configured logger.
    """
    logger_formats = {
        logging.ERROR: (
            "Timestamp: %(asctime)s\n"
            "Logger Name: %(name)s\n"
            "Log Level: %(levelname)s\n"
            "Custom: %(custom_message)s\n"
            "Traceback: %(traceback)s\n"
            "Message: %(message)s\n"
            "Module: %(module)s\n"
            "Function: %(funcName)s\n"
            "Line: %(lineno)d\n"
            "File Path: %(pathname)s\n"
        ),
        logging.INFO: (
            "Timestamp: %(asctime)s\n"
            "Logger Name: %(name)s\n"
            "Log Level: %(levelname)s\n"
            "Message: %(message)s\n"
            "Module: %(module)s\n"
            "Function: %(funcName)s\n"
            "Line: %(lineno)d\n"
            "File Path: %(pathname)s\n"
        ),
    }

    log_file = "log"
    logging.basicConfig(
        filename=f"{log_file}/log_{SIMPLE_TIMESTAMP}.log",
        level=log_level,
        format=logger_formats.get(log_level),
    )

    return logging.getLogger()


def catch_and_log_error(
    error: Exception,
    custom_message: str,
    echo_msg=True,
    echo_traceback=False,
    kill_if_fatal_error=False,
    echo_color=typer.colors.RED,
) -> None:
    """
    Setup logger and log an error message.

    This function creates a logger and logs an error message
    along with a custom message and an optional traceback.

    Args:
        error (Exception): The occurred exception.
        custom_message (str): A custom message to be displayed in the log file.
        echo_msg (bool, optional): Whether to print the error message to the console.
            Defaults to True.
        echo_traceback (bool, optional): Whether to print the traceback to the console.
        Defaults to False.
        kill_if_fatal_error (bool, optional): If True, program exits
            if the error is considered critical.
            Defaults to False.
        echo_color (typer.colors, optional): The color for console output.
            Defaults to typer.colors.RED.

    Returns:
        None
    """
    logger = get_logger()
    traceback_str = traceback.format_exc()

    if echo_msg:
        typer.secho(custom_message, fg=echo_color)

    if echo_traceback:
        typer.echo(traceback_str)

    logger.error(
        error, extra={"custom_message": custom_message, "traceback": traceback_str}
    )

    if kill_if_fatal_error:
        raise SystemExit(custom_message)


def catch_and_log_info(
    custom_message: str = "log info",
    echo_msg=False,
    log_info_message=True,
    echo_color=typer.colors.GREEN,
):
    """
    Setup logger and log an information message.

    This function creates a logger and logs an information message.

    Args:
        custom_message (str, optional): The information message to be logged.
            Defaults to "log info".
        echo_msg (bool, optional): Whether to print the information message to the console.
            Defaults to False.
        log_info_message (bool, optional): Whether to store the information message in the
            log file. Defaults to True.
        echo_color (typer.colors, optional): The color for console output.
            Defaults to typer.colors.GREEN.

    Returns:
        None
    """
    logger = get_logger(log_level=logging.INFO)
    if echo_msg:
        typer.secho(custom_message, fg=echo_color)
    if log_info_message:
        logger.info(custom_message)


if __name__ == "__main__":
    pass
