"""This class is inspired by the definition in Milner's 'Problem Solving with Algorithms'(2013) """


class Queue:
    def __init__(self):
        self.items = []  # defining the queue object as a list

    def __getitem__(self, position):  # in order to be able to use []
        return self.items[position]

    def is_empty(self):  # whether queue is empty
        return self.items == []

    def enqueue(self, item, position, chart):
        if item not in chart[position]:
            chart[position].append(item)
        else:
            self.current_id -= 1

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)
