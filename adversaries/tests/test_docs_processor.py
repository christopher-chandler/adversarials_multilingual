# Standard
import os
import time

# Pip
from typer.testing import CliRunner

# Custom
from adversaries.docs_processor.app_docs_processor import app_docs_processor

# Set up runner
runner = CliRunner()


def test_docs_processor_extract_prompt_text():
    result = runner.invoke(app_docs_processor)
    print(result.stdout)
    assert result.exit_code == 0


if __name__ == "__main__":
    pass
