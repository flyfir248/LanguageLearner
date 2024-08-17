from flask import Flask, render_template, request, jsonify, send_file
from gtts import gTTS
import os
import tempfile
import random

app = Flask(__name__)

# Kannada words dataset (unchanged)
kannada_words = [
    {"kannada": "ನಮಸ್ಕಾರ", "transliteration": "namaskāra", "english": "Hello"},
    {"kannada": "ಹೋಗಿಬರುತ್ತೇನೆ", "transliteration": "hōgubaruttēne", "english": "goodbye (\"I'll go and come back\")"},
    {"kannada": "ನಾನು…", "transliteration": "Nānu…", "english": "I am…"},
    {"kannada": "ನನ್ನ ಹೆಸರು…", "transliteration": "Nanna hesaru…", "english": "My name is…"},
    {"kannada": "ನಿನ್ನ/ನಿಮ್ಮ ಹೆಸರು ಏನು?", "transliteration": "Ninna/Nimma hesaru ēnu?",
     "english": "What is your name (informal/polite)?"},
    {"kannada": "ಹೇಗಿದ್ದೀಯ ನೀನು/ಹೇಗಿದ್ದೀರ ನೀವು?", "transliteration": "Hēgiddiya nīnu/Hēgiddira nivu?",
     "english": "How are you? (informal/polite)"},
    {"kannada": "ನಾನು ಚೆನ್ನಾಗಿದ್ದೀನಿ.", "transliteration": "Nānu cennāgiddini.", "english": "I'm fine."},
    {"kannada": "ಧನ್ಯವಾದ(ಗಳು).", "transliteration": "Dhanyavāda(gaḷu).", "english": "Thank you."},
    {"kannada": "ಎಲ್ಲ ಸರಿಯಾಗಿದ್ದಿಯಾ?", "transliteration": "Ellā sariyāgiddiyā?",
     "english": "(Is) everything well/alright?"},
    {"kannada": "ಎಲ್ಲ ಸರಿಯಗಿದ್ದೆ.", "transliteration": "Ellā sariyagidde.", "english": "Everything's fine."},
    {"kannada": "ಏನು ಸಮಾಚಾರ?", "transliteration": "Ēnu samācāra?", "english": "What's the latest/What's up?"},
    {"kannada": "ಏನು ಇಲ್ಲ.", "transliteration": "Ēnu illa.", "english": "Not much."},
    {"kannada": "ನಾನು (ತುಂಬ) ಸಂತೋಷವಾಗಿದ್ದೇನೆ ನಿನ್ನ/ನಿಮ್ಮ ಭೇಟಿ ಮಡಿದ್ದಿಂದ.",
     "transliteration": "Nānu (tuṃba) santōṣavāgiddēne ninna/nimma bhēṭi maḍiddinda.",
     "english": "I'm (very) pleased to meet you. (informal/polite)"}
]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get_word')
def get_word():
    word = random.choice(kannada_words)
    return jsonify(word)


@app.route('/check', methods=['POST'])
def check_answer():
    data = request.json
    user_answer = data['answer'].lower()
    correct_answer = data['english'].lower()

    if user_answer == correct_answer:
        result = "correct"
    else:
        result = "incorrect"

    return jsonify({'result': result, 'correct_answer': correct_answer})


@app.route('/audio')
def audio():
    text = request.args.get('text', '')
    tts = gTTS(text=text, lang='kn')

    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        tts.save(fp.name)
        fp.seek(0)
        return send_file(fp.name, mimetype='audio/mpeg')


if __name__ == '__main__':
    app.run(debug=True)