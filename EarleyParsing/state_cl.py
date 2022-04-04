"""defining the state class"""


class State:
    def __init__(self, state_id, lhs_symbol, grammar_rule, dot_idx, subtree_start_position, subtree_end_position,
                 pointers, procedure):
        self.state_id = state_id
        self. lhs_symbol = lhs_symbol
        self.grammar_rule = grammar_rule
        self.dot_idx = dot_idx  # if the dot index is zero then the first element is considered for expansion
        self.subtree_start_position = subtree_start_position
        self.subtree_end_position = subtree_end_position
        self.pointers = pointers
        self.procedure = procedure
        # pointers = []
        # grammar_rule = []

    def next_state(self):  # used for numbering the states
        return self.state_id + 1

    def complete(self, dot_idx):  # check whether the state is complete, the idea is if the dot is 1 then the word
        # is prosseced
        self.dot_idx = dot_idx
        if dot_idx == 1:
            return True
        return False

    def after_dot(self):  # returns the category after the dot
        return self.grammar_rule[self.dot_idx]

    def __eq__(self, other):  # used to check if two objects are the same and hence not adding similar states
        return (self.lhs_symbol == other.lhs_symbol and
                self.grammar_rule == other.grammar_rule and
                self.dot_idx == other.dot_idx and
                self.subtree_start_position == other.subtree_start_position and
                self.subtree_end_position == other.subtree_end_position)

    def __str__(self):  # output of the class in a string containing the place of the dot
        state_mode = ''
        for i, rule in enumerate(self.grammar_rule):
            if i == self.dot_idx:
                state_mode += '[BULLET]'
            state_mode += rule + ' '
        if self.dot_idx == len(self.grammar_rule):
            state_mode += '[BULLET]'
            """This part prints out more information than needed for debugging (they will be omitted at the end)"""
        return f'[S{self.state_id} {self.lhs_symbol} -> {self.dot_idx} {state_mode} {self.grammar_rule} {self.after_dot()}' \
               f' {self.complete(self.dot_idx)} [{self.subtree_start_position}, ' \
               f'{self.subtree_end_position}] {self.pointers} {self.procedure}]'
