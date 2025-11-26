from gptzzzs.docx_processor import process_docx, batch_process_docx, process_docx_with_progress
import os

# ============================================================================
# Example 1: Process a single docx file
# ============================================================================
print("=" * 80)
print("EXAMPLE 1: Process Single DOCX File")
print("=" * 80)

input_file = "testDoc.docx"  # Replace with your file path

try:
    output_file = process_docx(
        input_path=input_file,
        ollama_model="gpt-oss:120b-cloud",          # or "mistral", "codellama", etc.
        temperature=0.7,                 # 0.0 = conservative, 1.0 = creative
        max_tokens=2000,
        preserve_formatting=True         # Keep bold, italic, fonts, etc.
    )
    print(f"\nSuccess! Edited file saved as: {output_file}")
except Exception as e:
    print(f"Error: {e}")

print("\n")

# ============================================================================
# Example 2: Process with different temperature settings
# ============================================================================
print("=" * 80)
print("EXAMPLE 2: Different Temperature Settings")
print("=" * 80)



# Lower temperature = more conservative changes (closer to original)
try:
    output_file = process_docx(
        input_path=input_file,
        temperature=0.3,  # Very conservative
        preserve_formatting=True
    )
    print(f"Conservative edit saved as: {output_file}")
except Exception as e:
    print(f"Error: {e}")

print("\n")

# ============================================================================
# Example 3: Batch process multiple files in a directory
# ============================================================================
print("=" * 80)
print("EXAMPLE 3: Batch Process Multiple Files")
print("=" * 80)

# directory = "./documents"  # Replace with your directory path

# try:
#     output_files = batch_process_docx(
#         directory=directory,
#         file_pattern="*.docx",      # Process all .docx files
#         ollama_model="gpt-oss:120b-cloud",
#         temperature=0.7,
#         preserve_formatting=True
#     )
    
#     print("\nProcessed files:")
#     for file in output_files:
#         print(f"  - {file}")
        
# except Exception as e:
#     print(f"Error: {e}")

# print("\n")

# ============================================================================
# Example 4: Process with progress callback
# ============================================================================
print("=" * 80)
print("EXAMPLE 4: Process with Progress Tracking")
print("=" * 80)



def progress_callback(current, total, message):
    """Callback function to track progress"""
    percentage = (current / total * 100) if total > 0 else 0
    print(f"[{percentage:.1f}%] {message}")

try:
    output_file = process_docx_with_progress(
        input_path=input_file,
        ollama_model="gpt-oss:120b-cloud",
        temperature=0.7,
        preserve_formatting=True,
        progress_callback=progress_callback
    )
    print(f"\nCompleted! File saved as: {output_file}")
except Exception as e:
    print(f"Error: {e}")

print("\n")

# ============================================================================
# Example 5: Process without preserving formatting (faster)
# ============================================================================
print("=" * 80)
print("EXAMPLE 5: Fast Processing (No Formatting Preservation)")
print("=" * 80)

input_file = "notes.docx"

try:
    output_file = process_docx(
        input_path=input_file,
        temperature=0.8,
        preserve_formatting=False  # Faster but loses formatting
    )
    print(f"Quick edit saved as: {output_file}")
except Exception as e:
    print(f"Error: {e}")

print("\n")

# ============================================================================
# Example 6: Using different Ollama models
# ============================================================================
print("=" * 80)
print("EXAMPLE 6: Using Different Ollama Models")
print("=" * 80)



# Using Mistral (better at following instructions)
try:
    output_file = process_docx(
        input_path=input_file,
        ollama_model="gpt-oss:120b-cloud",  # Make sure you have: ollama pull mistral
        temperature=0.6,
        preserve_formatting=True
    )
    print(f"Mistral edit saved as: {output_file}")
except Exception as e:
    print(f"Error: {e}")

print("\n")

# ============================================================================
# Example 7: Complete workflow with error handling
# ============================================================================
print("=" * 80)
print("EXAMPLE 7: Complete Workflow with Error Handling")
print("=" * 80)

def process_document_safe(file_path):
    """Safely process a document with comprehensive error handling"""
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return None
    
    # Check if it's a docx file
    if not file_path.endswith('.docx'):
        print(f"❌ Not a .docx file: {file_path}")
        return None
    
    # Check if already edited
    if file_path.endswith('_edited.docx'):
        print(f"⚠️  File appears to be already edited: {file_path}")
        response = input("Process anyway? (y/n): ")
        if response.lower() != 'y':
            return None
    
    print(f"📄 Processing: {file_path}")
    
    try:
        output_file = process_docx(
            input_path=file_path,
            ollama_model="gpt-oss:120b-cloud",
            temperature=0.7,
            preserve_formatting=True
        )
        print(f"✅ Success! Output: {output_file}")
        return output_file
        
    except FileNotFoundError as e:
        print(f"❌ File error: {e}")
    except ValueError as e:
        print(f"❌ Invalid input: {e}")
    except ConnectionError as e:
        print(f"❌ Ollama connection error: {e}")
        print("💡 Make sure Ollama is running: ollama serve")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    return None

# Use the safe function
result = process_document_safe(input_file)

print("\n")

# ============================================================================
# TIPS AND BEST PRACTICES
# ============================================================================
print("=" * 80)
print("TIPS AND BEST PRACTICES")
print("=" * 80)
print("""
1. INSTALLATION:
   pip install python-docx requests

2. OLLAMA SETUP:
   - Install: https://ollama.ai
   - Start server: ollama serve
   - Pull model: ollama pull llama2
   
3. MODEL RECOMMENDATIONS:
   - llama2: Good all-around choice
   - mistral: Better at following instructions
   - phi: Fast but less capable
   - codellama: Good for technical documents
   
4. TEMPERATURE GUIDE:
   - 0.3-0.4: Very conservative, minimal changes
   - 0.5-0.7: Balanced (recommended)
   - 0.8-0.9: More creative/varied changes
   
5. FORMATTING:
   - preserve_formatting=True: Keeps bold, italic, fonts, etc. (slower)
   - preserve_formatting=False: Faster but loses formatting
   
6. PERFORMANCE:
   - Processing time depends on document length
   - Expect ~5-10 seconds per paragraph
   - Use batch processing for multiple files
   
7. QUALITY CHECK:
   - Always review the edited document
   - AI may occasionally change meaning
   - Keep original files as backup
   
8. TROUBLESHOOTING:
   - "Connection refused": Start Ollama with 'ollama serve'
   - "Model not found": Pull model with 'ollama pull <model>'
   - "Timeout": Increase max_tokens or try shorter paragraphs
""")
print("=" * 80)