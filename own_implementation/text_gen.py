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
    first_act = lsts[0][0]
    for i in range(0, lens[max_ind]):  # downwards iterations
        for j in range(0, len(lsts)):  # rightwards iteration
            if i == 0:
                if lsts[j][i] == first_act:  # remove mix from list
                    first_mix[j] = 1
                    lsts[j].remove(first_act)
                    print(lsts[j])
            if i < len(lsts[j]):
                if i == 0:
                    statements[j] = lsts[j][i]
                elif i < len(lsts[j]) - 2 and len(lsts[j]) > 2:
                    statements[j] = statements[j] + ", " + lsts[j][i]
                elif i == len(lsts[j]) - 2 and len(lsts[j]) > 2:
                    statements[j] = statements[j] + " and " + lsts[j][i]
                else:
                    statements[j] = statements[j] + " the " + lsts[j][i]

    return [statements, first_mix, first_act]


def gen_statements_revised(lsts, act_list):
    lens = []
    num_lists = len(lsts)
    i = 0
    while i < num_lists:
        if len(lsts[i]) == 0:
            lsts.remove(lsts[i])
        else:
            lens.append(len(lsts[i]))
            i = i + 1
        num_lists = len(lsts)

    max_ind = lens.index(max(lens))
    # k = 0
    first_act = ""
    if max(lens) > 2 and len(lsts) > 1:
        first_mix = [0] * len(lsts)
        j = 0
        first_act = lsts[0][0]
        lsts[0].remove(first_act)
        if len(lsts[j]) == 0:
            act_list.append("ing")
            act_list.append(first_act)
        else:
            j = 1
            was_same = 0
            count = 0
            while j < len(lsts):  # rightwards iteration
                if lsts[j][0] == first_act:
                    was_same = 1
                    if count == 0:
                        act_list.append(first_act)
                        count = count + 1
                    lsts[j].remove(first_act)
                j = j + 1
        return gen_statements_revised(lsts, act_list)
    else:
        return [lsts, act_list]


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


def gen_output_revised(lsts):
    count = 1
    for lst in lsts[0]:
        if len(lst) == 1:
            print(count, ". Add ", lst[0], sep="")
        else:
            stat = ""
            i = 0
            for str in lst:
                if i == 0:
                    stat = stat + " " + str
                elif i == len(lst) - 1:
                    stat = stat + " the " + str
                elif i == len(lst) - 2 and len(lst) > 2:
                    stat = stat + "and " + str
                else:
                    stat = stat + ", " + str
                i = i + 1

            print(count, ".", stat, sep="")
        count = count + 1

    i = 0
    while i < len(lsts[1]):
        if lsts[1][i] == "ing":
            print(count, ". Add ", lsts[1][i + 1], sep="")
            i = i + 2
        else:
            print(count, ". ", lsts[1][i], " the above ingredients", sep="")
            i = i + 1
        count = count + 1

    print("Enjoy!")





