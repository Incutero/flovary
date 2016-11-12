import ast
from astfunc import astfunc
from ast_helper import *

def construct_function_def_objects(tree):
    func_calls = []
    for node in dfs_walk(tree):
        if isinstance(node, ast.FunctionDef):
           temp = astfunc(node)
           func_calls.append(temp)
    return func_calls

if __name__ == '__main__':
    tree = ast.parse(open('sample.py').read())
    ast.dump(tree)
    x = construct_function_def_objects(tree)
