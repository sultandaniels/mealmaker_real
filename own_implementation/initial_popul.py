# This file defines functions used in the section "2) Initial Population:"
import numpy as np
import node as nd


# NOTICE that this function requires the pre-existence of variable ing_list. See "support_for_initial_population.ipynb" to build this.
def prep_ratio(ing, ing_list, agroup_x_ing):
    """
    returns the ratio of the number of prep actions and the number of heating actions historically applied to an ingredient
    """
    if ing in ing_list:
        idx = ing_list.index(ing)
        if round(agroup_x_ing[2, idx]) == 0:
            return 0
        if round(agroup_x_ing[0, idx]) == 0:
            return 1
        return agroup_x_ing[2, idx] / agroup_x_ing[0, idx]
    else:
        print(ing + ' is an unfamiliar ingredient. MealMaker is proceeding anyway.')
        return 0


def rand_prep(ing, ing_list, agroup_x_ing, prep_thresh):
    """
    returns a boolean value (with randomness) of whether ing should be prepared. If in doubt, set prep_thresh = 0.35
    """
    return prep_ratio(ing, ing_list, agroup_x_ing) > np.random.normal(prep_thresh, 0.2)


def heat_ratio(ing, ing_list, agroup_x_ing):
    """
    returns the ratio of the number of prep actions and the number of heating actions historically applied to an ingredient
    """
    if ing in ing_list:
        idx = ing_list.index(ing)
        if round(agroup_x_ing[2, idx]) == 0:
            return 1
        if round(agroup_x_ing[0, idx]) == 0:
            return 0
        ratio = 1 - agroup_x_ing[2, idx] / agroup_x_ing[0, idx]
        return ratio
    else:
        print(ing + ' is an unfamiliar ingredient. MealMaker is proceeding anyway.')
        return 0


def rand_heat(ing, ing_list, agroup_x_ing, heat_thresh):
    """
    returns a boolean value (with randomness) of whether ing should be prepared. If in doubt, set heat_thresh = 0.65
    """
    return heat_ratio(ing, ing_list, agroup_x_ing) > np.random.normal(heat_thresh, 0.2)


# functions to instantiate trees

# inputs a list of user inputed ingredient names and the list of all ingredient names and outputs a list of their
# indices
def ing_indices(ings, ing_list):
    ing_inds = []
    for ing in ings:
        ing_inds.append(ing_list.index(ing))

    return ing_inds


# inputs list of ingredient indices and outputs a list of trees
def create_trees(ing_inds):
    trees = []
    for ing in ing_inds:
        newing = nd.Node("ing", ing)  # create new ingredient node
        newtree = nd.Tree(newing)  # create new tree
        trees.append(newtree)  # append new tree to tree list

    return trees


# prepare action first, heating action second

# function that takes in the user ingredient list, ing list, prep threshold, and agrp matrix and outputs a
# list of booleans for if a prep action should be added
def need_prep_act(ings, ing_list, agrp_ing, prep_thresh):
    need_prep = []
    for ing in ings:  # ingredient in user ingredient list
        if rand_prep(ing, ing_list, agrp_ing, prep_thresh):
            need_prep.append(1)  # needs prep action
        else:
            need_prep.append(0)  # doesn't need prep action

    return need_prep


# function that takes in the user ingredient list, ing list, and agrp matrix and outputs a
# list of booleans for if a prep action should be added
def need_heat_act(ings, ing_list, agrp_ing, heat_thresh):
    need_heat = []
    for ing in ings:  # ingredient in user ingredient list
        if rand_heat(ing, ing_list, agrp_ing, heat_thresh):
            need_heat.append(1)  # needs prep action
        else:
            need_heat.append(0)  # doesn't need prep action

    return need_heat


# inputs heat(1) or prepare(0) boolean, ingredient index, heat action indices, prepare action indices,
# and action to ingredient matrix
# outputs the action index that will be applied to the ingredient
def choose_act(h_or_p, ing_ind, act_ing_mat, prep_inds, heat_inds):
    val = 0  # frequency of a given action
    if h_or_p:  # if heating action
        chosen_ind = heat_inds[np.random.randint(len(heat_inds))]  # random initialization
        for heat in heat_inds:
            if val < act_ing_mat[heat, ing_ind]:  # if other action has higher freq
                val = act_ing_mat[heat, ing_ind]  # update value of max freq
                chosen_ind = heat  # update index of chosen action
    else:  # if prepare action
        chosen_ind = prep_inds[np.random.randint(len(prep_inds))]  # random initialization
        for prep in prep_inds:
            # print("freq:", act_ing_mat[prep, ing_ind])
            if val < act_ing_mat[prep, ing_ind]:  # if other action has higher freq
                val = act_ing_mat[prep, ing_ind]  # update value of max freq
                chosen_ind = prep  # update index of chosen action

    return chosen_ind


# adds preparation actions where necessary on the ingredient nodes
#
# inputs list of trees, list of user ingredients, list of ing indices, list of all ingredients, action to ing mat,
# list of prepare action indices, list of heat action indices, and action group to ing matrix
# outputs a list of trees
def add_prep_act(output, trees, ings, ing_inds, ing_list, act_ing_mat, prep_inds, heat_inds, actgrp_ing_mat,
                 prep_thresh):
    need_prep = need_prep_act(ings, ing_list, actgrp_ing_mat, prep_thresh)  # boolean list
    i = 0
    if output:
        print("need_prep:", need_prep)
    for need in need_prep:
        if need:
            prep_ind = choose_act(0, ing_inds[i], act_ing_mat, prep_inds, heat_inds)  # find preparation action index
            act_node = nd.Node("action", prep_ind)  # create new action node
            act_node.insert_child([trees[i].root])  # connect new node to the tree
            trees[i].change_root(act_node)  # update the root of the tree
        i = i + 1

    return trees


# adds heating actions where necessary on the trees
#
# inputs list of trees, list of user ingredients, list of ing indices, list of all ingredients, action to ing mat,
# list of prepare action indices, list of heat action indices, action group to ing matrix, and heat threshold outputs
# a list of trees
def add_heat_act(output, trees, ings, ing_inds, ing_list, act_ing_mat, prep_inds, heat_inds, actgrp_ing_mat,
                 heat_thresh):
    need_heat = need_heat_act(ings, ing_list, actgrp_ing_mat, heat_thresh)  # boolean list
    i = 0
    if output:
        print("need_heat:", need_heat)
    for need in need_heat:
        if need:
            heat_ind = choose_act(1, ing_inds[i], act_ing_mat, prep_inds, heat_inds)  # find preparation action index
            act_node = nd.Node("action", heat_ind)  # create new action node
            act_node.insert_child([trees[i].root])  # connect new node to the tree
            trees[i].change_root(act_node)  # update the root of the tree
        i = i + 1

    return trees


# initializes the tree, first argument is a boolean for printing output or not
def initialize_tree(output, ings, all_ing, ing_inds, act_ing_mat, prep_inds, heat_inds, actgrp_ing_mat, prep_thresh,
                    cooking_verbs, heat_thresh):
    if output:
        print("user inputted ings:\n", ings)
        print("ingredient indices:\n", ing_inds)

    trees = create_trees(ing_inds)  # create initial trees
    if output:
        print("\ninitial trees:")
        i = 0
        for tree in trees:
            print("tree", i, "root:", all_ing[tree.root.index])
            i = i + 1

    trees = add_prep_act(output, trees, ings, ing_inds, all_ing, act_ing_mat, prep_inds, heat_inds, actgrp_ing_mat,
                         prep_thresh)
    if output:
        print("\nprepare actions added")
        i = 0
        for tree in trees:
            if tree.root.category == "action":
                print("tree", i, "root:", cooking_verbs[tree.root.index])
            elif tree.root.category == "ing":
                print("tree", i, "root:", all_ing[tree.root.index])
            i = i + 1

    trees = add_heat_act(output, trees, ings, ing_inds, all_ing, act_ing_mat, prep_inds, heat_inds, actgrp_ing_mat,
                         heat_thresh)
    if output:
        print("\nheat actions added")
        i = 0
        for tree in trees:
            if tree.root.category == "action":
                print("tree", i, "root:", cooking_verbs[tree.root.index])
            elif tree.root.category == "ing":
                print("tree", i, "root:", all_ing[tree.root.index])
            i = i + 1

    trees = nd.Tree.check_same_act(trees)
    if output:
        print("\nmerge trees with the same action root")
        i = 0
        for tree in trees:
            if tree.root.category == "action":
                print("tree", i, "root:", cooking_verbs[tree.root.index])
            elif tree.root.category == "ing":
                print("tree", i, "root:", all_ing[tree.root.index])
            i = i + 1

    valid_tree = nd.Tree.make_valid(trees)
    if output:
        print("\nfinal valid tree")
        i = 0
        print("root:", valid_tree.root.category)
        print("root's children:")
        for child in valid_tree.root.children:
            if child.category == "action":
                print("child", i, ":", cooking_verbs[child.index])
            elif child.category == "ing":
                print("child", i, ":", all_ing[child.index])
            i = i + 1

    return valid_tree


# create list of initialized trees
def init_pop(pop_size, ings, all_ing, ing_inds, act_ing_mat, prep_inds, heat_inds, actgrp_ing_mat, prep_thresh,
             cooking_verbs, heat_thresh):
    init_pop = []
    for i in range(0, pop_size):
        init_pop.append(
            initialize_tree(0, ings, all_ing, ing_inds, act_ing_mat, prep_inds, heat_inds, actgrp_ing_mat, prep_thresh,
                            cooking_verbs, heat_thresh))
    return init_pop
