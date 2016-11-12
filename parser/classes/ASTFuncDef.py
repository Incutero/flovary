import ast
from collections import deque
from ast_helper import *
from Call import Call 

class ASTFuncDef(object):

    def __init__(self, node):
        self.node = node
        self.name = node.name
        self.calls = self.dfs_walk_get_calls(node)

    def __str__(self):
        print self.name
 
    # Walks through function and returns linkedlist of calls.
    def dfs_walk_get_calls(self, node):
        todo = deque([node])
        latest_calls = None
        first_call = None
        while todo:
            node = todo.popleft()
            if isinstance(node, ast.Call):
                current_call = Call(node, latest_calls)
                if first_call is None:
                    first_call = current_call
                if latest_calls:
                    latest_calls.add_child(current_call)
                latest_calls = current_call
            child_nodes = iter_child_nodes(node)
            child_nodes.reverse()
            if child_nodes is not None:
                todo.extendleft(child_nodes)
        return first_call
