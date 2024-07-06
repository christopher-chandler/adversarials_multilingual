# Standard
import datetime

# Pip
# None

# Custom
from settings_manager import get_config_data

"""
Hier sind Konstanten, die von anderen Funktionen verwendet werden. 
"""
CONTENT_BURST_SEED = get_config_data().get("CONTENT_BURST_SEED")
TEST_TESSERACT_IMG = get_config_data().get("TEST_TESSERACT_IMG")
current_datetime = datetime.datetime.now()
TIMESTAMP = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")
SIMPLE_TIMESTAMP = current_datetime.strftime("%Y_%m_%d")


if __name__ == "__main__":
    pass
