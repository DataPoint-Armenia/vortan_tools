#!/usr/bin/python

import sys, os
sys.path.insert(0, './Tokenizer/')

import codecs

from tokenizer import Tokenizer

def getTextFromTxtFile(filename):
    txt_words = []
    try:
        f = codecs.open(filename, encoding='utf-8')
        f.seek(0)
        text = f.read()
        f.close()
    except (UnicodeDecodeError, OSError, IOError) as e:
        pass
    return text

if __name__ == "__main__":
    filename = "./data/test.txt"
    text = getTextFromTxtFile(filename)

    T = Tokenizer(text)
    T.segmentation().tokenization()

    print(T)
