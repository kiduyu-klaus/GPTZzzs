import gptzzzs

# Initialize GPTZzzs
thing = gptzzzs.Gptzzzs()

# Your text to humanize
text = """
Artificial intelligence has revolutionized the field of natural language processing. 
Machine learning models can now generate coherent and contextually appropriate text 
with remarkable accuracy. These advancements have significant implications for various 
industries and applications.
"""

print("=" * 80)
print("ORIGINAL TEXT:")
print("=" * 80)
print(text)
print()

# Example 1: Basic synonym replacement only
print("=" * 80)
print("METHOD 1: Basic Synonym Replacement")
print("=" * 80)
result1 = thing.basic_change_text(text, percent_synonyms=50)
print(result1)
print()

# Example 2: AI humanization only (requires Ollama running)
print("=" * 80)
print("METHOD 2: AI Humanization Only")
print("=" * 80)
try:
    result2 = thing.humanize_with_ai(text, temperature=0.7)
    print(result2)
except Exception as e:
    print(f"Error: {e}")
    print("Make sure Ollama is running with: ollama serve")
    print("And you have a model installed: ollama pull llama2")
print()

# Example 3: Combined approach (best results)
print("=" * 80)
print("METHOD 3: Combined Synonym + AI Humanization")
print("=" * 80)
try:
    result3 = thing.combined_humanize(
        text,
        use_synonyms=True,
        use_ai=True,
        percent_synonyms=40,  # Lower percentage for synonym changes
        temperature=0.8       # Higher temperature for more variation
    )
    print(result3)
except Exception as e:
    print(f"Error: {e}")
print()

# Example 4: Streaming output with callback
print("=" * 80)
print("METHOD 4: Streaming AI Humanization")
print("=" * 80)
try:
    def print_chunk(chunk):
        print(chunk, end='', flush=True)
    
    result4 = thing.humanize_with_ai(
        text,
        streaming=True,
        callback=print_chunk,
        temperature=0.7
    )
    print("\n")
except Exception as e:
    print(f"Error: {e}")
print()

# Example 5: Configure custom Ollama settings
print("=" * 80)
print("METHOD 5: Custom Ollama Model (e.g., mistral, codellama)")
print("=" * 80)
try:
    # Set custom model (make sure you have it installed)
    thing.set_ollama_config(model="mistral")
    
    result5 = thing.humanize_with_ai(text)
    print(result5)
except Exception as e:
    print(f"Error: {e}")
    print("Install the model with: ollama pull mistral")
print()

# Example 6: Using a custom Ollama URL (if running on different port/host)
print("=" * 80)
print("METHOD 6: Custom Ollama URL")
print("=" * 80)
try:
    thing.set_ollama_config(url="http://localhost:11434", model="llama2")
    
    result6 = thing.humanize_with_ai(text)
    print(result6)
except Exception as e:
    print(f"Error: {e}")
print()

print("=" * 80)
print("TIPS:")
print("=" * 80)
print("1. Install Ollama from: https://ollama.ai")
print("2. Start Ollama: ollama serve")
print("3. Pull a model: ollama pull llama2")
print("4. Other models: mistral, codellama, gemma, phi, etc.")
print("5. Lower temperature (0.3-0.5) = more conservative changes")
print("6. Higher temperature (0.7-0.9) = more creative changes")
print("7. Combined method works best: synonyms first, then AI")
print("=" * 80)