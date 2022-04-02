"""
CKY algorithm from the "Natural Language Processing" course by Michael Collins
https://class.coursera.org/nlangp-001/class
"""
import sys
from sys import stdin, stderr
from time import time
from json import dumps

from collections import defaultdict
from pprint import pprint

from pcfg import PCFG
from tokenizer import PennTreebankTokenizer


def argmax(lst):
    return max(lst) if lst else (0.0, None)


def backtrace(back, bp):
    # Extract the tree from the backpointers
    if len(back) == 4:
        return back[0], back[1]

    elif len(back) == 6:
        return back[0], backtrace(bp[back[3], back[4], back[1]], bp), backtrace(bp[back[4], back[5], back[2]], bp)


def CKY(pcfg, norm_words):

    # Initialize your charts (for scores and backpointers)
    chart = defaultdict(float)
    bp = defaultdict(tuple)

    # Code for adding the words to the chart
    n = len(norm_words)
    for i, (norm, word) in enumerate(norm_words):
        for g_sym, lex_ent in pcfg.q1:
            if norm == lex_ent:
                chart[i, i + 1, g_sym] = pcfg.q1[g_sym, norm]
                bp[i, i + 1, g_sym] = (g_sym, word, i + 1, i)

    # Code for the dynamic programming part, where larger and larger subtrees are built
    for max_p in range(2, n+1):
        for min_p in range((max_p - 2), -1, -1):
            for g_sym in pcfg.N:
                best = 0
                backpointer = None
                for g_sym1, g_sym2 in pcfg.binary_rules[g_sym]:
                    for mid_p in range(min_p + 1, max_p):
                        t1 = chart[min_p, mid_p, g_sym1]
                        t2 = chart[mid_p, max_p, g_sym2]
                        candidate = t1*t2*pcfg.q2[g_sym, g_sym1, g_sym2]
                        if candidate > best:
                            best = candidate
                            backpointer = (g_sym, g_sym1, g_sym2, min_p, mid_p, max_p)
                            chart[min_p, max_p, g_sym] = best
                            bp[min_p, max_p, g_sym] = backpointer

    # Below is one option for retrieving the best trees, assuming we only want trees with the "S" category
    # This is a simplification, since not all sentences are of the category "S"
    # The exact arguments also depends on how you implement your back-pointer chart.
    # Below it is also assumed that it is called "bp"
    return backtrace(bp[0, n, "S"], bp)


class Parser:
    def __init__(self, pcfg):
        self.pcfg = pcfg
        self.tokenizer = PennTreebankTokenizer()
    
    def parse(self, sentence):
        words = self.tokenizer.tokenize(sentence)
        norm_words = []
        for word in words:                # rare words normalization + keep word
            norm_words.append((self.pcfg.norm_word(word), word))
        tree = CKY(self.pcfg, norm_words)
        # tree[0] = tree[0].split("|")[0]
        return tree
    
def display_tree(tree):
    pprint(tree)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("usage: python3 parser.py GRAMMAR")
        exit()

    start = time()
    grammar_file = sys.argv[1]
    print("Loading grammar from " + grammar_file + " ...", file=stderr)    
    pcfg = PCFG()
    pcfg.load_model(grammar_file)
    parser = Parser(pcfg)

    print("Parsing sentences ...", file=stderr)
    for sentence in stdin:
        tree = parser.parse(sentence)
        print(dumps(tree))
    print("Time: (%.2f)s\n" % (time() - start), file=stderr)
