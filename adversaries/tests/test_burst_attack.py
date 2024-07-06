# Standard
import os
import time

# Pip
from typer.testing import CliRunner

# Custom
from adversaries.burst_attack.app_burst_attack import app_burst_attack

# Set up runner
runner = CliRunner()


def test_burst_attack_generate_burst():
    result = runner.invoke(app_burst_attack)
    print(result.stdout)
    assert result.exit_code == 0


if __name__ == "__main__":
    pass
