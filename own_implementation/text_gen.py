import node as nd
import numpy as np


def gen_strings_ing(node, strings, acts, ings, ing_ind):
    if not node:
        return None
    if node.category == "action":
        strings.append(acts[node.index])
    if node.category == "ing":
        if node.index == ing_ind:
            strings.append(ings[node.index])
            return strings
    if node.category == "mix":
        strings.append("mix")

    for child in node.children:
        if gen_strings_ing(child, strings, acts, ings, ing_ind):
            return strings

    return None


def gen_strings(node, acts, ings, ing_inds):
    lst_strings = []
    for ind in ing_inds:
        lst_strings.append(gen_strings_ing(node, [], acts, ings, ind))

    return lst_strings


def gen_statements(lsts):
    lens = [None] * len(lsts)
    for i in range(0, len(lsts)):
        lens[i] = len(lsts[i])

    max_ind = lens.index(max(lens))

    statements = [""] * len(lsts)
    first_mix = [0] * len(lsts)
    for i in range(0, lens[max_ind]):  # downwards iterations
        for j in range(0, len(lsts)):  # rightwards iteration
            if i == 0:
                if lsts[j][i] == "mix":  # remove mix from list
                    first_mix[j] = 1
                    lsts[j].remove("mix")
                    print(lsts[j])
            if i < len(lsts[j]):
                if i == 0:
                    statements[j] = lsts[j][i]
                elif i < len(lsts[j]) - 2 and len(lsts[j]) > 2:
                    statements[j] = statements[j] + ", " + lsts[j][i]
                elif i == len(lsts[j]) - 2 and len(lsts[j]) > 2:
                    statements[j] = statements[j] + " and " + lsts[j][i]
                else:
                    statements[j] = statements[j] + " " + lsts[j][i]

    return [statements, first_mix]


def gen_output(statements):
    mixed = np.nonzero(statements[1])
    mixed = mixed[0].tolist()
    count = 1

    for ind in mixed:
        print(count, ". " + statements[0][ind], sep="")
        count = count + 1

    print(count, ". " + "Mix the above ingredients", sep="")
    count = count + 1

    for ind in range(0, len(statements[1])):
        if ind not in mixed:
            print(count, ". " + statements[0][ind], sep="")
            count = count + 1

    print(count, ". " + "Enjoy!", sep="")
