class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __str__(self):
        if not self.left and not self.right:
            return str(self.value)

        left_str = str(self.left) if self.left else ""
        right_str = str(self.right) if self.right else ""

        return f"{self.value} ({left_str},{right_str})"


def parse_tree(s: str) -> Node:
    s = s.strip()

    def skip_spaces(i):
        while i < len(s) and s[i].isspace():
            i += 1
        return i

    def parse_subtree(i=0):
        i = skip_spaces(i)

        start = i
        while i < len(s) and (s[i].isdigit() or s[i] == '-'):
            i += 1
        value = int(s[start:i])
        node = Node(value)

        i = skip_spaces(i)

        if i < len(s) and s[i] == '(':
            i += 1
            i = skip_spaces(i)

            if i < len(s) and s[i] not in ',)':
                node.left, i = parse_subtree(i)

            i = skip_spaces(i)

            if i < len(s) and s[i] == ',':
                i += 1
                i = skip_spaces(i)

            if i < len(s) and s[i] != ')':
                node.right, i = parse_subtree(i)

            i = skip_spaces(i)

            if i < len(s) and s[i] == ')':
                i += 1

        return node, i

    root, _ = parse_subtree(0)
    return root

def preorder_iterative(root):
    stack = list()
    stack.append(root)

    while len(stack) != 0:
        cur = stack[-1]
        print(cur.value, end=" ")
        stack.pop()

        if cur.right is not None:
            stack.append(cur.right)

        if cur.left is not None:
            stack.append(cur.left)

tree_str = "8 (3 (1, 6 (4,7)), 10 (, 14(13,)))"
tree = parse_tree(tree_str)

preorder_iterative(tree)



