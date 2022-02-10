import sys
from sys import stdin, stderr
from json import loads, dumps


def cnf(tree):
    if len(tree) == 2:
        if type(tree[1]) == str:
            return tree
        # list contains two items, string and list
        else:
            new_tree = []
            new_tree.append(f"{tree[0]}+{tree[1][0]}")
            new_tree.extend(tree[1][1:])
            return cnf(new_tree)
    # list contains three symbols, string, list, list
    elif len(tree) == 3:
        if type(tree[1:]) is list:
            return [tree[0], cnf(tree[1]), cnf(tree[2])]
    # List contains more than three symbols, string, list,  list, list, ...
    elif len(tree) > 3:
        if type(tree[1:]) is list:
            new_tree_2 = []
            sub_tree_1 = []
            new_tree_2.append(tree[0])
            new_tree_2.append(tree[1])
            sub_tree_1.append(f'{tree[0]}|{tree[1][0]}')
            sub_tree_1.extend(tree[2:])
            new_tree_2.append(sub_tree_1)
            return cnf(new_tree_2)
    else:
        return print('it is an empty list')


def is_cnf(tree):
    n = len(tree)
    if n == 2:
        return isinstance(tree[1], str)
    elif n == 3:
        return is_cnf(tree[1]) and is_cnf(tree[2])
    else:
        return False


def words(tree):
    if isinstance(tree, str):
        return [tree]
    else:
        ws = []
        for t in tree[1:]:
            ws = ws + words(t)
        return ws


if __name__ == "__main__":
    for line in stdin:
        tree = loads(line)
        sentence = words(tree)
        input = str(dumps(tree))
        conv_tree = cnf(tree)
        if is_cnf(conv_tree) and words(conv_tree) == sentence:
            print(dumps(conv_tree))
        else:
            print("Something went wrong!", file=stderr)
            print("Sentence: " + " ".join(sentence), file=stderr)
            print("Input: " + input, file=stderr)
            print("Output: " + str(dumps(tree)), file=stderr)
            exit()
