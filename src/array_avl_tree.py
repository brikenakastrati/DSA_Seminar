import array

class ArrayAVLTree:
    def __init__(self, capacity=1000):
        self.capacity = capacity
        self.size = 0
        self.keys = array.array('i', [0] * capacity)
        self.heights = array.array('i', [0] * capacity)
        self.left = array.array('i', [-1] * capacity)
        self.right = array.array('i', [-1] * capacity)
        self.root = -1

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node_index, key):
        if node_index == -1:
            if self.size >= self.capacity:
                raise Exception("Tree is full")
            node_index = self.size
            self.keys[node_index] = key
            self.heights[node_index] = 1
            self.left[node_index] = -1
            self.right[node_index] = -1
            self.size += 1
            return node_index

        if key < self.keys[node_index]:
            self.left[node_index] = self._insert(self.left[node_index], key)
        else:
            self.right[node_index] = self._insert(self.right[node_index], key)

        self.heights[node_index] = 1 + max(self._get_height(self.left[node_index]),
                                           self._get_height(self.right[node_index]))

        balance = self._get_balance(node_index)

        # Left Left Case
        if balance > 1 and key < self.keys[self.left[node_index]]:
            return self._right_rotate(node_index)

        # Right Right Case
        if balance < -1 and key > self.keys[self.right[node_index]]:
            return self._left_rotate(node_index)

        # Left Right Case
        if balance > 1 and key > self.keys[self.left[node_index]]:
            self.left[node_index] = self._left_rotate(self.left[node_index])
            return self._right_rotate(node_index)

        # Right Left Case
        if balance < -1 and key < self.keys[self.right[node_index]]:
            self.right[node_index] = self._right_rotate(self.right[node_index])
            return self._left_rotate(node_index)

        return node_index

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node_index, key):
        if node_index == -1:
            return node_index

        if key < self.keys[node_index]:
            self.left[node_index] = self._delete(self.left[node_index], key)
        elif key > self.keys[node_index]:
            self.right[node_index] = self._delete(self.right[node_index], key)
        else:
            if self.left[node_index] == -1:
                return self.right[node_index]
            elif self.right[node_index] == -1:
                return self.left[node_index]

            min_node = self._get_min_value_node(self.right[node_index])
            self.keys[node_index] = self.keys[min_node]
            self.right[node_index] = self._delete(self.right[node_index], self.keys[min_node])

        if node_index == -1:
            return node_index

        self.heights[node_index] = 1 + max(self._get_height(self.left[node_index]),
                                           self._get_height(self.right[node_index]))

        balance = self._get_balance(node_index)

        # Left Left Case
        if balance > 1 and self._get_balance(self.left[node_index]) >= 0:
            return self._right_rotate(node_index)

        # Right Right Case
        if balance < -1 and self._get_balance(self.right[node_index]) <= 0:
            return self._left_rotate(node_index)

        # Left Right Case
        if balance > 1 and self._get_balance(self.left[node_index]) < 0:
            self.left[node_index] = self._left_rotate(self.left[node_index])
            return self._right_rotate(node_index)

        # Right Left Case
        if balance < -1 and self._get_balance(self.right[node_index]) > 0:
            self.right[node_index] = self._right_rotate(self.right[node_index])
            return self._left_rotate(node_index)

        return node_index

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node_index, key):
        if node_index == -1:
            return -1
        if self.keys[node_index] == key:
            return node_index
        if key < self.keys[node_index]:
            return self._search(self.left[node_index], key)
        return self._search(self.right[node_index], key)

    def _get_height(self, node_index):
        if node_index == -1:
            return 0
        return self.heights[node_index]

    def _get_balance(self, node_index):
        if node_index == -1:
            return 0
        return self._get_height(self.left[node_index]) - self._get_height(self.right[node_index])

    def _left_rotate(self, z):
        y = self.right[z]
        T2 = self.left[y]

        self.left[y] = z
        self.right[z] = T2

        self.heights[z] = 1 + max(self._get_height(self.left[z]), self._get_height(self.right[z]))
        self.heights[y] = 1 + max(self._get_height(self.left[y]), self._get_height(self.right[y]))

        return y

    def _right_rotate(self, z):
        y = self.left[z]
        T3 = self.right[y]

        self.right[y] = z
        self.left[z] = T3

        self.heights[z] = 1 + max(self._get_height(self.left[z]), self._get_height(self.right[z]))
        self.heights[y] = 1 + max(self._get_height(self.left[y]), self._get_height(self.right[y]))

        return y

    def _get_min_value_node(self, node_index):
        current = node_index
        while self.left[current] != -1:
            current = self.left[current]
        return current
