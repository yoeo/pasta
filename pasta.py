#!/usr/bin/env python3

import json
import logging.config
from pathlib import Path
import urllib.parse
import urllib.request

from flask import Flask, request
from guesslang import Guess


CONFIG = Path(__file__).parent.joinpath('config')

logging.config.dictConfig(
    json.loads(CONFIG.joinpath('logging.json').read_text()))
LOGGER = logging.getLogger(__name__)

TITLE = "pasted by @{}"
TOKENS = json.loads(CONFIG.joinpath('tokens.json').read_text())
UPLOAD = 'https://slack.com/api/files.upload?{}'
LANGUAGES = {
  'C': 'c',
  'C++': 'cpp',
  'C#': 'csharp',
  'CSS': 'css',
  'Erlang': 'erlang',
  'Go': 'go',
  'HTML': 'html',
  'Java': 'java',
  'Javascript': 'javascript',
  'Markdown': 'markdown',
  'Objective-C': 'objc',
  'PHP': 'php',
  'Perl': 'perl',
  'Python': 'python',
  'Ruby': 'ruby',
  'Rust': 'rust',
  'Scala': 'scala',
  'Shell': 'shell',
  'SQL': 'sql',
  'Swift': 'swift'
}

app = Flask(__name__)
app.config.update({'DEBUG': True, 'SECRET_KEY': TOKENS['flask']})

guess = Guess()


def main():
    app.run()


@app.route('/', methods=['GET', 'POST'])
def index():
    return _process(dict(request.form))


def _process(data):
    tokens = data.get('token', [])
    if not any(token in TOKENS['slash-cmd'] for token in tokens):
        LOGGER.error("Unauthorized")
        return 'Unauthorized!'

    content = ''.join(data['text'])
    fileinfo = {
        'token': TOKENS['bot-user'],
        'content': content,
        'filetype': LANGUAGES[guess.language_name(content)],
        'title': TITLE.format(data['user_name'][0]),
        'channels': data['channel_id'][0]
    }

    url = UPLOAD.format(urllib.parse.urlencode(fileinfo))
    with urllib.request.urlopen(url) as response:
        payload = json.loads(response.read().decode())
        if not payload['ok']:
            LOGGER.error("File upload failed: %s", payload)
            return 'Cannot /paste on private channels'

    LOGGER.info("File uploaded")
    return ''  # OK


if __name__ == '__main__':
    main()
