SH = 0; RE = 1; RA = 2; LA = 3;
labels = ["det", "nsubj", "case", "nmod", "root"]


def attach_orphans(arcs, n):
    attached = []
    for (h, d, l) in arcs:
        attached.append(d)
    for i in range(1, n):
        if i not in attached:
            arcs.append((0, i, "root"))


def print_tree(root, arcs, words, indent):
    if root == 0:
        print(" ".join(words[1:]))
    children = [(root, i, l) for i in range(len(words)) for l in labels if (root, i, l) in arcs]
    for (h, d, l) in sorted(children):
        print(indent + l + "(" + words[h] + "_" + str(h) + ", " + words[d] + "_" + str(d) + ")")
        print_tree(d, arcs, words, indent + "  ")


def transition(trans, stack, buffer, arcs):
    # add code for missing transitions: (RE, "_"), (RA, label), (LA, label)
    dep_in_arc = []
    for (h, d, l) in arcs:
        dep_in_arc.append(d)

    if trans[0] == LA:
        # dependents_la = []
        # for (h, d, l) in arcs:
        #     dependents_la.append(d)
        if not stack[0] in dep_in_arc:
            if stack[0] != 0:
                arcs.append((buffer[0], stack[0], trans[1]))
                stack.pop(0)

    elif trans[0] == RA:
        arcs.append((stack[0], buffer[0], trans[1]))
        stack.insert(0, buffer.pop(0))

    elif trans[0] == RE:
        # dependents_re = []
        # for (h, d, l) in arcs:
        #     dependents_re.append(d)
        if stack[0] in dep_in_arc:
            stack.pop(0)

    else:
        stack.insert(0, buffer.pop(0))

    return stack, buffer, arcs


def parse():
    words = "root the cat is on the mat today".split()
    stack = [0]
    buffer = [x for x in range(1, len(words))]
    arcs = []
    for trans in [(SH, "_"), (LA, "det"), (SH, "_"), (LA, "nsubj"), (SH, "_"), (SH, "_"), (SH, "_"), (LA, "det"),
                  (LA, "case"), (RA, "nmod"), (RE, "_"), (RA, "nmod")]:
        stack, buffer, arcs = transition(trans, stack, buffer, arcs)
    attach_orphans(arcs, len(words))
    print_tree(0, arcs, words, "")


if __name__ == "__main__":
    parse()
