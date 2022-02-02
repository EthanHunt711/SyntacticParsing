def convert_to_cnf(tree):
    #length more than 3
    new_tree = []
    for subtree in tree:
        if len(subtree) > 2:
            new_tree.append(subtree[:1])
        elif len(subtree) == 2:
            subtree = subtree
        elif len(subtree) == 1:
            subtree + subtree

        print(subtree)

        print(new_tree)


ex_tree = ["S", ["NP", ["NNP", "Ms."], ["NNP", "Haag"]], ["VP", ["VBZ", "plays"], ["NP", ["NNP", "Elianti"]]], [".", "."]]
ex2_tree = ["S", ["NP", ["NNP", "Pierre"], ["NNP", "Vinken"]], ["S|NP", ["VP", ["MD", "will"], ["VP|MD", ["ADVP+RB", "soon"]], ["VP", ["VB", "join"],           ["NP",
                  ["DT", "the"],
                  ["NN", "board"]]]]],
      [".", "."]]
convert_to_cnf(ex2_tree)
