import json
import sys
from time import time
from collections import defaultdict
from sys import stdin, stderr, argv


class Grammar:
    grammar = defaultdict(list)
    # raw_grammar = sys.argv[1]

    def __init__(self, path):
        self.path = path

    def remove_duplicate(self, grammar_dic):
        d = defaultdict(list)
        for k in grammar_dic:
            new_list = []
            for kk in grammar_dic[k]:
                if kk not in new_list:
                    new_list.append(kk)
            d[k] = new_list
        return d

    def extract_grammar(self):
        with open(self.path, 'r') as in_f:
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

    # def load_file(self):


# if __name__ == '__main__':
#
#     if len(argv) != 3:
#         print("usage: python3 extract_grammar.py RAW_GRAMMAR ")
#         exit()
#
#     path = sys.argv[1]
#     extracted_grammar = sys.argv[2]
#     grammar = Grammar(path)
#     print("Extracting grammar from " + path + " ...", file=stderr)
#     grammar.extract_grammar()
#
#     start = time()
