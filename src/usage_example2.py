"""
Advanced usage examples showing sentence structure variation and combined transformations
"""

import gptzzzs

# Initialize GPTZzzs
gpt = gptzzzs.Gptzzzs()

# Sample texts to demonstrate different features
sample_text_1 = """
The research paper was written by the student, and the professor reviewed it carefully. 
The experiment was conducted in the laboratory. The results were very interesting and 
the conclusion was extremely important. The data supports the hypothesis, but more 
research is needed.
"""

sample_text_2 = """
John threw the ball to Mary, and she caught it with ease. The game was played on 
Saturday. The team won the championship. The coach was very proud of the players, 
and the fans were really excited about the victory.
"""

sample_text_3 = """
The company announced new policies. The employees attended the meeting. The changes 
were implemented immediately, and everyone adapted quickly. The manager explained 
the benefits, but some workers had concerns.
"""

print("=" * 80)
print("DEMONSTRATION 1: SENTENCE STRUCTURE VARIATION ONLY")
print("=" * 80)
print("\nOriginal:")
print(sample_text_1)

print("\nStructure Varied (no synonym changes):")
structure_only = gpt.vary_structure_only(
    sample_text_1,
    percent_reorder=50,
    percent_voice_change=30,
    percent_beginning_vary=40
)
print(structure_only)

print("\n" + "=" * 80)
print("DEMONSTRATION 2: ACTIVE/PASSIVE VOICE CONVERSION")
print("=" * 80)
print("\nOriginal:")
print(sample_text_2)

print("\nWith Voice Changes:")
voice_changed = gpt.vary_structure_only(
    sample_text_2,
    percent_reorder=0,
    percent_voice_change=60,  # High percentage for voice changes
    percent_beginning_vary=0
)
print(voice_changed)

print("\n" + "=" * 80)
print("DEMONSTRATION 3: CONTEXTUAL SYNONYMS (Previous Feature)")
print("=" * 80)
print("\nOriginal:")
print(sample_text_3)

print("\nWith Contextual Synonyms:")
contextual = gpt.contextual_change_text(
    sample_text_3,
    percent_synonyms=40
)
print(contextual)

print("\n" + "=" * 80)
print("DEMONSTRATION 4: ADVANCED COMBINED TRANSFORMATION (RECOMMENDED)")
print("=" * 80)
print("\nOriginal:")
print(sample_text_3)

print("\nAdvanced Combined (Synonyms + Structure Variation):")
advanced = gpt.advanced_change_text(
    sample_text_3,
    percent_synonyms=35,
    percent_reorder=40,
    percent_voice_change=25,
    percent_beginning_vary=30
)
print(advanced)

print("\n" + "=" * 80)
print("DEMONSTRATION 5: COMPARISON OF ALL METHODS")
print("=" * 80)

comparison_text = """
The scientist discovered a new species in the rainforest, and the finding was 
published in a prestigious journal. The research was funded by the university.
"""

print("\nOriginal Text:")
print(comparison_text)

print("\n1. Basic Change (old method):")
print(gpt.basic_change_text(comparison_text, percent_synonyms=40))

print("\n2. Contextual Change (with POS tagging):")
print(gpt.contextual_change_text(comparison_text, percent_synonyms=40))

print("\n3. Structure Variation Only:")
print(gpt.vary_structure_only(comparison_text, percent_voice_change=50))

print("\n4. Advanced Combined (BEST QUALITY):")
print(gpt.advanced_change_text(
    comparison_text,
    percent_synonyms=35,
    percent_reorder=40,
    percent_voice_change=30,
    percent_beginning_vary=25
))

print("\n" + "=" * 80)
print("FEATURE SUMMARY")
print("=" * 80)
print("""
Available Methods:

1. basic_change_text() - Original simple synonym replacement
   - Fast but less natural
   - May produce awkward results

2. contextual_change_text() - Context-aware synonyms with POS tagging
   - Better synonym selection
   - Respects grammar and context
   - Recommended over basic_change_text()

3. vary_structure_only() - Sentence structure variation without synonyms
   - Reorders compound sentences
   - Changes active/passive voice
   - Adds transitions and varies beginnings
   - Keeps original vocabulary

4. advanced_change_text() - MOST COMPREHENSIVE (RECOMMENDED)
   - Combines contextual synonyms + structure variation
   - Highest quality output
   - Most natural-sounding results
   - Best for avoiding detection

Tips for Best Results:
- Use advanced_change_text() for comprehensive transformation
- Lower percentages (20-35%) produce more natural results
- Always review and edit the output
- Adjust percentages based on your needs
""")
