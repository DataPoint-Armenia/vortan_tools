#!/usr/bin/python
# This Python file uses the following encoding: utf-8

from collections import Counter
import os
import sys
from nltk import FreqDist
from nltk.util import ngrams
from typing import List
from typing import Any
from typing import Tuple
from concurrent.futures import TimeoutError
from codetiming import Timer
from pebble import ProcessPool, ProcessExpired

from util import get_words_from_sentences
from util import extract_ngrams
from util import write_ngram_freq_to_file

if __name__ == "__main__":
    if len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        sys.stderr.write(
            "Usage:   ./gramify_sentences.py <file/>)\n")
        sys.stderr.write(
            "Example: ./gramify.py corpus/wiki_sentences.txt\n")
        sys.exit()

    uni_filename = "out/uni_freq.txt"
    bi_filename = "out/bi_freq.txt"

    print(f"# Parsing file")
    file_sentences = get_words_from_sentences(path)
    print(f"# Extracting ngrams")
    unigram_freqs, bigram_freqs = extract_ngrams(file_sentences)
    print(f"# Writing to files")
    write_ngram_freq_to_file(unigram_freqs, uni_filename, sort=True)
    write_ngram_freq_to_file(bigram_freqs, bi_filename, sort=True)
