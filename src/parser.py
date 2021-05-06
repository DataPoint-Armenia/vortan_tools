#!/usr/bin/python

# modules
from util import get_text_from_txt_file
import sys
import os
import pathlib

# extern
sys.path.insert(0, './extern/End-to-end-Parser/')
from predict import Predictor

if __name__ == "__main__":
    model_path = "./extern/End-to-end-Parser/model.pkl"
    filename = str(pathlib.Path.cwd()) + "/data/test_sentence.txt"

    model = Predictor(model_path=model_path)
    res = model.predict_raw(input_text=filename)

    print(res)
