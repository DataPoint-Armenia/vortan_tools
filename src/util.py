import codecs
import epub
from typing import Any

def get_text_from_txt_file(filename: str) -> str:
    try:
        f = codecs.open(filename, encoding='utf-8')
        f.seek(0)
        text = f.read()
        f.close()
    except (UnicodeDecodeError, OSError, IOError) as e:
        pass
    return text


def get_text_from_epub_file(filename: str) -> str:
    book = epub.open_epub(filename)
    for item in book.opf.manifest.values():
        try:
            text = book.read_item(item)
        except KeyError as k:
            continue
        try:
            text = text.decode('utf-8')
        except UnicodeDecodeError as u:
            pass
    book.close()
    return text

# Expects an nltk.FreqDist
def write_ngram_freq_to_file(freq_dist: Any, filename: str, sort: bool = False):
    grams = sorted(freq_dist.items(), key = lambda x: x[1], reverse = True) if sorted else freq_dist.items()
    with open(filename, 'w+') as f:
        f.writelines(f"{' '.join(k)} {v}\n" for k, v in grams)
    print(f"Wrote to {filename}")
