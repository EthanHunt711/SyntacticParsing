from queue_cl import Queue
from state_cl import State

AXIOM = 1; PREDICTOR = 2; SCANNER = 3; COMPLETE = 4;

"""Earley parsing class containing the operations and the parser"""


class EarleyOperations:
    def __init__(self, words, grammar):
        self.grammar = grammar
        self.words = words
        self.chart = [Queue() for _ in range(len(words)+1)]  # the chart is a list of queues/instances of Queue class

    def predictor(self, state):
        for post_dot_grammar_rule in self.grammar[state.after_dot()]:
            self.chart[state.subtree_end_position].enqueue(State(state.next_state(),
                                                                 state.after_dot(),
                                                                 post_dot_grammar_rule,
                                                                 0,
                                                                 state.subtree_end_position,
                                                                 state.subtree_end_position,
                                                                 [],
                                                                 'Predictor'),
                                                           state.subtree_end_position)

    def scanner(self, state):
        if self.grammar[state.after_dot()] is self.words[state.subtree_end_position]:
            self.chart[state.subtree_end_position + 1].enqueue(State(state.next_state(),
                                                                     self.grammar[state.after_dot()],
                                                                     self.words[state.subtree_end_position],
                                                                     1,
                                                                     state.subtree_end_position,
                                                                     state.subtree_end_position + 1,
                                                                     [],
                                                                     'Scanner'),
                                                               state.subtree_end_position + 1)

    def completer(self, state):
        if state.dot_idx == 1:
            for state_before_c in self.chart[state.subtree_start_position]:
                if state_before_c.after_dot() == state.lhs_symbol:
                    if state_before_c.subtree_end_position == state.subtree_start_position:
                        self.chart[state.subtree_end_position].enqueue(State(state.next_state(),
                                                                             state_before_c.lhs_symbol,
                                                                             self.grammar[state.lhs_symbol],
                                                                             1,
                                                                             state_before_c.subtree_start_position,
                                                                             state.subtree_end_position,
                                                                             [],
                                                                             'Completer'),
                                                                       state.subtree_end_position)

    def is_pos(self, state):  # a method for checking whether in a given state the dot is at a POS tag
        if self.grammar[state.after_dot()] in self.words:
            return True
        return False

    def earley_parser(self):

        self.chart[0].enqueue(State(0, 'gamma', ['S'], 0, 0, 0, [], 'Axiom'), 0)  # the dummy first state

        for i in range(len(self.words)):
            for n, state_p in enumerate(self.chart[i]):
                # self.predictor(state)
                if state_p.complete(state_p.dot_idx) is False and self.is_pos(state_p) is False:
                    self.predictor(state_p)
                    # print('No1')
                    # print(f'iter{n}')
                elif state_p.complete(state_p.dot_idx) is False and self.is_pos(state_p) is True:
                    self.scanner(state_p)
                    # print('No2')
                else:
                    self.completer(state_p)
                    # print('No3')
        return self.chart

    def __str__(self):  # a string  for the output of the chart
        out_print_state = ''

        for i, chart in enumerate(self.chart):
            out_print_state += f'\nChart{i}\n'
            for state_o in chart:
                out_print_state += str(state_o) + '\n'

        return out_print_state


def test_parser():  # a test method containing a dummy grammar and a sequence of words
    dummy_grammar = {
        'S': [['NP', 'VP'], ['Aux', 'NP', 'VP'], ['VP']],
        'NP': [['Det', 'Nominal'], ['Proper-Noun']],
        'Nominal': [['Noun'], ['Noun', 'Nominal']],
        'VP': [['Verb'], ['Verb', 'NP']],
        'Det': ['that', 'this', 'a'],
        'Noun': ['book', 'flight', 'meal', 'money'],
        'Verb': ['book', 'include', 'prever'],
        'Aux': ['does'],
        'Prep': ['from', 'to', 'on'],
        'Proper-Noun': ['Houston', 'TWA']
    }

    earley = EarleyOperations(['book', 'that', 'flight'], dummy_grammar)
    earley.earley_parser()
    print(earley)


if __name__ == '__main__':
    test_parser()
    # pass
