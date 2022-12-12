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
        return 0
    if node.category == "ing" and node.index == i:
        return act_num
    if node.category == "action":
        act_num = act_num + 1

    for child in node.children:
        val = num_acts(child, act_num, i)
        if val:
            return val

    return 0


# number of duplicate actions on an ingredient
# input node, number of actions, ingredient index, and seen action indices
# output number of duplicate actions done to an ingredient
def num_dup_acts(node, dup_num, i, act_inds):
    if not node:
        return 0
    if node.category == "ing" and node.index == i:
        return dup_num
    if node.category == "action":  # action node
        if node.index in act_inds:  # duplicate action
            dup_num = dup_num + 1
        else:
            act_inds.append(node.index)  # new action

    for child in node.children:
        val = num_dup_acts(child, dup_num, i, act_inds)
        if val:
            return val

    return 0


# inputs a tree and outputs list of action scores for each ingredient
def s_act(tree, ing_inds):
    s_a_list = []  # list of action scores
    for ing in ing_inds:
        n_a = num_acts(tree.root, 0, ing)  # number of actions on an ing
        n_da = num_dup_acts(tree.root, 0, ing, [])  # num of dup acts
        if n_a:
            s_a_list.append((n_a - n_da) / n_a)  # score function
        else:
            s_a_list.append(0.0)
    return s_a_list


# final ingredient score list (normalized sum)
def s_ing(s_h, s_p, s_a):
    s_ing_list = []
    for i in range(0, len(s_a)):
        s_ing_list.append(0.5 * (s_h[i] + s_p[i] + s_a[i]))
    return s_ing_list


# inputs an action node and outputs its action node score
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
    if len(s_i):
        return sum(s_i) / len(s_i)
    else:
        return 0


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
    accum = 0
    for tup in tups:
        accum = accum + ing_ing_mat[tup[0], tup[1]]
        counter = counter + 1
    if counter:
        return accum / counter
    else:
        return 0


# finds all action nodes, computes their scores
# outputs total action node score and amount of action nodes
def s_act_nodes_sum(tree, act_ing_mat):
    accum = 0
    count = 0
    queue = [tree.root]
    while len(queue):
        node = queue.pop(0)
        if node.category == "action":
            count = count + 1
            accum = accum + s_act_nodes(node, node.index, act_ing_mat, [])
        for child in node.children:
            if child is not None:
                queue.append(child)

    return [accum, count]


def s_ing_nodes_sum(s_ings):
    return [sum(s_ings), len(s_ings)]


# finds all mix nodes, computes their scores
# outputs total mix node score and amount of mix nodes
def s_mix_nodes_sum(tree, ing_ing_mat):
    accum = 0
    count = 0
    queue = [tree.root]
    while len(queue):
        node = queue.pop(0)
        if node.category == "mix":
            count = count + 1
            s_i = [None] * len(node.children)  # empty list that's the size of the child list
            s_i = s_mix_tuples(node, s_i)
            tups = tuple_pairs(s_i)
            accum = accum + s_mix(tups, ing_ing_mat)
        for child in node.children:
            if child is not None:
                queue.append(child)

    return [accum, count]


def node_score(tree, ings, all_ing, ing_inds, actgrp_ing_mat, heat_thresh, prep_thresh, heat_eps, prep_eps, act_ing_mat,
               ing_ing_mat):
    b_h = pop.need_heat_act(ings, all_ing, actgrp_ing_mat, heat_thresh)
    b_p = pop.need_prep_act(ings, all_ing, actgrp_ing_mat, prep_thresh)
    s_h = s_heat(b_h, ings, actgrp_ing_mat, heat_thresh, heat_eps)
    s_p = s_heat(b_p, ings, actgrp_ing_mat, prep_thresh, prep_eps)
    s_a = s_act(tree, ing_inds)
    s_ings = s_ing(s_h, s_p, s_a)

    s_ing_lst = s_ing_nodes_sum(s_ings)
    s_act_lst = s_act_nodes_sum(tree, act_ing_mat)
    s_mix_lst = s_mix_nodes_sum(tree, ing_ing_mat)

    if s_ing_lst[1] + s_act_lst[1] + s_mix_lst[1]:
        return (s_ing_lst[0] + s_act_lst[0] + s_mix_lst[0]) / (s_ing_lst[1] + s_act_lst[1] + s_mix_lst[1])
    else:
        return 0


# computes total number of actions and number of distinct actions
# outputs s_dup, b_acts and b_ings
def s_duplicates_b_acts_b_ings(tree):
    s_dup = 0
    acts = []
    distinct = 0
    total = 0
    b_acts = 0
    b_ings = 0
    ing_amt = 0
    queue = [tree.root]
    while len(queue):
        node = queue.pop(0)
        if node.category == "action":
            if node.index not in acts:
                distinct = distinct + 1
                total = total + 1
                acts.append(node.index)
            else:
                total = total + 1
        if node.category == "ing":
            ing_amt = ing_amt + 1
        for child in node.children:
            if child is not None:
                queue.append(child)
    if total:
        s_dup = distinct / total
    if total > 2:
        b_acts = 1
    if ing_amt > 2:
        b_ings = 1

    return [s_dup, b_acts, b_ings]


def tree_score(tree, ings, all_ing, ing_inds, actgrp_ing_mat, heat_thresh, prep_thresh, heat_eps, prep_eps, act_ing_mat,
               ing_ing_mat):
    s_nodes = node_score(tree, ings, all_ing, ing_inds, actgrp_ing_mat, heat_thresh, prep_thresh, heat_eps, prep_eps,
                         act_ing_mat, ing_ing_mat)
    s_others = s_duplicates_b_acts_b_ings(tree)

    return s_nodes*s_others[0]*s_others[1]*s_others[2]
