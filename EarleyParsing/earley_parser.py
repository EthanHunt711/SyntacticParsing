import sys
from sys import argv, stderr
from time import time
from state_cl import State
from extract_grammar import Grammar

"""Earley parsing class containing the operations and the parser"""


class EarleyOperations:
    def __init__(self, words, grammar, pos_tags):
        self.grammar = grammar
        self.words = words
        self.chart = [[] for _ in range(len(words) + 1)]
        self.current_id = 0
        self.pos_tags = pos_tags

    def enqueue(self, state, chart_position):
        if state not in self.chart[chart_position]:
            self.chart[chart_position].append(state)
        else:
            self.current_id -= 1

    def next_state_id(self):
        self.current_id += 1
        return self.current_id - 1

    # a class method for checking whether in a given state the rhs is a POS or returns a terminal
    def is_pos(self, rhs_symbol):
        return rhs_symbol in self.pos_tags

    def is_complete(self, state):
        return len(state.grammar_rule) == state.dot_idx

    def predictor(self, state):
        for post_dot_grammar_rule in self.grammar[state.after_dot()]:
            self.enqueue(
                State(self.next_state_id(),
                      state.after_dot(),
                      post_dot_grammar_rule,
                      0,
                      state.subtree_end_position,
                      state.subtree_end_position,
                      [],
                      'Predictor'),
                state.subtree_end_position)

    def scanner(self, state):
        if self.words[state.subtree_end_position] in self.grammar[state.after_dot()]:
            self.enqueue(
                State(self.next_state_id(),
                      state.after_dot(),
                      [self.words[state.subtree_end_position]],
                      1,
                      state.subtree_end_position,
                      state.subtree_end_position+1,
                      [],
                      'Scanner'),
                state.subtree_end_position + 1)

    def completer(self, state):
        for sub_state in self.chart[state.subtree_start_position]:
            if not sub_state.complete() and sub_state.after_dot() == state.lhs_symbol and sub_state.subtree_end_position == state.subtree_start_position and sub_state.lhs_symbol != 'gamma':
                self.enqueue(State(self.next_state_id(),
                                   sub_state.lhs_symbol,
                                   sub_state.grammar_rule,
                                   sub_state.dot_idx + 1,
                                   sub_state.subtree_start_position,
                                   state.subtree_end_position,
                                   sub_state.pointers + [state.state_id],
                                   'completer'),
                             state.subtree_end_position)

    def earley_parser(self):

        self.enqueue(State(0, 'gamma', ['S'], 0, 0, self.next_state_id(), [], 'Axiom'), 0)  # the dummy first state

        for i in range(len(self.words) + 1):
            for state_p in self.chart[i]:
                if not state_p.complete() and not self.is_pos(state_p.after_dot()):
                    self.predictor(state_p)
                elif not state_p.complete() and self.is_pos(state_p.after_dot()) and i != len(self.words):
                    self.scanner(state_p)
                else:
                    self.completer(state_p)

    def __str__(self):  # a string  for the output of the chart
        out_print_state = ''

        for i, chart in enumerate(self.chart):
            out_print_state += f'\nChart--{i}--\n'
            for state_o in chart:
                out_print_state += str(state_o) + '\n'

        return out_print_state


def parser():
    g = Grammar('out.dat')
    dummy_grammar = g.extract_grammar()[0]

    pos_tags = g.extract_grammar()[1]

    # in order to simplify only a random sentence among the first 20 sentence of the Penn Treebank is used
    earley = EarleyOperations(['There', 'is', 'no', 'asbestos', 'in', 'our', 'products', 'now', '.'],
                              dummy_grammar, pos_tags)
    earley.earley_parser()

    print(earley)


if __name__ == '__main__':
    if len(argv) != 2:
        print("usage: python3 earley_parser.py TREEBANK_GRAMMAR")
        exit()

    in_file = sys.argv[1]

    start = time()
    print('Parsing initiated .... ')

    g = Grammar(in_file)
    dummy_grammar = g.extract_grammar()[0]

    pos_tags = g.extract_grammar()[1]

    # in order to simplify only a random sentence among the first 20 sentence of the Penn Treebank is used
    earley = EarleyOperations(['There', 'is', 'no', 'asbestos', 'in', 'our', 'products', 'now', '.'],
                              dummy_grammar, pos_tags)

    earley.earley_parser()

    print(earley)

    print("Time: %.2fs\n" % (time() - start), file=stderr)
