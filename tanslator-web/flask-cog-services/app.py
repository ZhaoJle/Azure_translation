from flask import Flask, render_template, url_for, jsonify, request
from flask_nav import Nav
from flask_nav.elements import *
import translate, sentiment, synthesize

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

nav = Nav()

nav.register_element('top', Navbar(
    View('Home.', 'index'),
    Subgroup(
        'Products',
        View('Wg240-Series', 'products', product='wg240'),
        View('Wg250-Series', 'products', product='wg250'),
        Separator(),
        Text('Discontinued Products'),
        View('Wg10X', 'products', product='wg10x'),
    ),
    Link('Tech Support', 'http://techsupport.invalid/widgits_inc'),
    View('About', 'about')
))

# 3. 初始化 app
nav.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate')
def translate_index():
    return render_template('translate.html')

@app.route('/synthesize')
def synthesize_index():
    return render_template('synthesize.html')

@app.route('/sentiment')
def sentiment_index():
    return render_template('sentiment.html')

@app.route('/translate-text', methods=['POST'])
def translate_text():
    data = request.get_json()
    text_input = data['text']
    translation_output = data['to']
    response = translate.get_translation(text_input, translation_output)
    return jsonify(response)

@app.route('/sentiment-analysis', methods=['POST'])
def sentiment_analysis():
    data = request.get_json()
    input_text = data['inputText']
    input_lang = data['inputLanguage']
    output_text = data['outputText']
    output_lang =  data['outputLanguage']
    response = sentiment.get_sentiment(input_text, input_lang, output_text, output_lang)
    return jsonify(response)

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text_input = data['text']
    voice_font = data['voice']
    tts = synthesize.TextToSpeech(text_input, voice_font)
    tts.get_token()
    audio_response = tts.save_audio()
    return audio_response