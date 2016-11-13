from ast_helper import *

class ASTFuncDef(object):

    def __init__(self, node):
        self.node = node
        self.name = node.name
        self.calls = self.dfs_walk_get_calls(node)

    def __str__(self):
        print self.name

    # Walks through function and returns linkedlist of calls.
    def dfs_walk_get_calls(self, node):
        return dfs_walk_body([node])


