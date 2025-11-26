"""
Example usage showing the difference between basic and contextual text change
"""

import gptzzzs

# Initialize GPTZzzs
gpt = gptzzzs.Gptzzzs()

# Sample text to test
sample_text = """
The bank manager decided to walk along the river bank during his lunch break. 
He saw a beautiful bird perched on a branch. The weather was very nice and the 
scenery was really peaceful. He thought about how the financial bank he worked 
at was very different from this natural setting.
"""

"""
The bank manager decided to walking along the river bank during his dejeuner burst. 
He saw a extremely beautiful fowl perched on a branch. The weather was incredibly real skillful and the scene was peaceful. 
He thought about how the financial camber he worked at was real so different from this quite instinctive background."""

print("=" * 80)
print("ORIGINAL TEXT:")
print("=" * 80)
print(sample_text)

print("\n" + "=" * 80)
print("BASIC CHANGE (without context awareness):")
print("=" * 80)
basic_result = gpt.basic_change_text(
    sample_text,
    synonym_list="finnlp",
    percent_synonyms=50,
    ignore_quotes=True,
    percent_adjectives=60
)
print(basic_result)
gpts = gptzzzs.Gptzzzs()


print("\n" + "=" * 80)
print("CONTEXTUAL CHANGE (with POS tagging and context awareness):")
print("=" * 80)
contextual_result = gpt.contextual_change_text(
    sample_text,
    synonym_list="finnlp",
    percent_synonyms=50,
    ignore_quotes=True,
    percent_adjectives=60,
    use_pos_filtering=True
)
print(contextual_result)

print("\n" + "=" * 80)
print("COMPARISON NOTES:")
print("=" * 80)
print("""
The contextual version:
1. Respects part-of-speech (won't replace verb 'bank' with noun synonyms)
2. Skips proper nouns and acronyms automatically
3. Ranks synonyms by contextual similarity
4. Better handles punctuation
5. More natural output with better word choices
""")

# Another example showing the improvement
technical_text = """
The function returns a list of values. The company will return the investment 
next quarter. Please return this book to the library.
"""

print("\n" + "=" * 80)
print("TECHNICAL TEXT EXAMPLE:")
print("=" * 80)
print("Original:", technical_text)
print("\nContextual:", gpt.contextual_change_text(technical_text, percent_synonyms=40))
