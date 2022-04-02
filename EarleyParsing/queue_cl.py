"""This class is derived from Milner's 'Problem Solving with Algorithms'(2013) """


class Queue:
    def __init__(self):
        self.items = []

    def __getitem__(self, position):
        return self.items[position]

    def is_empty(self):
        return self.items == []

    def enqueue(self, item, position):
        self.item = item
        self.position = position
        if item not in self.items:
            self.items.insert(position, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)
