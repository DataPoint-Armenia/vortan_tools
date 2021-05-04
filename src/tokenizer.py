#!/usr/bin/python

# modules
import sys
import os

# extern
sys.path.insert(0, './extern/Tokenizer/')
from tokenizer import Tokenizer

# local
from util import get_text_from_txt_file

if __name__ == "__main__":
    filename = "./data/test_sentence.txt"
    text = get_text_from_txt_file(filename)

    T = Tokenizer(text)
    T.segmentation().tokenization()

    print(T)
