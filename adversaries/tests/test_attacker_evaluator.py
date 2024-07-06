# Standard
# None

# Pip
from typer.testing import CliRunner

# Custom

from adversaries.attacker_evaluator.app_attacker_evaluator import app_attack_evaluator

# Set up runner
runner = CliRunner()


def test_attack_evaluator_singular():
    result = runner.invoke(app_attack_evaluator, ["singular"])
    print(result.stdout)
    assert result.exit_code == 0


def test_attack_evaluator_multiple():

    result = runner.invoke(app_attack_evaluator, ["multiple"])
    print(result.stdout)
    assert result.exit_code == 0


def test_attack_evaluator_visualize():
    result = runner.invoke(app_attack_evaluator, ["visualize"])
    print(result.stdout)
    assert result.exit_code == 0


def test_attack_evaluator_generate_excerpts():
    result = runner.invoke(app_attack_evaluator, ["generate_excerpts"])

    print(result.stdout)
    assert result.exit_code == 0


if __name__ == "__main__":
    pass
