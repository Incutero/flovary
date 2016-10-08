import re
import networkx as nx
import matplotlib.pyplot as plt

def get_name(function_signature): # Get function name
	name = re.findall( r'def ([a-zA-z0-9_]*)', function_signature, re.M|re.I)
	return name[0]

def get_parameters(function_signature):	# Get function parameters
	list_params = re.findall( r'def [a-zA-z0-9_]*\((.*)\):', function_signature, re.M|re.I)
	params = list_params[0].split(",")
	params = [p.strip() for p in params]
	return params

def get_body(code, line_num):
	first_line = code[line_num]
	spaces = len(first_line) - len(first_line.lstrip())

	curr_line_num = line_num + 1
	curr_line = code[curr_line_num]
	curr_spaces = len(curr_line) - len(curr_line.lstrip())

	while curr_spaces > spaces and curr_line_num < len(code):
		curr_line_num += 1
		if (curr_line_num < len(code)):
			curr_line = code[curr_line_num]
			curr_spaces = len(curr_line) - len(curr_line.lstrip())
		else:
			pass		
	final_line_num = curr_line_num
	code_as_list = code[line_num:final_line_num]
	code_as_string = "".join(code_as_list)
	return code_as_string

def get_functions_in_body(f):
	for line in f.body:
		func_sig = re.findall( r"def [a-zA-Z0-9_]*\(.*\):\n", line)

class Function(object):

	def __init__(self, name, params, body):
		self.name = name
		self.params = params
		self.body = body

	def __str__(self):
		return "Function %s has parameters: %s \nFunction Body \n %s" % (self.name, self.params, self.body)

class FunctionNode(object):

	def __init__(self, function):
		self.function = function
		self.children = None





# file_name = '../tests/toy_example_1.py'
# file_name = '../tests/sp14_006_ps4_folder_test/decimal.py'
# file_name = '../tests/006_ps5_test.py'
# file_name = '../tests/006_ps4_test.py'
# file_name  = '../tests/k_cookies_n_gen_incr.py'
# file_name = 'data_thing_constructor.py'

functions = []

# In python 2.x, all function names are comprised of digits, numbers, and underscores.
python_file =  open(file_name, 'r')
python_code = python_file.readlines()

all_func_names = []

for i in xrange(len(python_code)):
	func_sig  = re.findall( r"def [a-zA-Z0-9_]*\(.*\):\n", python_code[i])
	if func_sig:
		func_name = get_name(func_sig[0])
		func_params = get_parameters(func_sig[0])
		func_body = get_body(python_code, i)
		functions.append( Function(func_name, func_params, func_body) )
		all_func_names.append( func_name )

G = nx.DiGraph()

directed_edges = []
for func in functions:
	for func_name in all_func_names:
		if func_name in func.body and func_name != func.name:
			print "%s is called by %s" % (func_name, func.name)
			directed_edges.append((func.name, func_name))

G.add_edges_from(directed_edges)
values = ['white' for node in G.nodes()]
labels={}

# node_labels = [name.strip('_') for name in G.nodes()]
node_labels = [name for name in G.nodes()]
for i in xrange(len(G.nodes())):
	# labels[G.nodes()[i]]=r'$%s$' % (G.nodes()[i])
	labels[G.nodes()[i]] = r'%s' %(node_labels[i])
pos = nx.spring_layout(G)

nx.draw_networkx_nodes (G, pos, node_color = values, node_size = 1500, alpha = 0.5)
nx.draw_networkx_edges (G, pos, edgelist=G.edges(), edge_color='black', width=2, arrows=True)
nx.draw_networkx_labels(G, pos, labels, font_size=16)

plt.show()

