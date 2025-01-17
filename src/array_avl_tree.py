
import numpy as np

class AVLTreeArray:
    def __init__(self):
        self.tree = np.full(1024, None, dtype=object)  # Preallocate with a fixed size

    def height(self, index):
        if index >= len(self.tree) or self.tree[index] is None:
            return 0
        left_index = 2 * index + 1
        right_index = 2 * index + 2
        left_height = self.height(left_index)
        right_height = self.height(right_index)
        return 1 + max(left_height, right_height)

    def balance_factor(self, index):
        if index >= len(self.tree) or self.tree[index] is None:
            return 0
        left_index = 2 * index + 1
        right_index = 2 * index + 2
        return self.height(left_index) - self.height(right_index)

    def update_height(self, index):
        if index >= len(self.tree) or self.tree[index] is None:
            return
        left_index = 2 * index + 1
        right_index = 2 * index + 2
        left_height = self.height(left_index)
        right_height = self.height(right_index)
        # Only update the height of the node
        self.tree[index] = self.tree[index]  # Store the key in the array, height is dynamic

    def left_rotate(self, index):
        right_index = 2 * index + 2
        if right_index >= len(self.tree) or self.tree[right_index] is None:
            return

        # Swap the current node with the right child
        self.tree[index], self.tree[right_index] = self.tree[right_index], self.tree[index]
        
        # Perform rotation to balance the structure
        left_of_right = 2 * right_index + 1
        if left_of_right < len(self.tree):
            self.tree[2 * index + 2] = self.tree[left_of_right]

    def right_rotate(self, index):
        left_index = 2 * index + 1
        if left_index >= len(self.tree) or self.tree[left_index] is None:
            return

        # Swap the current node with the left child
        self.tree[index], self.tree[left_index] = self.tree[left_index], self.tree[index]

        # Perform rotation to balance the structure
        right_of_left = 2 * left_index + 2
        if right_of_left < len(self.tree):
            self.tree[2 * index + 1] = self.tree[right_of_left]

    def rebalance_upward(self, index):
        while index >= 0:
            balance = self.balance_factor(index)

            if balance > 1:  # Left-heavy
                if self.balance_factor(2 * index + 1) < 0:  # Left-Right case
                    self.left_rotate(2 * index + 1)
                self.right_rotate(index)

            elif balance < -1:  # Right-heavy
                if self.balance_factor(2 * index + 2) > 0:  # Right-Left case
                    self.right_rotate(2 * index + 2)
                self.left_rotate(index)

            # Move upward to the parent node
            if index == 0:
                break  # Root node
            index = (index - 1) // 2

    def insert(self, key):
        index = 0
        while index < len(self.tree):
            if self.tree[index] is None:
                self.tree[index] = key  # Only store the key
                break

            current_key = self.tree[index]
            if key < current_key:
                index = 2 * index + 1
            else:
                index = 2 * index + 2

            if index >= len(self.tree):
                self.expand_tree(index)

        self.rebalance_upward(index)

    def expand_tree(self, index):
        new_size = max(len(self.tree) * 2, index + 1)
        new_tree = np.full(new_size, None, dtype=object)
        new_tree[:len(self.tree)] = self.tree
        self.tree = new_tree

    def search(self, key):
        index = 0
        while index < len(self.tree) and self.tree[index] is not None:
            current_key = self.tree[index]
            if key == current_key:
                return True
            elif key < current_key:
                index = 2 * index + 1
            else:
                index = 2 * index + 2
        return False

    def delete(self, key):
        def find_min(index):
            while 2 * index + 1 < len(self.tree) and self.tree[2 * index + 1] is not None:
                index = 2 * index + 1
            return index

        def remove(index):
            left_index = 2 * index + 1
            right_index = 2 * index + 2

            if left_index >= len(self.tree) or self.tree[left_index] is None:
                return right_index  # Return the index of the right child
            elif right_index >= len(self.tree) or self.tree[right_index] is None:
                return left_index  # Return the index of the left child

            min_larger_index = find_min(right_index)
            self.tree[index] = self.tree[min_larger_index]
            self.tree[min_larger_index] = None
            return index  # Make sure this is a valid index to continue rebalancing

        index = 0
        while index < len(self.tree) and self.tree[index] is not None:
            current_key = self.tree[index]
            if key == current_key:
                replacement_index = remove(index)
                if replacement_index is not None:
                    # Ensure we're passing a valid integer index to rebalance
                    self.rebalance_upward(replacement_index)
                return
            elif key < current_key:
                index = 2 * index + 1
            else:
                index = 2 * index + 2
