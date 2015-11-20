'''
for h in range(4,11,2):
	for ra in range(1,5):
		for ta in range(1,11):
			for i in range(1,2):
				fname = str(h)+"_"+str(ra)+"_"+str(ta)+"_"+str(i)
				print "python tcj.py",h,ra,ta," > ",("../input/"+fname)

'''
'''
for h in range(4,11,2):
	for ra in range(1,5):
		for ta in range(1,11):
			for i in range(1,2):
				fname = str(h)+"_"+str(ra)+"_"+str(ta)+"_"+str(i)
				print "echo ",fname
				print "../bin/dijkstra < ../input/%s > ../output/dijkstra_%s" %(fname,fname)

'''

import random
import sys
# '''
h,ra,ta = map(int, sys.argv[2:])
w = h

x = ["-","-","-","*","-"]
p = ["R","T"]
r = []
t = []
g = []
print sys.argv[1]
for i in range(h):
	for j in range(w):
		g.append([i,j])
random.shuffle(g)
random.shuffle(g)
random.shuffle(g)
r = g[:ra]
t = g[ra:ra+ta]

print h, w
for i in range(h):
	s = ""
	for j in range(w):
		if [i,j] in r:
			s+= "R"
		elif [i,j] in t:
			s+= "T"
		else:
			s+= x[random.randint(0,4)]
	print s
# '''
