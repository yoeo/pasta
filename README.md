# Pasta

Pretty-paste source code on Slack

![Webguesslang](data/icon.png)

## /paste source code

**Pasta** is a Slack `/command` that allow you to past source code
directly on channels. The source code is converted into a file and its
[programming language is automatically detected](https://github.com/yoeo/guesslang).

#### Preview

<a href="http://guesslang.readthedocs.io/en/latest/_static/videos/pasta.webm">
  <img src="data/pasta.png" alt="Pasta preview_"/>
</a>

## Install & Run

* Python 3.5+ required

* Create your Slack app https://api.slack.com/

* Fill [config/tokens.json](config/tokens.json) with your Slack app tokens

* Install **Pasta** on your server:

```bash
python3 setup.py install
```

* Run **Pasta**:

```bash
pasta-gunicorn
```

## License and stuff...

* [Language detection powered by Guesslang](https://github.com/yoeo/guesslang)

* [Guesslang documentation](https://guesslang.readthedocs.io/en/latest/)

* Icon created by
  [Demograph™ (Creative Commons)](https://thenounproject.com/term/spaghetti/187779/)

* Pasta — Copyright (c) 2017 Y. SOMDA, [MIT License](LICENSE)
