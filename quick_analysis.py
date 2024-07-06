# Standard
# None

# Pip
# None

# Custom
from adversaries.docs_processor.app_docs_processor import extract_text_from_all_prompts
from adversaries.attacker_evaluator.app_attacker_evaluator import (
    generate_multi_arr,
    generate_excerpts,
)

extract_text_from_all_prompts()  # Create text files from the .docx prompt
generate_multi_arr()  # generate the adversarials and score them
generate_excerpts()  # Generate excerpts from the content burst files

if __name__ == "__main__":
    pass
