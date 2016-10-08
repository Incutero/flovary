# Tests for the following
#	- Functions with n_args > 1, 1, 0
#	- Functions that call no functions
#	- Functions that are called by no functions
# 	- Param types: int, float, dict, arr
test_dict_1 = {"main":  {"params": ["int", "float", "dict"], 
						 "calls": ["foo", "bar", "foobar"], 
			   			 "called_by": []}}, 
			   "foo": 	{"params": ["int", "int", "arr"]},
						"calls": ["bar"], 
						"called_by": ["main"]},
			   "bar": 	{"params": ["int"]},
						"calls": [], 
						"called_by": ["foo", "main"]},
			   "foobar":{"params": []},
						"calls": [], 
						"called_by": ["main"]}}

test_dict_2 = {"main": {"params": ["tuple", "int"], 
						"calls": ["lollerskates", "lollercopter"], 
						"called_by": []}, 
			   "lollerskates": {"params": ["float", "arr"], 
			   					"calls":  ["lollerskates", "lollercopter"], 
			   					"called_by": ["lollerskates", "main"]}, 
			   "lollercopter": {"params": ["int"], 
			   					"calls": ["lollercopter"], 
			   					"called_by": ["lollercopter", "lollerskates"]}}

