# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 11:27:30 2015

@author: magusverma
"""

#'''
import random

test_cases = []
for _ in range(4):
    for h in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
        w = h
        for ra in [1,2,3,4,5]:
            for ta in [1,2,3,4,5]:
                for block_percent in [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]:
                    if ra + ta > (w*h):
                        continue
                    if ra + ta > 5:
                        continue
                    g = []
                    for i in range(h):
                        for j in range(w):
                            g.append([i,j])
                    
                    random.shuffle(g)
                    random.shuffle(g)
                    random.shuffle(g)
                    r = g[:ra]
                    t = g[ra:ra+ta]
                    s = ""
                    for i in range(h):
                        for j in range(w):
                            if [i,j] in r:
                                s+= "R"
                            elif [i,j] in t:
                                s+= "T"
                            else:
                                if (random.randint(1,10)/10.0) > block_percent:
                                    s += "-"
                                else:
                                    s += "*"
                        s += "\n"
                    test_cases.append([_,h,w,ra,ta,block_percent,s])

test_cases = sorted(test_cases, key=lambda x:x[1])
#'''

for i, test_case in enumerate(test_cases):
    _,h,w,ra,ta,block_percent,s = test_case
    c = str(i+1) + "\n"
    c += str(h)+ " " +str(w)+"\n"
    c += s
    filename = str(i+1)+"_"+str(h)+"_"+str(w)+"_"+str(ra)+"_"+str(ta)+"_"+str(int(block_percent*100))
    f = open("../random_grid_inputs/"+filename, "w")
    f.write(c)   
    f.close()
