"""
Telugu-English Translation Model
"""

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class TeluguEnglishTranslator:
    def __init__(self, model_name="Helsinki-NLP/opus-mt-te-en"):
        """
        Initialize the translator with a pre-trained model
        """
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
    def load_model(self):
        """Load the translation model and tokenizer"""
        try:
            print(f"Loading model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            self.model.to(self.device)
            print("Model loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def translate(self, text, source_lang="te", target_lang="en", max_length=512):
        """
        Translate text from source language to target language
        """
        if not self.model or not self.tokenizer:
            if not self.load_model():
                return "Error: Could not load translation model"
        
        try:
            # Prepare input
            input_text = text
                
            # Tokenize
            inputs = self.tokenizer(input_text, return_tensors="pt", 
                                  padding=True, truncation=True, max_length=max_length)
            inputs = inputs.to(self.device)
            
            # Generate translation
            with torch.no_grad():
                outputs = self.model.generate(**inputs, max_length=max_length, 
                                            num_beams=4, early_stopping=True)
            
            # Decode output
            translation = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return translation
            
        except Exception as e:
            return f"Translation error: {str(e)}"

# Example usage
if __name__ == "__main__":
    translator = TeluguEnglishTranslator()
    
    # Test translation
    telugu_text = "నమస్కారం, మీరు ఎలా ఉన్నారు?"
    print(f"Telugu: {telugu_text}")
    
    english_translation = translator.translate(telugu_text)
    print(f"English: {english_translation}")