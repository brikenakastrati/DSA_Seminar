class AVLTreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTreeReference:
    def __init__(self):
        self.root = None

    def insert(self, root, key):
        if not root:
            return AVLTreeNode(key)

        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        balance = self.get_balance(root)

        # Left Left Case
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        # Right Right Case
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        # Left Right Case
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left Case
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete(self, root, key):
        """
        Delete one node from the tree, ensuring the root node is never deleted directly.
        If the key matches the root node, delete one of its child or leaf nodes instead.
        """
        if not root:
            return root

        if root.key == key:
            # Delete one of the child or leaf nodes
            leaf_node, parent = self.find_leaf(root, None)
            if leaf_node:
                # Delete the leaf node without printing
                if parent:
                    if parent.left == leaf_node:
                        parent.left = None
                    elif parent.right == leaf_node:
                        parent.right = None
                return root  # Return the root since we don't delete it
        elif key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            # Perform standard deletion if the node to be deleted is not the root
            if not root.left:
                temp = root.right
                root = None
                return temp
            elif not root.right:
                temp = root.left
                root = None
                return temp

            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)

        # Update the height
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # Rebalance the tree if necessary
        balance = self.get_balance(root)

        # Left Left Case
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)

        # Right Right Case
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)

        # Left Right Case
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left Case
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def find_leaf(self, node, parent):
        """
        Find any leaf node (node with no children) and return it along with its parent.
        """
        if not node:
            return None, None
        if not node.left and not node.right:
            return node, parent  # Return the leaf node and its parent
        # Search for a leaf node in the left subtree first
        left_leaf, left_parent = self.find_leaf(node.left, node)
        if left_leaf:
            return left_leaf, left_parent
        # If no leaf found in the left subtree, search in the right subtree
        return self.find_leaf(node.right, node)

    def search(self, root, key):
        # No print statements here, just search and return the result
        if not root:
            return None
        if root.key == key:
            return root
        if key < root.key:
            return self.search(root.left, key)
        return self.search(root.right, key)

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def get_min_value_node(self, root):
        current = root
        while current.left:
            current = current.left
        return current
