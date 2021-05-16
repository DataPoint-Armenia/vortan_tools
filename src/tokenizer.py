#!/usr/bin/python

# modules
from util import get_text_from_txt_file
import sys
import os

# extern
sys.path.insert(0, './extern/vortan_tokenizer/')
from tokenizer import Tokenizer

def tokenize(text):
    T = Tokenizer(text)
    T.segmentation().tokenization()
    return T

if __name__ == "__main__":

    # Tokenize file
    filename = "data/test_book.txt"
    file_text = get_text_from_txt_file(filename)

    # Tokenize text
    str_text = """
    Նա սենյակ մտավ՝ ծածկելու պատուհանները, երբ մենք դեռ անկողնում էինք, ու տեսա, որ տեսքը հիվանդի է։
    Ի՞նչ ես կարծում, քանի՞ ժամից կմեռնեմ։
    """

    t = tokenize(str_text)

    print(t)
