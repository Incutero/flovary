import ast
from FuncCallVisitor import FuncCallVisitor

class Call(ast.Call):
    
    def __init__(self, node, parent):
        self.node = node
        self.name = self.get_name(node)
        self.parent = parent
        self.children = []

    def get_name(self, node):
        callvisitor = FuncCallVisitor()
        callvisitor.visit(node.func)
        return callvisitor.name

    def add_child(self, child):
        self.children.append(child)

    def traverse(self):
        cur_node = self;
        calls = []
        calls.append(cur_node.name)
        while len(cur_node.children) is not 0:
            cur_node = cur_node.children[0]
            calls.append(cur_node.name)
        return calls
