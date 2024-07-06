# Standard
import os
import time

# Pip
# None

# Custom
from main import main_app, empty_chosen_directory

print("Empty chosen directories")
open("log/log.log", mode="w+", encoding="utf-8").write("Hello world")

print(os.path.exists("log/log.log"))
time.sleep(1)

empty_chosen_directory(trg_dir="log", file_type="log")
print(os.path.exists("log/log.log"))


main_app()


if __name__ == "__main__":
    pass
