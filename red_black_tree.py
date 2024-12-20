'''
Data structure for Red Black Tree inheriting attributes and functions from RedBlack Node class.
Supports initialization, search, insertion, deletion, find minimum, in order traversal, right and left rotations and fixing consecutive 
red node problem and black node problem after every insert and delete.
'''
class RedBlackTree:
    def __init__(self):
        self.root = None

    # Search a for a node using the key in Red Black Tree
    def search(self, key):
        current_node = self.root
        while current_node is not None:
            if key == current_node.key:
                return current_node
            elif key < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right
        return None

    '''
    Inserts a new node with the specified key into the Red-Black Tree.
    First, it performs a standard binary search tree insertion. It finds the correct position for the new node by 
    comparing its key to existing nodes, moving left if the key is smaller or right if it’s larger, 
    and attaches the new node as a left or right child as needed.
    After insertion, it calls `insert_correction` to enforce Red-Black Tree properties
    '''
    def insert(self, node_value):
        new_node = RedBlackNode(node_value)
        key = node_value[0]
        if self.root is None:
            self.root = new_node
        else:
            current_node = self.root
            while True:
                if key < current_node.key:
                    if current_node.left is None:
                        current_node.left = new_node
                        new_node.parent = current_node
                        break
                    else:
                        current_node = current_node.left
                else:
                    if current_node.right is None:
                        current_node.right = new_node
                        new_node.parent = current_node
                        break
                    else:
                        current_node = current_node.right
        self.insert_correction(new_node)

    '''
     Fixes any violations of Red-Black Tree properties after an insertion.
     This function ensures that the tree maintains balanced properties by recoloring nodes or rotating the tree as necessary, 
     depending on the color of the nodes and their relatives.
    '''
    def insert_correction(self, new_node):
        while new_node.parent and new_node.parent.color == 'red':
            if new_node.grandparent() is None:
                break

            if new_node.parent == new_node.grandparent().left:
                parents_sibling = new_node.parents_sibling()
                if parents_sibling and parents_sibling.color == 'red':
                    new_node.parent.color = 'black'
                    parents_sibling.color = 'black'
                    new_node.grandparent().color = 'red'
                    new_node = new_node.grandparent()
                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.rotate_left(new_node)
                    new_node.parent.color = 'black'
                    if new_node.grandparent():
                        new_node.grandparent().color = 'red'
                        self.rotate_right(new_node.grandparent())
            else:
                parents_sibling = new_node.parents_sibling()
                if parents_sibling and parents_sibling.color == 'red':
                    new_node.parent.color = 'black'
                    parents_sibling.color = 'black'
                    new_node.grandparent().color = 'red'
                    new_node = new_node.grandparent()
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.rotate_right(new_node)
                    new_node.parent.color = 'black'
                    if new_node.grandparent():
                        new_node.grandparent().color = 'red'
                        self.rotate_left(new_node.grandparent())
        self.root.color = 'black'

    '''
    Deletes a node with the specified key from the Red-Black Tree. First finds the node, then either removes it directly 
    if it has at most one child, or swaps it with its in-order successor if it has two children.
    Finally, it calls delete_correction to restore Red-Black Tree properties
    '''
    def delete(self, key):
        node_to_remove = self.search(key)
        if node_to_remove is None:
            return

        if node_to_remove.left is None or node_to_remove.right is None:
            self.replace_node(
                node_to_remove, node_to_remove.left or node_to_remove.right)
        else:
            successor = self.find_min(node_to_remove.right)
            node_to_remove.key = successor.key
            node_to_remove.value = successor.value
            self.replace_node(successor, successor.right)

        self.delete_correction(node_to_remove)

    '''
    Fixes any violations of Red-Black Tree properties after a deletion. 
    This function ensures that the tree remains balanced and adheres to Red-Black rules. 
    It recolors or rotates nodes based on the color of the sibling and its children, depending on the child deleted.
    '''
    def delete_correction(self, node):
        while node != self.root and node is not None and node.color == 'black':
            if node.parent:
                if node == node.parent.left:
                    sibling = node.sibling()
                else:
                    sibling = node.sibling()

                if sibling is None:
                    break

                if sibling.color == 'red':
                    sibling.color = 'black'
                    node.parent.color = 'red'
                    if node == node.parent.left:
                        self.rotate_left(node.parent)
                    else:
                        self.rotate_right(node.parent)
                    sibling = node.sibling()

                if sibling and (sibling.left is None or sibling.left.color == 'black') and \
                   (sibling.right is None or sibling.right.color == 'black'):
                    sibling.color = 'red'
                    node = node.parent
                else:
                    if sibling:
                        if node == node.parent.left:
                            if sibling.right is None or sibling.right.color == 'black':
                                if sibling.left:
                                    sibling.left.color = 'black'
                                sibling.color = 'red'
                                self.rotate_right(sibling)
                                sibling = node.sibling()

                            sibling.color = node.parent.color
                            node.parent.color = 'black'
                            if sibling.right:
                                sibling.right.color = 'black'
                            self.rotate_left(node.parent)
                        else:
                            if sibling.left is None or sibling.left.color == 'black':
                                if sibling.right:
                                    sibling.right.color = 'black'
                                sibling.color = 'red'
                                self.rotate_left(sibling)
                                sibling = node.sibling()

                            sibling.color = node.parent.color
                            node.parent.color = 'black'
                            if sibling.left:
                                sibling.left.color = 'black'
                            self.rotate_right(node.parent)

                    node = self.root
            else:
                break

        if node:
            node.color = 'black'

    '''
    Performs a left rotation on the given node to maintain tree balance.
    Moves the node's right child into its position and shifts the node down to its left.
    '''
    def rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left

        if right_child.left is not None:
            right_child.left.parent = node

        right_child.parent = node.parent

        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child

    '''
    Performs a right rotation on the given node to maintain tree balance.
    Moves the node's left child into its position and shifts the node down to its right.
    '''
    def rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right

        if left_child.right is not None:
            left_child.right.parent = node

        left_child.parent = node.parent

        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child

        left_child.right = node
        node.parent = left_child

    '''
    Replaces `old_node` with `new_node` in the tree structure.
    Updates the parent-child links to reflect the replacement, adjusting the root if necessary.
    '''
    def replace_node(self, old_node, new_node):
        if old_node.parent is None:
            # `old_node` is the root; replace the root with `new_node`
            self.root = new_node
        else:
            # Update the parent's left or right pointer to `new_node`
            if old_node == old_node.parent.left:
                old_node.parent.left = new_node
            else:
                old_node.parent.right = new_node

        if new_node is not None:
            new_node.parent = old_node.parent

    # Find node with minimum key in a subtree
    def find_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    # Perform inorder traversal
    def inorder_traversal(self, node, nodes_list):
        if node is not None:
            self.inorder_traversal(node.left, nodes_list)
            nodes_list.append(node)
            self.inorder_traversal(node.right, nodes_list)


'''
Data structure for node of Red Black Tree
'''

class RedBlackNode:
    def __init__(self, node_value, color='red'):
        self.key = node_value[0]
        self.value = node_value[1]
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

    # Get the grandparent of node
    def grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    # Get the sibling of node
    def sibling(self):
        if self.parent is None:
            return None
        if self == self.parent.left:
            return self.parent.right
        return self.parent.left

    # Get the parent's sibling of node
    def parents_sibling(self):
        if self.parent is None:
            return None
        return self.parent.sibling()


