"""
Flask API for Telugu-English Translation
"""

from flask import Flask, request, jsonify, render_template_string
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from translator.model import TeluguEnglishTranslator

app = Flask(__name__)

# Initialize translator globally
translator = TeluguEnglishTranslator()

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Telugu-English Translator</title>
        <style>
            body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
            .container { background: #f5f5f5; padding: 20px; border-radius: 10px; }
            textarea { width: 100%; height: 100px; margin: 10px 0; padding: 10px; }
            button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .result { background: white; padding: 15px; margin: 20px 0; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Telugu ⇄ English Translator</h1>
            <form id="translateForm">
                <div>
                    <label>Enter Telugu Text:</label>
                    <textarea id="inputText" placeholder="నమస్కారం, మీరు ఎలా ఉన్నారు?"></textarea>
                </div>
                <button type="submit">Translate to English</button>
            </form>
            <div id="result" class="result" style="display:none;">
                <h3>Translation:</h3>
                <p id="translationText"></p>
            </div>
        </div>
        
        <script>
            document.getElementById('translateForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const text = document.getElementById('inputText').value;
                const response = await fetch('/translate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: text})
                });
                const result = await response.json();
                document.getElementById('translationText').textContent = result.translation;
                document.getElementById('result').style.display = 'block';
            });
        </script>
    </body>
    </html>
    """)

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Load model if not already loaded
        if not translator.model:
            translator.load_model()
        
        translation = translator.translate(text)
        
        return jsonify({
            'original': text,
            'translation': translation,
            'source_lang': 'te',
            'target_lang': 'en'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Telugu-English Translator API...")
    app.run(debug=True, host='0.0.0.0', port=5000)