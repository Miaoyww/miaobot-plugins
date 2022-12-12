import json
import os
from pathlib import Path
import random
from typing import Any
import difflib

voice_lst = [item.split(".")[0] for item in os.listdir(f"{Path(__file__).parent}/res/dingzhen")]


def a(arg, lst):
    matchlist = []
    for cf in range(20):
        match = difflib.get_close_matches(arg, lst, cutoff=1.0 - cf / 20.0, n=20)
        if len(match) > 0:
            matchlist.append(match[0])
    return matchlist


while True:
    input_arg = input()

    print(a(input_arg, voice_lst))
random.choice()
