import ast
import ast_helper


class For(ast.For):
    
    def __init__(self, node):
        self.node = node
        self.body = ast_helper.dfs_walk_body(node.body)
        self.parent = [] 
        self.children = []
        self.name = 'For Loop', self.body

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
            break
        return calls

    def get_tails(self):
        tails = []
        if len(self.children) == 0:
            return self
        for child in self.children:
            tails.append(child.get_tails())
        return ast_helper.flatten(tails)
