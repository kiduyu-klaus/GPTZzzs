from gptzzzs import Gptzzzs

# Initialize
gpt = Gptzzzs()

# Modify a DOCX file
output_file = gpt.modify_docx(
    input_path=r"Clinton New Covenant and Governance Strategy.edited.docx",
    synonym_list="finnlp",
    percent_synonyms=30,
    ignore_quotes=True,
    percent_adjectives=60,
    use_pos_filtering=True
)
output_file1=gpt.modify_docx_from_gptzzzs(
    input_path=r"Clinton New Covenant and Governance Strategy.docx",
    gptzzzs_instance=gpt,
    synonym_list=gpt.synonym_list,
    percent_synonyms=gpt.percent_synonyms,
    ignore_quotes=gpt.ignore_quotes,
    percent_adjectives=gpt.percent_adjectives,
    use_pos_filtering=False )
print(f"Modified document saved to: {output_file1}")
# Output: Modified document saved to: assignment1_edited.docx