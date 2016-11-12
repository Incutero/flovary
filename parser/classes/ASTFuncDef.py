import ast
from collections import deque
from ast_helper import *
from Call import Call 

class ASTFuncDef(object):

    def __init__(self, node):
        self.name = node.name
        self.calls = self.dfs_walk_get_calls(node)

    def tostr(self):
        print self.name

    def dfs_walk_get_calls(self, node):
        all_calls = []
        todo = deque([node])
        while todo:
            node = todo.popleft()
            if isinstance(node, ast.Call):
                all_calls.append(Call(node))
            child_nodes = iter_child_nodes(node)
            child_nodes.reverse()
            if child_nodes is not None:
                todo.extendleft(child_nodes)
        return all_calls
