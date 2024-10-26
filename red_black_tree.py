class RBTNode:
    def __init__(self, key, color="RED"):
        self.key = key
        self.color = color  # "RED" or "BLACK"
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.TNULL = RBTNode(0)
        self.TNULL.color = "BLACK"
        self.root = self.TNULL

    def insert(self, key):
        new_node = RBTNode(key)
        new_node.left = self.TNULL
        new_node.right = self.TNULL
        self._insert(new_node)
        print(f"Inserted {key}:")
        self.print_tree()

    def _insert(self, new_node):
        node = self.root
        parent = None

        while node != self.TNULL:
            parent = node
            if new_node.key < node.key:
                node = node.left
            else:
                node = node.right

        new_node.parent = parent
        if parent is None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self.fix_insert(new_node)

    def fix_insert(self, k):
        while k != self.root and k.parent.color == "RED":
            if k.parent == k.parent.parent.left:  # Case A: Parent is a left child
                uncle = k.parent.parent.right
                if uncle.color == "RED":  # Case 1: Uncle is red
                    k.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:  # Case 2: Uncle is black
                    if k == k.parent.right:  # Left-Right case
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.right_rotate(k.parent.parent)
            else:  # Case B: Parent is a right child
                uncle = k.parent.parent.left
                if uncle.color == "RED":  # Case 1: Uncle is red
                    k.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:  # Case 2: Uncle is black
                    if k == k.parent.left:  # Right-Left case
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.left_rotate(k.parent.parent)
        self.root.color = "BLACK"  # Ensure the root is always black

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def delete(self, key):
        self._delete(self.root, key)

    def _delete(self, node, key):
        z = self.TNULL
        while node != self.TNULL:
            if node.key == key:
                z = node
            if node.key <= key:
                node = node.right
            else:
                node = node.left

        if z == self.TNULL:
            print(f"Key {key} not found for deletion.")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == "BLACK":
            self.fix_delete(x)

    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def fix_delete(self, x):
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                w = x.parent.right
                if w.color == "RED":
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == "BLACK" and w.right.color == "BLACK":
                    w.color = "RED"
                    x = x.parent
                else:
                    if w.right.color == "BLACK":
                        w.left.color = "BLACK"
                        w.color = "RED"
                        self.right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = "BLACK"
                    w.right.color = "BLACK"
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == "RED":
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == "BLACK" and w.left.color == "BLACK":
                    w.color = "RED"
                    x = x.parent
                else:
                    if w.left.color == "BLACK":
                        w.right.color = "BLACK"
                        w.color = "RED"
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = "BLACK"
                    w.left.color = "BLACK"
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = "BLACK"  # Ensure that the root is always black

    def inorder(self):
        result = []
        self._inorder_helper(self.root, result)
        return result

    def _inorder_helper(self, node, result):
        if node != self.TNULL:
            self._inorder_helper(node.left, result)
            result.append(node.key)
            self._inorder_helper(node.right, result)

    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        if node != self.TNULL:
            self.print_tree(node.right, level + 1)
            print(" " * 4 * level + "->", node.key, f"({node.color})")
            self.print_tree(node.left, level + 1)


rbt = RedBlackTree()

for value in [21, 17, 16, 5, 4, 1, 10, 18]:
    rbt.insert(value)

print("Final In-order traversal after insertions:", rbt.inorder())

rbt.delete(18)
print("Final In-order traversal after deleting 18:", rbt.inorder())
