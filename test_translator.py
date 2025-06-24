# test_translator.py - Place this in the root directory
"""
Debug script to test the Telugu translator
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("Python path:", sys.path)
print("Current directory:", os.getcwd())
print("Files in src/translator:", os.listdir('src/translator') if os.path.exists('src/translator') else "Directory not found")

try:
    from translator.model import TeluguEnglishTranslator
    print("✅ Successfully imported TeluguEnglishTranslator")
    
    # Test the translator
    translator = TeluguEnglishTranslator()
    print("✅ Created translator instance")
    
    print("Loading model... (this may take a few minutes)")
    translator.load_model()
    print("✅ Model loaded successfully")
    
    # Test translation
    test_text = "నమస్కారం"  # Hello in Telugu
    translation = translator.translate(test_text)
    print(f"✅ Translation test:")
    print(f"   Telugu: {test_text}")
    print(f"   English: {translation}")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Let's debug this...")
    
    # Check if files exist
    model_file = os.path.join('src', 'translator', 'model.py')
    print(f"model.py exists: {os.path.exists(model_file)}")
    
    if os.path.exists(model_file):
        with open(model_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'class TeluguEnglishTranslator' in content:
                print("✅ TeluguEnglishTranslator class found in file")
            else:
                print("❌ TeluguEnglishTranslator class NOT found in file")
                
except Exception as e:
    print(f"❌ Other Error: {e}")
    import traceback
    traceback.print_exc()