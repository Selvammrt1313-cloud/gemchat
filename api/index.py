import os
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Initialize the new Gemini Client
# It automatically reads GEMINI_API_KEY from the terminal environment!
client = genai.Client()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        # Using the brand-new standard syntax for Gemini
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=f"You are a helpful student AI tutor. Answer this question clearly and concisely: {user_message}"
        )
        
        return jsonify({'reply': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Required for Vercel execution
def handler(request):
    return app(request)

if __name__ == '__main__':
    app.run(debug=True)
