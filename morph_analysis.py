import numpy as np
import pymorphy2 as py
from itertools import permutations, combinations, product

from tagging import *
from rules import apply_rules

def parse_sentence(sentence):
    def parse_option(tokens):
        tokens = list(tokens)
        replacements = []
        # # print(tokens)
        while True:
            iter_tokens, replacement = apply_rules(tokens)
            if replacement is None:
                return tokens, replacements
            #             if iter_tokens == tokens:
            #                 return tokens
            replacements += [replacement]
            tokens = iter_tokens

    token_options = [get_tags(word)
                     for word in split_sentence(sentence)
                     if word not in STOP_TOKENS]

    token_options = list(product(*token_options))
    token_options = choose_options(token_options)

    parse_results = []
    for option in token_options:
        _res = parse_option(option)
        if len(_res[0]) == 1 and _res[0][0] == "предлож":
            parse_results += [_res]

    return parse_results