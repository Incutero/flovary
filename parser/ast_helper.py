import ast
from collections import deque
def iter_fields(node):
    """
    Yield a tuple of ``(fieldname, value)`` for each field in ``node._fields``
    that is present on *node*.
    """
    for field in node._fields:
        try:
            yield field, getattr(node, field)
        except AttributeError:
            pass

def iter_child_nodes(node):
    """
    Yield all direct child nodes of *node*, that is, all fields that are nodes
    and all items of fields that are lists of nodes.
    """
    child_nodes = []
    for name, field in iter_fields(node):
        if isinstance(field, ast.AST):
            child_nodes.append(field)
        elif isinstance(field, list):
            for item in field:
                if isinstance(item, ast.AST):
                    child_nodes.append(item)
    return child_nodes

def dfs_walk(node):
    todo = deque([node])
    while todo:
        node = todo.popleft()
        child_nodes = iter_child_nodes(node)
        child_nodes.reverse()
        if child_nodes is not None:
            todo.extendleft(child_nodes)
        yield node
