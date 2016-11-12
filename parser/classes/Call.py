import ast
from FuncCallVisitor import FuncCallVisitor

class Call(ast.Call):
    
    def __init__(self, node):
        self.node = node
        self.name = self.get_name(node)

    def get_name(self, node):
        callvisitor = FuncCallVisitor()
        callvisitor.visit(node.func)
        return callvisitor.name
