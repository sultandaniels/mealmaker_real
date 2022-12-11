import numpy as np
import numpy.random as rand
import node as nd


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
