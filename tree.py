from PrettyPrint import PrettyPrintTree


class Node:
    def __init__(self, value, is_operator=False, is_function=False):
        self.id = None
        self.value = value
        self.children = []
        self.is_operator = is_operator
        self.is_function = is_function


def print_tree(tree):
    def format_node(node):
        if node.id is not None:
            return f"{node.id}: [{node.value}]"
        else:
            return node.value
    pt = PrettyPrintTree(lambda x: x.children, lambda x: format_node(x))
    pt(tree)


class Tree:
    def __init__(self, expression):
        self.expression = expression.replace(' ', '')
        self.pos = -1
        self.ch = None
        self.prev = None
        self.parenthesis_state = 0
        self.id_counter = 0

    def next_char(self):
        self.pos += 1
        self.prev = self.ch
        if self.pos < len(self.expression):
            self.ch = self.expression[self.pos]
        else:
            self.ch = None

    def parse_expression(self):
        root = self.parse_term()
        while self.ch in ['+', '-']:
            op = Node(self.ch, is_operator=True)
            op.children.append(root)
            self.next_char()
            op.children.append(self.parse_term())
            root = op
        return root

    def parse_term(self):
        root = self.parse_factor()
        while self.ch in ['*', '/']:
            op = Node(self.ch, is_operator=True)
            op.children.append(root)
            self.next_char()
            op.children.append(self.parse_factor())
            root = op
        return root

    def parse_factor(self):
        if self.ch in ['+', '-']:
            op = Node(self.ch, is_operator=True)
            self.next_char()
            op.children.append(self.parse_factor())
            return op
        elif self.ch == '(':
            self.next_char()
            expr = self.parse_expression()
            self.next_char()
            return expr
        elif self.ch.isnumeric() or self.ch == '.':
            start_pos = self.pos
            dot = False
            while self.ch is not None and self.ch.isnumeric() or (self.ch == '.' and not dot):
                if self.ch == '.':
                    dot = True
                self.next_char()
            return Node(self.expression[start_pos:self.pos])
        elif self.ch.isalpha():
            start_pos = self.pos
            while self.ch is not None and self.ch.isalpha():
                self.next_char()
            name = self.expression[start_pos:self.pos]
            if self.ch == '(':
                self.next_char()
                func = Node(name, is_function=True)
                func.children.append(self.parse_expression())
                self.next_char()
                while self.prev == ',':
                    func.children.append(self.parse_expression())
                    self.next_char()
                return func
            else:
                return Node(name)

    def build(self, optimize=False):
        self.next_char()
        tree = self.parse_expression()
        if self.pos < len(self.expression):
            raise ValueError('Виникла помилка! Будь ласка, виконайте лексичний та синтаксичний аналіз виразу.')
        if optimize:
            optimized_tree = self.optimize_tree(self.optimize_tree(tree))
            self.set_ids(optimized_tree)
            return optimized_tree
        self.set_ids(tree)
        return tree

    def optimize_tree(self, node):
        if node.value == '-':
            if len(node.children) == 2 and node.children[0].value == '-' and self.tree_height(
                    node.children[0]) > self.tree_height(node.children[1]):
                new_child = Node('+', is_operator=True)
                new_child.children = [node.children[1], node.children[0].children[1]]
                node.children[1] = new_child
                node.children[0] = node.children[0].children[0]
                return self.optimize_tree(node)
        while node.value == '+' and node.children[0].value == '+' and node.children[0].children[0].value == '+' and self.tree_height(node.children[0]) > self.tree_height(node.children[1]):
            new_child = Node('+', is_operator=True)
            new_child.children = [node.children[0].children[1], node.children[1]]
            node.children = [node.children[0].children[0], new_child]
        while node.value == '+' and node.children[1].value == '+' and node.children[1].children[1].value == '+' and self.tree_height(node.children[1]) > self.tree_height(node.children[0]):
            new_child = Node('+', is_operator=True)
            new_child.children = [node.children[0], node.children[1].children[0]]
            node.children = [new_child, node.children[1].children[1]]
        while node.value == '*' and node.children[0].value == '*' and node.children[0].children[0].value == '*' and self.tree_height(node.children[0]) > self.tree_height(node.children[1]):
            new_child = Node('*', is_operator=True)
            new_child.children = [node.children[0].children[1], node.children[1]]
            node.children = [node.children[0].children[0], new_child]
        while node.value == '*' and node.children[1].value == '*' and node.children[1].children[1].value == '*' and self.tree_height(node.children[1]) > self.tree_height(node.children[0]):
            new_child = Node('*', is_operator=True)
            new_child.children = [node.children[0], node.children[1].children[0]]
            node.children = [new_child, node.children[1].children[1]]
        if node.value == '/' and node.children[0].value == '/' and node.children[0].children[0].value == '/' and self.tree_height(node.children[0]) > self.tree_height(node.children[1]):
            current = node
            while current.children[0].value == '/':
                new_child_0 = Node('*', is_operator=True)
                new_child_1 = Node('*', is_operator=True)
                new_child_0.children = [current.children[0].children[0].children[0], current.children[0].children[1]]
                new_child_1.children = [current.children[0].children[0].children[1], node.children[1]]
                current.children[0] = new_child_0
                node.children[1] = new_child_1
                current = current.children[0]
            return self.optimize_tree(node)
        if node.value in ['*', '/'] and len(node.children) == 2:
            value_0 = node.children[0].value
            value_1 = node.children[1].value
            if value_0 == '1' or (value_0.startswith('1.') and all(char == '0' for char in value_0[2:])):
                node = node.children[1]
            if value_1 == '1' or (value_1.startswith('1.') and all(char == '0' for char in value_1[2:])):
                node = node.children[0]
        if node.value == '*' and len(node.children[0].children) == 2:
            current = node
            while current.value == '*':
                value_0 = current.children[0].value
                value_1 = current.children[1].value
                if value_0 == '0' or (value_0.startswith('0.') and all(char == '0' for char in value_0[2:])):
                    node = Node('0')
                    break
                if value_1 == '0' or (value_1.startswith('0.') and all(char == '0' for char in value_1[2:])):
                    node = Node('0')
                    break
                current = current.children[0]
            current = node
            while current.value == '*':
                value_0 = current.children[0].value
                value_1 = current.children[1].value
                if value_0 == '0' or (value_0.startswith('0.') and all(char == '0' for char in value_0[2:])):
                    node = Node('0')
                    break
                if value_1 == '0' or (value_1.startswith('0.') and all(char == '0' for char in value_1[2:])):
                    node = Node('0')
                    break
                current = current.children[1]
        if node.value in ['+', '-'] and len(node.children) == 2:
            value_0 = node.children[0].value
            value_1 = node.children[1].value
            if value_0 == '0' or (value_0.startswith('0.') and all(char == '0' for char in value_0[2:])):
                node = node.children[1]
            if value_1 == '0' or (value_1.startswith('0.') and all(char == '0' for char in value_1[2:])):
                node = node.children[0]
        if len(node.children) == 1:
            node.children[0] = self.optimize_tree(node.children[0])
        if len(node.children) == 2:
            node.children[0] = self.optimize_tree(node.children[0])
            node.children[1] = self.optimize_tree(node.children[1])
        return node

    def tree_height(self, node):
        if node is None:
            return 0
        else:
            children_heights = [self.tree_height(child) for child in node.children]
            if not children_heights:
                return 1
            else:
                return max(children_heights) + 1

    def set_ids(self, node):
        if node.is_operator or node.is_function:
            node.id = self.id_counter
            self.id_counter += 1
        for child in node.children:
            self.set_ids(child)
