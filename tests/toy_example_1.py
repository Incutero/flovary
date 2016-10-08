def Add(x, y):
	return x+y

def Mult(x, y):
	answer = 0
	for i in xrange(y):
		answer = Add(answer, x)
	return answer

def Pow(x, y):
	answer = 1
	for i in xrange(y):
		answer = Mult(answer, x)

def Weird(a, b, c, d):
	s = Add(a,b)
	t = Mult(c,d)
	s = Add(s,t)

