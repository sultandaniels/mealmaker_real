import numpy as np
import numpy.random as rand
import node as nd
import fitness_eval as fit


# input a node of a tree and mutate one of the mix nodes. (recursively and nondeterministically searches the tree
# a mix node)
# Outputs a boolean that is false if no mix nodes are within the tree
def mix_mut(node):
    if node.category == "mix" and len(node.children) > 2:  # adding another mix node when only two children is invalid
        upper = []  # upper mix node children
        lower = []  # lower mix node children
        ml = len(node.children)  # length of mix node child list
        minds = np.arange(ml)  # mix node child list indices
        np.random.shuffle(minds)  # shuffle mix node child list indices

        k = rand.randint(ml)  # random cutoff between subsets
        for i in range(0, ml):  # deal out children to the upper and lower mix node
            if i < k:
                upper.append(node.children[minds[i]])
            else:
                lower.append(node.children[minds[i]])

        for i in range(0, len(lower)):  # remove lower list from original child list
            node.children.remove(lower[i])

        newmix = nd.Node("mix", -1)  # new mix node
        newmix.insert_child(lower)  # set lower list as new mix node's child list
        print("adding mix node")

        node.insert_child([newmix])  # insert lower mix node into the upper mix node's child list

        return True

    if not node.children:
        return False

    # find mix node
    mixfound = 0  # mix node found
    l = len(node.children)  # length of child list
    i = 0  # go through each child

    inds = np.arange(l)  # list of indices of child list
    rand.shuffle(inds)  # shuffle the indices so that the next child is chosen randomly
    while mixfound == 0 and (i < l):  # while a mix node hasn't been found and the node has children
        if mix_mut(node.children[inds[i]]):  # if mix node is found within one of the subtrees
            mixfound = 1
            return True
        i = i + 1

    return False


# inputs an action node and its parent and deletes the action node from the tree
def del_act(node, parent):
    print("deleting action", node.index)
    parent.children.remove(node)
    parent.insert_child(node.children)

    # merge adjacent mix nodes
    for child in parent.children:  # for every node in the child list
        to_iterate = parent.children.copy()  # make a copy of the child list
        if child.category == "mix":
            to_iterate.remove(child)  # check other nodes in child list
            for other in to_iterate:
                if other.category == "mix":  # if another node is a mix node
                    parent.children.remove(other)  # remove it from the child list
                    child.insert_child(other.children)  # add its children to the other mix nodes child list

    return ...


# inputs a node, its parent, and the action list and adds a random action node to the tree
def add_act(node, parent, acts):
    acts_ind = np.arange(0, len(acts))

    newact = nd.Node("action", rand.randint(len(acts)))  # new random action node
    newact.insert_child([node])  # make og node its child
    print("adding action", newact.index)

    parent.children.remove(node)  # remove og node from parent's child list
    parent.insert_child([newact])  # insert new action to parent's child list

    return ...


# inputs a node of a tree, its parent, and the action list and mutates one of its action nodes
# (recursively and nondeterministically searches the tree for a mix node)
# Outputs a boolean that is false if no action nodes are within the tree
def act_mut(node, parent, acts):
    if node.category == "action":  # adding another mix node when only two children is invalid
        if not parent:  # this means the node is the root and we can't delete it
            add_act(node, parent, acts)
        else:
            choice = rand.randint(2)  # choose to add or delete the action node
            if choice:
                add_act(node, parent, acts)
            else:
                del_act(node, parent)

        return True

    if not node.children:
        return False

    # find action node
    actfound = 0  # mix node found
    l = len(node.children)  # length of child list
    i = 0  # go through each child

    inds = np.arange(l)  # list of indices of child list
    rand.shuffle(inds)  # shuffle the indices so that the next child is chosen randomly
    while actfound == 0 and (i < l):  # while a mix node hasn't been found and the node has children
        if act_mut(node.children[inds[i]], node, acts):  # if mix node is found within one of the subtrees
            actfound = 1
            return True
        i = i + 1

    return False


# inputs a node of a tree, its parent, and the action list and adds a random action node on top of an ingredient node
# (recursively and nondeterministically searches the tree for an ingredient node)
# Outputs a boolean that is false if no ingredient nodes are within the tree
def ing_mut(node, parent, acts):
    if node.category == "ing":  # adding another mix node when only two children is invalid
        add_act(node, parent, acts)
        return True

    if not node.children:
        return False

    # find action node
    actfound = 0  # mix node found
    l = len(node.children)  # length of child list
    i = 0  # go through each child

    inds = np.arange(l)  # list of indices of child list
    rand.shuffle(inds)  # shuffle the indices so that the next child is chosen randomly
    while actfound == 0 and (i < l):  # while a mix node hasn't been found and the node has children
        if ing_mut(node.children[inds[i]], node, acts):  # if mix node is found within one of the subtrees
            actfound = 1
            return True
        i = i + 1

    return False


# given the number of generations, the population, and other parameter, mutate the generation
# choosing the higher scored individual pairwise for the next generation
# finally at the end of the mutations, choose the individual with the highest score
def mutate(gens, population, acts, ings, all_ing, ing_inds, actgrp_ing_mat, heat_thresh, prep_thresh, heat_eps,
           prep_eps, act_ing_mat,
           ing_ing_mat):
    for j in range(0, gens):
        for i in range(0, len(population)):
            nextgen = population[i].copy()  # copy tree
            k = np.random.randint(3)  # random choose how to mutate the copy
            if k == 0:  # mutate mix node
                mix_mut(nextgen.root)
            elif k == 1:  # mutate action node
                act_mut(nextgen.root, None, acts)
            elif k == 2:  # mutate ingredient node
                ing_mut(nextgen.root, None, acts)

            nextgen_score = fit.tree_score(nextgen, ings, all_ing, ing_inds, actgrp_ing_mat, heat_thresh, prep_thresh,
                                           heat_eps, prep_eps, act_ing_mat,
                                           ing_ing_mat)
            currentgen_score = fit.tree_score(population[i], ings, all_ing, ing_inds, actgrp_ing_mat, heat_thresh,
                                              prep_thresh,
                                              heat_eps, prep_eps, act_ing_mat,
                                              ing_ing_mat)

            if nextgen_score > currentgen_score:  # pick the generation with the better score
                population[i] = nextgen

    final_scores = [None] * len(population)
    for i in range(0, len(population)):
        final_scores[i] = fit.tree_score(population[i], ings, all_ing, ing_inds, actgrp_ing_mat, heat_thresh,
                                         prep_thresh,
                                         heat_eps, prep_eps, act_ing_mat,
                                         ing_ing_mat)

    final_ind = final_scores.index(max(final_scores))
    return population[final_ind]
