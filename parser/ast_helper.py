import ast
from collections import deque, Sequence
from classes.Call import Call
from classes.For import For
from classes.While import While

# Walks through if statements and returns head of children
def dfs_walk_ifs(node):
    children = []
    while True:
        body = node.body
        children.append(dfs_walk_body(body)) # first if
        if len(node.orelse) == 0:
            break
        elif isinstance(node.orelse[0], ast.If):
            node = node.orelse[0]
        else:
            children.append(dfs_walk_body(node.orelse))
            break
    return flatten(children)

# Walks through body and
def dfs_walk_body(todo):
    todo = deque(todo)
    latest_calls = [Call(None)]
    first_call = None
    while todo:
        node = todo.popleft()
        if isinstance(node, ast.If):
            children = dfs_walk_ifs(node)
            for child in children:
                for latest_call in latest_calls:
                    latest_call.add_child(child)
                    child.add_parent(latest_call)
            latest_calls = [child.get_tails() for child in children]
            latest_calls = flatten(latest_calls)
            child_nodes = None
            if first_call is None:
                first_call = children
        elif isinstance(node, ast.For):
            for_loop = For(node)
            for latest_call in latest_calls:
                latest_call.add_child(for_loop)
                for_loop.add_parent(latest_call)
            latest_calls = [for_loop]
            if first_call is None:
                first_call = for_loop
            child_nodes = None
        elif isinstance(node, ast.While):
            while_loop = While(node)
            for latest_call in latest_calls:
                latest_call.add_child(while_loop)
                while_loop.add_parent(latest_call)
            latest_calls = [while_loop]
            if first_call is None:
                first_call = while_loop
            child_nodes = None
        elif isinstance(node, ast.Call):
            current_call = Call(node)
            for latest_call in latest_calls:
                latest_call.add_child(current_call)
                current_call.add_parent(latest_call)
            latest_calls = [current_call]
            if first_call is None:
                first_call = current_call
            child_nodes = None
        else:
            child_nodes = iter_child_nodes(node)
            child_nodes.reverse()
        if child_nodes is not None:
            todo.extendleft(child_nodes)
    return first_call

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

def flatten(l):
    return sum(map(lambda x: x if isinstance(x, Sequence) else [x], l), [])

def dfs_walk(node):
    todo = deque([node])
    while todo:
        node = todo.popleft()
        child_nodes = iter_child_nodes(node)
        child_nodes.reverse()
        if child_nodes is not None:
            todo.extendleft(child_nodes)
        yield node
