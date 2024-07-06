# Standard
import os
import platform

# Pip
import pytesseract
import typer

from pytesseract.pytesseract import TesseractNotFoundError

# Custom
from adversaries.settings.constants.constant_vars import TEST_TESSERACT_IMG
from adversaries.settings.constants.constant_paths import GeneralPaths as Gp


operating_system = platform.system()

if operating_system == "Windows":
    # This is only relevant if you have a Windows machine
    # Mac and Linux automatically install to path.
    pytesseract.pytesseract.tesseract_cmd = (
        "C://Program Files/Tesseract-OCR/tesseract.exe"
    )


def is_tesseract_installed() -> None:
    """
    Checks if Tesseract OCR is installed on the system.
    If not installed, provides instructions for installation based on the operating system.

    Raises:
        SystemExit: If Tesseract OCR is not installed.
    """
    try:

        pytesseract.image_to_string(f"{os.getcwd()}/{TEST_TESSERACT_IMG}")
    except TesseractNotFoundError as error:
        typer.echo(error)

        # Detect the operating system
        if operating_system == "Darwin":  # Mac
            mac_error = """
            To install Tesseract OCR on a Mac using Homebrew, follow these steps:

            1. Open your terminal application.
            2. Ensure you have Homebrew installed. If not, you can install it by running:
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            3. Once Homebrew is installed, you can install Tesseract by running:
                brew install tesseract
            4. Wait for the installation to complete. Homebrew will automatically handle dependencies.
            5. After the installation is finished, you can verify Tesseract is installed by running:
                tesseract --version
            6. This command should output the version number of Tesseract installed on your system.

            Now you have successfully installed Tesseract OCR on your Mac using Homebrew.
            """

            typer.echo(mac_error)

        elif operating_system == "Windows":
            windows_error = """
            To accomplish OCR with Python on Windows, you will need Python and OpenCV (which you already have), as well as Tesseract and the Pytesseract Python package.

            To install Tesseract OCR for Windows:
            1. Download tesseract exe from https://github.com/UB-Mannheim/tesseract/wiki.
            2. Run the installer (find 2021) from UB Mannheim.
            3. Configure your installation (choose installation path and language data to include).
            4. Add Tesseract OCR to your environment variables.

            To install and use Pytesseract on Windows:

            Simply run: 
                pip install pytesseract

            You will also need to install Pillow with: 
                pip install Pillow 

            Import it in your Python document like so: 
                from PIL import Image

            To be able to call pytesseract on your machine, add the following line in your code: 
                pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
            """

            typer.echo(windows_error)
        else:
            unknown_error = "Unsupported operating system."
            typer.echo(unknown_error)

        raise SystemExit


if __name__ == "__main__":
    is_tesseract_installed()
