import re

# In python 2.x, all function names are comprised of digits, numbers, and underscores.
test_file = open('../tests/006_ps5_test.py', 'r')
python_code = test_file.read();

# searchObj = re.findall( r'def [a-zA-z0-9_]*\((.*)\):', string, re.M|re.I)
func_sigs = re.findall( r"def [a-zA-Z0-9_]*\(.*\):\n", python_code)

for func_sig in func_sigs:
	params = re.findall( r"(.*)", func_sig)
	print func_sig
	print params



# if searchObj:
#    print "search --> searchObj.group() : ", searchObj.group(0)
#    print "search --> searchObj.group() : ", searchObj.group(1)
# else:
#    print "Nothing found!!"


