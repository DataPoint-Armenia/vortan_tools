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

from util import get_text_from_txt_file
from util import get_text_from_epub_file
from util import write_ngram_freq_to_file

sys.path.insert(0, './extern/vortan_tokenizer/')
from tokenizer import VortanTokenizer

AGENT_COUNT = 5  # number of workers
AGENT_TIMEOUT = 10000  # seconds


def print_progress(i: int, total: int, ext: str) -> None:
    sys.stderr.write('\r')
    sys.stderr.write("Progress: {0:.1f}%".format(
        i / float(total) * 100) + " of '%s'" % ext)
    sys.stderr.flush()


def get_words_from_txt_file(filename: str) -> List[str]:
    sys.stderr.write(f"Parsing '{filename}'\n")
    return get_words_from_text(get_text_from_txt_file(filename))


def get_words_from_epub_file(filename) -> List[str]:
    sys.stderr.write(f"Parsing '{filename}'\n")
    return get_words_from_text(get_text_from_epub_file(filename))


# @Timer(text="tokenize: Elapsed time: {:.4f} seconds")
def get_words_from_text(text: str) -> List[List[str]]:
    words = []
    T = VortanTokenizer(text)
    T.segmentation().tokenization()
    for s in T.segments:
        sentence = []
        for index, t in enumerate(s['tokens']):
            w = t[1] if index != 0 else t[1].lower()
            sentence.append(w)
        words.append(sentence)
    return words


# @Timer(text="ngrams: Elapsed time: {:.4f} seconds")
def extract_ngrams(all_sentences: List[List[str]]) -> Tuple[Any, Any]:
    unigram_freqs = FreqDist()
    bigram_freqs = FreqDist()
    for sentences in all_sentences:
        for words in sentences:
            unigram_freqs.update(ngrams(words, 1))
            bigram_freqs.update(ngrams(words, 2))
    return unigram_freqs, bigram_freqs


def get_filenames(ext):
    # get all .ext file paths recursively
    files = [os.path.join(dirpath, f)
             for dirpath, dirnames, files in os.walk(path)
             for f in files if f.endswith('.' + ext)]
    print("Found %d '%s' files" % (len(files), ext))
    return files


def get_parse_method(ext):
    if ext == 'txt' or ext == 'html':
        return get_words_from_txt_file
    elif ext == 'epub' or ext == 'epub_;' or 'epub' in ext:
        return get_words_from_epub_file
    else:
        sys.stderr.write('%s not supported.' % ext)
        return None


def get_sentences_from_files_async(path: str, exts: List[str]) -> List[List[str]]:
    all_sentences = []

    # Process files
    for ext in exts:
        files = get_filenames(ext)
        method = get_parse_method(ext)
        with ProcessPool(max_workers=AGENT_COUNT) as pool:
            future = pool.map(method, files, timeout=AGENT_TIMEOUT)
            iterator = future.result()

            # iterate over all results, if a computation timed out
            # print it and continue to the next result
            while True:
                try:
                    result = next(iterator)
                    all_sentences.append(result)
                except StopIteration:
                    break
                except ProcessExpired as error:
                    print("%s. Exit code: %d" % (error, error.exitcode))
                except Exception as error:
                    print("function raised %s" % error)
                    print(error.traceback)
                except TimeoutError as error:
                    print(
                        f"Killing agent that took longer than {error.args[1]} seconds")

    return all_sentences


def get_sentences_from_files(path: str, exts: List[str]) -> List[List[str]]:
    all_sentences = []

    # Process files
    for ext in exts:
        files = get_filenames(ext)
        method = get_parse_method(ext)
        for filename in files:
            sentences = method(filename)
            all_sentences.append(sentences)

    return all_sentences


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

    print(f"# Parsing files")
    file_sentences = get_sentences_from_files_async(path, exts)
    print(f"# Extracting ngrams")
    unigram_freqs, bigram_freqs = extract_ngrams(file_sentences)
    print(f"# Writing to files")
    write_ngram_freq_to_file(unigram_freqs, uni_filename, sort=True)
    write_ngram_freq_to_file(bigram_freqs, bi_filename, sort=True)
