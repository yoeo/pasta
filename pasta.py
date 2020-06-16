#!/usr/bin/env python3

import json
import logging.config
import os
from pathlib import Path
import urllib.parse
import urllib.request

from flask import Flask, request
from guesslang import Guess


def update_with_env(config):
    for name in config:
        env_name = 'PASTA_{}'.format(name.replace('-', '_').upper())
        if env_name in os.environ:
            config[name] = os.environ[env_name]


CONFIGDIR = Path(__file__).parent.joinpath('config')

# Logging
logging.config.dictConfig(
    json.loads(CONFIGDIR.joinpath('logging.json').read_text()))
LOGGER = logging.getLogger(__name__)

# Configuration
CONFIG = json.loads(CONFIGDIR.joinpath('config.json').read_text())
update_with_env(CONFIG)  # Bypass config file with environment variables

# Comunication data
TITLE = "pasted by @{}"
UPLOAD = 'https://slack.com/api/files.upload?{}'
REQUIRED_FIELDS = ['token', 'text', 'user_name', 'channel_id']
LANGUAGES = json.loads(CONFIGDIR.joinpath('languages.json').read_text())

# Application
app = Flask(__name__)
app.config.update({'DEBUG': int(CONFIG['debug'])})

guess = Guess()


def main():
    app.run()


@app.route('/', methods=['GET', 'POST'])
def index():
    return _process(dict(request.form))


def _process(data):
    if not all(field in data for field in REQUIRED_FIELDS):
        LOGGER.error("Required data missing")
        return "Required data missing"

    if not CONFIG['client-id'] in data.get('token', []):
        LOGGER.error("Unauthorized")
        return "Unauthorized!"

    content = ''.join(data['text'])
    language_name = guess.language_name(content)
    filetype = LANGUAGES.get(language_name)
    if not filetype:
        return "Unsupported file format"

    fileinfo = {
        'token': CONFIG['bot-token'],
        'content': content,
        'filetype': filetype,
        'title': TITLE.format(data['user_name'][0]),
        'channels': data['channel_id'][0]
    }

    url = UPLOAD.format(urllib.parse.urlencode(fileinfo))
    with urllib.request.urlopen(url) as response:
        payload = json.loads(response.read().decode())
        if not payload['ok']:
            LOGGER.error("File upload failed: %s", payload)
            return (
                "/paste don't work in private channels :-(\n"
                "Help us add this feature at https://github.com/yoeo/pasta"
            )

    LOGGER.info("File uploaded")
    return ""  # OK


if __name__ == '__main__':
    main()
