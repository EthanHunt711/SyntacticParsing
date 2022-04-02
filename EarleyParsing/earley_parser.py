from queue_cl import Queue
from state_cl import State

AXIOM = 1; PREDICTOR = 2; SCANNER = 3; COMPLETE = 4;


class EarleyOperations:
    def __init__(self, words, grammar):
        self.grammar = grammar
        self.words = words
        self.chart = [Queue() for _ in range(len(words)+1)]

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

    def is_pos(self, state):
        for word in self.words:
            if word in self.grammar[state.grammar_rule[0]]:
                return True
        return False

    def earley_parser(self):

        self.chart[0].enqueue(State(0, 'gamma', ['S'], 0, 0, 0, [], 'Axiom'), 0)

        for i in range(len(self.words)):
            for state in self.chart[i]:
                # self.predictor(state)
                if state.complete(state.dot_idx) is False and self.is_pos(state) is False:
                    self.predictor(state)
                    print('No1')
                elif state.complete(state.dot_idx) is False and self.is_pos(state) is True:
                    self.scanner(state)
                    print('No2')
                else:
                    self.completer(state)
                    print('No3')
        return self.chart

    def __str__(self):
        res = ''

        for i, chart in enumerate(self.chart):
            res += '\nChart[%d]\n' % i
            for state in chart:
                res += str(state) + '\n'

        return res


def test():
    grammar = {
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
    # terminals = ['Det', 'Noun', 'Verb', 'Aux', 'Prep', 'Proper-Noun']

    earley = EarleyOperations(['book', 'that', 'flight'], grammar)
    earley.earley_parser()
    print(earley)


if __name__ == '__main__':
    test()
    # pass
