from sys import argv, stderr
from json import loads, dumps
from collections import defaultdict
from time import time
from nltk import grammar
from nltk.corpus import treebank
from nltk.grammar import Production
from nltk.grammar import Nonterminal
from nltk.grammar import CFG
from nltk.grammar import PCFG

pcfg_dict = defaultdict(float)


def simple_nonterminal(nt):
    sym = nt.symbol()
    if "-" in sym:
        sym = sym.split("-")[0]
    if sym == "":
        sym = "EMPTY"
    if sym in ["#", "$", "SYM"]:
        sym = "SYM"
    elif sym in ["HYPH", '"', ",", "-LRB-", "-RRB-",".", ":", "LS", "``"]:
        sym = "PUNCT"
    elif sym in ["AFX", "JJ", "JJR", "JJS"]:
        sym = "ADJ"
    elif sym in ["CC"]:
        sym = "CONJ"
    elif sym in ["CD"]:
        sym = "NUM"
    elif sym in ["DT", "PDT", "PRP$", "WDT", "WP$"]:
        sym = "DET"
    elif sym in ["EX", "RB", "RBR", "RBS", "WRB"]:
        sym = "ADV"
    elif sym in ["FW", "NIL"]:
        sym = "X"
    elif sym in ["IN"]:
        sym = "ADP"
    elif sym in ["MD"]:
        sym = "AUX"
    elif sym in ["NN", "NNS"]:
        sym = "NOUN"
    elif sym in ["NNP", "NNPS"]:
        sym = "PROPN"
    elif sym in ["POS", "RP", "TO"]:
        sym = "PART"
    elif sym in ["PRP", "WP"]:
        sym = "PRON"
    elif sym in ["UH"]:
        sym = "INTJ"
    elif sym in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]:
        sym = "VERB"

    return Nonterminal(sym)


def simple_rule(r):
    left = simple_nonterminal(r.lhs())
    if r.is_nonlexical():
        right = []
        for rh in r.rhs():
            right.append(simple_nonterminal(rh))
    else:
        right = r.rhs()
    return Production(left, right)


def extract_simple_productions(n):
    rules = []
    new_rules = []
    for t in treebank.parsed_sents()[:n]:
        rules = rules + t.productions()
    for r in rules:
        r = simple_rule(r)
        if not "EMPTY" in str(r):
            new_rules.append(r)
    return new_rules


def sort_rules(rules):
    nt_rules = []
    t_rules = []
    for r in rules:
        if not "EMPTY" in str(r):
            if r.is_nonlexical():
                nt_rules.append(r)
            else:
                t_rules.append(r)
    return sorted(list(set(nt_rules))) + sorted(list(set(t_rules)))


def extract_simple_pcfg(n):
    rules = extract_simple_productions(n)
    pcfg = grammar.induce_pcfg(Nonterminal("S"), rules)
    return PCFG(pcfg.start(), sort_rules(pcfg.productions()))


def extract_simple_cfg(n):
    rules = extract_simple_productions(n)
    rules = list(set(rules))
    return CFG(Nonterminal("S"), sort_rules(rules))


def to_dict_grammar(grammar, nonterminal=""):
    for rule in grammar.productions():
        if nonterminal == "" or rule.lhs().symbol() == nonterminal:
            pcfg_dict[rule.lhs(), rule.rhs()] = rule.prob()
    return pcfg_dict


def save_model(path, diction):
    with open(path, 'w') as model:
        for (lhs, rhs), prob in diction.items():
            model.write(dumps([lhs, rhs, diction[lhs, rhs]], default=lambda o: o.__dict__) + '\n')


if __name__ == '__main__':

    if len(argv) != 2:
        print("usage: python3 treebank_grammar.py GRAMMAR")
        exit()

    grammar_file = argv[1]

    g = extract_simple_pcfg(10)
    ds = to_dict_grammar(g)
    save_model(argv[1], ds)

    #  to_dict_grammar(g)