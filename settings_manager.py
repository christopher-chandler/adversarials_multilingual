# Standard
import os

# Pip
import yaml

# Custom
# None


def get_config_data(file: str = None) -> dict:
    """
    Reads configuration data from a YAML file and returns it as
    a Python data structure.

    Args:
    file (str): The file path to the YAML configuration file.
        If not specified, the default configuration file 'config.yaml'
        in the script's directory will be used.

    Returns:
        config_data (dict): A Python dictionary containing the configuration data.
    """
    if file is None:
        # The directory where the script is located
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # The path to the YAML configuration file relative to the script's directory
        file = os.path.join(script_directory, "setting_files/settings.yaml")

    # Load the YAML configuration file
    with open(file, "r") as config_file:
        config_data: dict = yaml.safe_load(config_file)

    return config_data


if __name__ == "__main__":
    pass
