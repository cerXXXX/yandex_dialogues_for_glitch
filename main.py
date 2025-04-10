from flask import Flask, request, jsonify
import logging
from googletrans import Translator

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s %(levelname)s %(name)s %(message)s')

translator = Translator()


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Response: %r', response)
    return jsonify(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = 'Привет! Скажи, какое слово ты хочешь перевести.'
        return

    user_input = req['request']['nlu']['tokens']
    word_to_translate = get_word(user_input)

    if word_to_translate:
        translated_word = translate_word(word_to_translate)
        res['response']['text'] = f'{word_to_translate} на английском будет {translated_word}.'
    else:
        res['response']['text'] = 'Не расслышал слово для перевода. Повтори, пожалуйста.'


def get_word(tokens):
    for token in tokens:
        if token.isalpha():
            return token
    return None


def translate_word(word):
    try:
        translated = translator.translate(word, src='ru', dest='en')
        return translated.text
    except Exception as e:
        return f'Ошибка перевода: {e}'


if __name__ == '__main__':
    app.run()
