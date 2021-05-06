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
from util import get_text_from_txt_file

sys.path.insert(0, './extern/vortan_tokenizer/')
from tokenizer import Tokenizer


def print_progress(i, total, ext):
    sys.stderr.write('\r')
    sys.stderr.write("Progress: {0:.1f}%".format(
        i/float(total) * 100) + " of '%s'" % ext)
    sys.stderr.flush()


def get_words_from_txt_file(filename):
    return get_words_from_text(get_text_from_txt_file(filename))


def get_words_from_epub_file(filename):
    return get_words_from_text(get_text_from_epub_file(filename))


def get_words_from_text(text):
    words = []
    T = Tokenizer(text)
    T.segmentation().tokenization()
    for s in T.segments:
        for index, t in enumerate(s['tokens']):
            w = t[1] if index != 0 else t[1].lower()
            words.append(w)
    return words


def process_files(path, exts):
    freqs = Counter()
    for ext in exts:
        # get all .ext file paths recursively
        files = [os.path.join(dirpath, f)
                 for dirpath, dirnames, files in os.walk(path)
                 for f in files if f.endswith('.' + ext)]
        sys.stderr.write("Found %d '%s' files\n" % (len(files), ext))
        # for each file
        for i, filename in enumerate(files):
            words = []
            if ext == 'txt' or ext == 'html':
                words = get_words_from_txt_file(filename)
            elif ext == 'epub' or ext == 'epub_;' or 'epub' in ext:
                words = get_words_from_epub_file(filename)
            else:
                sys.stderr.write('%s not supported.' % ext)
            freqs.update(Counter(words))
            print_progress(i+1, len(files), ext)
        if files:
            sys.stderr.write('\n')

    # write output
    with open('out/freq.json', 'w', encoding='utf8') as json_file:
        json.dump(dict(freqs), json_file, ensure_ascii=False)
    sys.stderr.write("done\n")


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

    process_files(path, exts)
