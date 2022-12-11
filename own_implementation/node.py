# by default all mix nodes have index -1

class Node:
    def __init__(self, category, index):
        self.index = index
        self.category = category
        self.children = []

    # inputs a node object and a list of children nodes and appends the children to the nodes list.
    def insert_child(node, kids):
        node.children = node.children + kids

    # # make a copy of this node
    # def copy(self):
    #     newnode = Node(self.category, self.index)
    #     return newnode

    # need a function that adds prepare actions if necessary

    # need a function that adds cooking actions if necessary (prepare actions are always added first)


class Tree:
    def __init__(self, root):
        self.root = root

    # inputs a list of trees and checks if the root nodes of each tree have the same action node. Returns a list of
    # the mixed trees
    def check_same_act(trees):
        newtrees = []  # new list of mixed trees
        iterate = trees.copy()  # make copy of tree list for iterating thru
        for tree in iterate:
            trees.remove(tree)  # trees to check
            i = 0
            for check in trees:
                if (check.root.category == tree.root.category) and (
                        check.root.index == tree.root.index):  # if the same action is applied on the root node to
                    # two ingredients
                    action = [check.root.category, check.root.index]  # store the common action
                    newmix = Node("mix", -1)  # new mix node
                    newmix.insert_child(
                        [tree.root.children[0], check.root.children[0]])  # mix the ingredients using a tree
                    newact = Node(action[0], action[1])  # common action node
                    newact.insert_child([newmix])  # new mix node is the child of the common action
                    tree = Tree(newact)  # create new tree
                    iterate.remove(check)  # remove checked tree from tree list

            newtrees.append(tree)
        return newtrees

    # inputs a list of trees and outputs a singular mixed and valid tree
    def make_valid(trees):
        if len(trees) == 1:  # if singular tree output it
            valid = trees[0]
        else:
            newmix = Node("mix", -1)  # new mix node
            children = []  # children of mix node
            for tree in trees:
                children.append(tree.root)  # all roots of subtrees are the children of new mix node
            newmix.insert_child(children)  # set children of new mix node
            valid = Tree(newmix)  # create valid tree
        return valid

    # helper function for copy tree. Inputs root node to the tree and outputs the root node to the copy of the tree
    def clone_tree(self, root):
        if not root:
            return None
        newnode = Node(root.category, root.index)  # copy root node
        for child in root.children: # append the copy of the subtree to the root node's child list
            newnode.children.append(self.clone_tree(child))
        return newnode

    # copy the tree
    def copy(self):
        return Tree(self.clone_tree(self.root))
