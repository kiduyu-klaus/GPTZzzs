from gptzzzs import Gptzzzs
import os

# Initialize
gpt = Gptzzzs()

# --- Example of modifying a DOCX file ---
# This script should be run from the root of the project directory.
# Make sure the input file exists.

input_filename = r"Clinton New Covenant and Governance Strategy.docx" # Replace with your DOCX file


# Modify a DOCX file
output_file = gpt.modify_docx_from_gptzzzs(
    input_path=input_filename,
    synonym_list="finnlp",
    percent_synonyms=30,
    ignore_quotes=True,
    percent_adjectives=60,
    use_pos_filtering=False
)

print(f"\nSuccessfully modified document. Output saved to: {output_file}")