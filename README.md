# vortan_tools
## About

Tools around the vortan project.

## Documentation

- **Google Drive Folder**: [link](https://drive.google.com/drive/folders/1f1feyB_po6hS7TFvdvPWZ3Q6dSEDjklQ)
- **Slack Channel**: [#vortan](https://datapointarmenia.slack.com/archives/C01LE2ADLFJ)

## Prereqs

- [python](https://www.python.org/downloads/)
- [pip](https://pypi.org/project/pip/)

## Installation

1. Clone the repo
```
git clone --recursive https://github.com/DataPoint-Armenia/vortan_tools.git
```
2. Install requirements
```
pip3 install -r requirements.txt --user
```

## Usage

### N-Grams

Generate n-gram frequency files:
```
python3 src/gramify.py data txt
less out/uni_freq.txt
less out/bi_freq.txt
```

### Tokenizer

Wrapper around Armtreebank/Tokenizer

```
python3 src/tokenizer.py
```

### Parser

Wrapper around Armtreebank/End-to-end-Parser

```
pip3 install -r extern/End-to-end-Parser/requirements.txt --user
python3 src/parser.py
```

Currently fails with this error:
```
Traceback (most recent call last):
  File "src/parser.py", line 15, in <module>
    res = model.predict_raw(input_text=filename)
  File "./extern/End-to-end-Parser/predict.py", line 102, in predict_raw
    raise ValueError("Couldn't tokenize the text")
ValueError: Couldn't tokenize the text
```

## Testing

Static type check your code:
```
python3 -m mypy src/gramify.py
```

## Contributors

- [@sourencho](https://github.com/sourencho)

## Acknowledgements

- https://github.com/Armtreebank/Tokenizer
- https://github.com/Armtreebank/End-to-end-Parser

