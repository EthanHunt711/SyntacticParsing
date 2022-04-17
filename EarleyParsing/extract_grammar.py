"""a class for creating two objects: dictionary grammar and list pos_tags"""
import json
from collections import defaultdict


class Grammar:
    grammar = defaultdict(list)

    def __init__(self, raw_g_file):
        self.raw_g_file = raw_g_file

    def remove_duplicate(self, grammar_dic):  # removing duplicate grammatical symbols from any given list
        d = defaultdict(list)
        for k in grammar_dic:
            new_list = []
            for kk in grammar_dic[k]:
                if kk not in new_list:
                    new_list.append(kk)
            d[k] = new_list
        return d

    def extract_grammar(self):  # extracting a cfg grammar from the raw file produced by treebank_grammar.py
        with open(self.raw_g_file, 'r') as in_f:
            pos_list = []
            for line in in_f:
                w = json.loads(line)
                for k, v in w[0].items():
                    g_rule = []
                    for xx in w[1]:
                        if isinstance(xx, dict):
                            for kk, vv in xx.items():
                                g_rule.insert(0, vv)
                            self.grammar[v].append(g_rule)
                        else:
                            self.grammar[v].append(xx)
                            pos_list.append(v)
        return self.remove_duplicate(self.grammar), list(dict.fromkeys(pos_list))
