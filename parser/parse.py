import sys, ast
from ast_helper import *
from classes.ASTFuncDef import ASTFuncDef
from classes.FuncCallVisitor import FuncCallVisitor

def construct_function_def_objects(tree):
    func_calls = []
    for node in dfs_walk(tree):
        if isinstance(node, ast.FunctionDef):
           temp = ASTFuncDef(node)
           func_calls.append(temp)
    return func_calls

if __name__ == '__main__':
    file = 'sample.py'
    # file = 'ast_helper.py'
    start = None
    if len(sys.argv) == 3:
        file = sys.argv[1]
        start = sys.argv[2]
    tree = ast.parse(open(file).read())
    x = construct_function_def_objects(tree)
    if start is None:
        print x
    else:
        for function in x:
            if function.name == start:
                print function.name, function.calls
                for call in function.calls:
                    print call.name
