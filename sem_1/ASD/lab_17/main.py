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

def find_elem(tree, el):
    if el == tree.value:
        print("Exist")
        return tree
    elif tree.right is not None and tree.right.value <= el:
            return find_elem(tree.right, el)
    elif tree.left is not None and tree.left.value >= el:
            return find_elem(tree.left, el)
    else:
        print("Not exist")
        return "Not exist"
    
def add_elem(tree, el):
    if tree is None:
        return Node(el)
    if el == tree.value:
        return tree
    elif el < tree.value:
        tree.left = add_elem(tree.left, el)
    else:
        tree.right = add_elem(tree.right, el)
    return tree

def del_elem(tree, el):
    if tree is None:
        return None

    if el < tree.value:
        tree.left = del_elem(tree.left, el)
    elif el > tree.value:
        tree.right = del_elem(tree.right, el)
    else:
        if tree.left is None and tree.right is None:
            return None
        elif tree.left is None:
            return tree.right
        elif tree.right is None:
            return tree.left
        else:
            successor = tree.right
            while successor.left is not None:
                successor = successor.left
            
            tree.value = successor.value
            tree.right = del_elem(tree.right, successor.value)
    
    return tree

tree_str = "10(5(2,7),15(12,20))"
tree = parse_tree(tree_str)

code = None

operations = {
    1: find_elem,
    2: add_elem,
    3: del_elem
}

while code != 0:
    print(
    """
    0: Stop
    1: find_elem,
    2: add_elem,
    3: del_elem
    """)
    code = int(input("Enter code of operation "))
    if code == 0:
        break
    
    el = int(input("Enter elem of operation "))

    operations[code](tree, el)

print(tree)
