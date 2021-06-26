import codecs
import epub
from typing import Any, List, Tuple
from nltk import FreqDist
from nltk.util import ngrams
import io, sys

sys.path.insert(0, './extern/vortan_tokenizer/')
from tokenizer import VortanTokenizer


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


def tokenize_sentence(text: str) -> List[str]:
    words = []
    T = VortanTokenizer(text)
    T.segmentation().tokenization()
    for s in T.segments:
        sentence = []
        for index, t in enumerate(s['tokens']):
            w = t[1] if index != 0 else t[1].lower()
            sentence.append(w)
        return sentence # just first sentence


# Expects each row in file to be a single sentence
def get_words_from_sentences(
    filename: str,
    make_first_word_lowercase: bool = True,
) -> List[List[str]]:
    sentences = []
    try:
        f = codecs.open(filename, encoding='utf-8')
        f.seek(0)
        for line in f:
            sentence = line.strip()
            if make_first_word_lowercase:
                sentence = sentence[0].lower() + sentence[1:]
            words = tokenize_sentence(sentence)
            if words is not None and len(words):
                sentences.append(words)
        f.close()
    except (UnicodeDecodeError, OSError, IOError) as e:
        pass
    return sentences


def extract_ngrams(all_sentences: List[List[str]]) -> Tuple[Any, Any]:
    unigram_freqs = FreqDist()
    bigram_freqs = FreqDist()
    for sentence in all_sentences:
        unigram_freqs.update(ngrams(sentence, 1))
        bigram_freqs.update(ngrams(sentence, 2))
    return unigram_freqs, bigram_freqs


# Expects an nltk.FreqDist
def write_ngram_freq_to_file(freq_dist: Any, filename: str, sort: bool = False):
    grams = sorted(freq_dist.items(
    ), key=lambda x: x[1], reverse=True) if sorted else freq_dist.items()
    with io.open(filename, 'w+', encoding="utf-8") as f:
        f.writelines(f"{' '.join(k)} {v}\n" for k, v in grams)
    print(f"Wrote to {filename}")
