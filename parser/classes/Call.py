import ast
from FuncCallVisitor import FuncCallVisitor

class Call(ast.Call):
    
    def __init__(self, node):
        self.node = node
        if node:
            self.name = self.get_name(node)
        else:
            self.name = "start"
        self.parent = [] 
        self.children = []

    def get_name(self, node):
        callvisitor = FuncCallVisitor()
        callvisitor.visit(node.func)
        return callvisitor.name

    def add_child(self, child):
        self.children.append(child)

    def add_parent(self, parent):
        self.parent.append(parent)

    def traverse(self):
        cur_node = self;
        calls = []
        calls.append(cur_node.name)
        while len(cur_node.children) is not 0:
            for node in cur_node.children:
                calls.append(node.traverse())
            cur_node = cur_node.children[0]
        return calls

    def get_tails(self):
        tails = []
        if len(self.children) == 0:
            return self
        for child in self.children:
            tails.append(child.get_tails())
        return tails
