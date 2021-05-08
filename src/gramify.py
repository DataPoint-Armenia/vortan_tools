from collections import Counter
import json
import epub
import time
import collections
import operator
import codecs
import unicodedata
import re
import os
import sys
import nltk
from nltk import FreqDist
from nltk.util import ngrams
from typing import List
from typing import Any
from typing import Tuple

from util import get_text_from_txt_file
from util import get_text_from_epub_file
from util import write_ngram_freq_to_file

sys.path.insert(0, './extern/vortan_tokenizer/')
from tokenizer import Tokenizer


def print_progress(i: int, total: int, ext: str) -> None:
    sys.stderr.write('\r')
    sys.stderr.write("Progress: {0:.1f}%".format(
        i/float(total) * 100) + " of '%s'" % ext)
    sys.stderr.flush()


def get_words_from_txt_file(filename: str) -> List[str]:
    return get_words_from_text(get_text_from_txt_file(filename))


def get_words_from_epub_file(filename) -> List[str]:
    return get_words_from_text(get_text_from_epub_file(filename))


def get_words_from_text(text: str) -> List[str]:
    words = []
    T = Tokenizer(text)
    T.segmentation().tokenization()
    for s in T.segments:
        for index, t in enumerate(s['tokens']):
            w = t[1] if index != 0 else t[1].lower()
            words.append(w)
    return words


def process_files(path: str, exts: List[str]) -> Tuple[Any, Any]:
    # Init
    unigram_freqs = FreqDist()
    bigram_freqs = FreqDist()

    # Process files
    for ext in exts:
        # get all .ext file paths recursively
        files = [os.path.join(dirpath, f)
                 for dirpath, dirnames, files in os.walk(path)
                 for f in files if f.endswith('.' + ext)]
        sys.stderr.write("Found %d '%s' files\n" % (len(files), ext))
        # for each file
        for i, filename in enumerate(files):
            words: List[str] = []
            if ext == 'txt' or ext == 'html':
                words = get_words_from_txt_file(filename)
            elif ext == 'epub' or ext == 'epub_;' or 'epub' in ext:
                words = get_words_from_epub_file(filename)
            else:
                sys.stderr.write('%s not supported.' % ext)

            # Extract n-grams
            unigram_freqs.update(ngrams(words, 1))
            bigram_freqs.update(ngrams(words, 2))
            # Verbose
            print_progress(i+1, len(files), ext)
        if files:
            sys.stderr.write('\n')
    sys.stderr.write("done processing files\n")
    return unigram_freqs, bigram_freqs


if __name__ == "__main__":
    if len(sys.argv) == 3:
        path = sys.argv[1]
        exts = sys.argv[2].split(',')
    else:
        sys.stderr.write(
            "Usage:   ./gramify.py <dir/> <extention1,extention2...>\n")
        sys.stderr.write(
            "Example: ./gramify.py corpus/ txt,html,epub\n")
        sys.exit()

    uni_filename = "out/uni_freq.txt"
    bi_filename = "out/bi_freq.txt"

    unigram_freqs, bigram_freqs = process_files(path, exts)
    write_ngram_freq_to_file(unigram_freqs, uni_filename)
    write_ngram_freq_to_file(bigram_freqs, bi_filename)
