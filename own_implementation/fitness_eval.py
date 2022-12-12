# This module defines functions for section "4) Fitness Evaluation" of the paper

import initial_popul as pop
import node as nd
from itertools import product


# ingredient heat score
def s_heat(B_h, ing_list, agroup_x_ing, thresh_heat, eps_heat):
    s_h = [None] * len(B_h)
    """
    returns a list of booleans of the same length as B_h; when in doubt, set thresh_heat=0.65 and eps_heat=0.1
    """
    i = 0
    for ing in ing_list:
        if pop.heat_ratio(ing, ing_list, agroup_x_ing) > thresh_heat + eps_heat and not B_h[i]:
            s_h[i] = 0
        elif pop.heat_ratio(ing, ing_list, agroup_x_ing) < thresh_heat - eps_heat and B_h[i]:
            s_h[i] = 0
        else:
            s_h[i] = 1

        i = i + 1
    return s_h


# ingredient prep score
def s_prep(B_p, ing_list, agroup_x_ing, thresh_prep, eps_prep):
    """
    returns a list of booleans of the same length as B_p; when in doubt, set thresh_prep=0.35 and eps_prep=0.1
    """
    s_p = [None] * len(B_p)
    """
    returns a list of booleans of the same length as B_h; when in doubt, set thresh_heat=0.65 and eps_heat=0.1
    """
    i = 0
    for ing in ing_list:
        if pop.prep_ratio(ing, ing_list, agroup_x_ing) > thresh_prep + eps_prep and not B_p[i]:
            s_p[i] = 0
        elif pop.prep_ratio(ing, ing_list, agroup_x_ing) < thresh_prep - eps_prep and B_p[i]:
            s_p[i] = 0
        else:
            s_p[i] = 1

        i = i + 1
    return s_p


# number of actions on an ingredient
# input node, number of actions, and ingredient index
# output number of actions done to an ingredient
def num_acts(node, act_num, i):
    if not node:
        return None
    if node.category == "ing" and node.index == i:
        return act_num
    if node.category == "action":
        act_num = act_num + 1

    for child in node.children:
        val = num_acts(child, act_num, i)
        if val:
            return val

    return None


# number of duplicate actions on an ingredient
# input node, number of actions, ingredient index, and seen action indices
# output number of duplicate actions done to an ingredient
def num_dup_acts(node, dup_num, i, act_inds):
    if not node:
        return None
    if node.category == "ing" and node.index == i:
        return dup_num
    if node.category == "action":  # action node
        if node.index in act_inds:  # duplicate action
            dup_num = dup_num + 1
        else:
            act_inds.append(node.index)  # new action

    for child in node.children:
        val = num_dup_acts(child, dup_num, i, act_inds)
        if val is not None:
            return val

    return None


# inputs a tree and outputs list of action scores for each ingredient
def s_act(tree, ing_inds):
    s_a_list = []  # list of action scores
    for ing in ing_inds:
        n_a = num_acts(tree.root, 0, ing)  # number of actions on an ing
        n_da = num_dup_acts(tree.root, 0, ing, [])  # num of dup acts
        s_a_list.append((n_a - n_da) / n_a)  # score function
    return s_a_list


# final ingredient score list (normalized sum)
def s_ing(s_h, s_p, s_a):
    s_ing_list = []
    for i in range(0, len(s_a)):
        s_ing_list.append(0.5 * (s_h[i] + s_p[i] + s_a[i]))
    return s_ing_list


# inputs an action node and outputs list that specifies
# whether this action is valid for the ingredients it
# is applied to
def s_act_nodes(node, act_ind, act_ing_mat, s_i):
    queue = [node]
    while len(queue):
        node = queue.pop(0)
        if node.category == "ing":
            if act_ing_mat[act_ind, node.index]:
                s_i.append(1)
            else:
                s_i.append(0)
        for child in node.children:
            if child is not None:
                queue.append(child)

    return s_i


# inputs a mix node and a list that is the length
# of the mix nodes child list
# outputs list of subtree ingredient sets
def s_mix_tuples(node, s_i):
    for i in range(0, len(s_i)):  # BFS on each child of mix node
        s_i[i] = []
        queue = [node.children[i]]  # start bfs on child of mix node
        while len(queue):
            current = queue.pop(0)  # get next node in the queue
            if current.category == "ing":  # add ing index to sublist
                s_i[i].append(current.index)
            for child in current.children:  # add child nodes to the queue
                if child is not None:
                    queue.append(child)

    return s_i


# cartesian product of all ingredient pairs
def tuple_pairs(s_i):
    tups = []
    for i in range(0, len(s_i)):
        for j in range(i + 1, len(s_i)):
            tups = tups + list(product(s_i[i], s_i[j]))
    return tups


# inputs pairwise tuples and ingredient adj matrix
# outputs mix node score
def s_mix(tups, ing_ing_mat):
    counter = 0
    sum = 0
    for tup in tups:
        sum = sum + ing_ing_mat[tup[0], tup[1]]
        counter = counter + 1

    return sum / counter
