# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 03:48:00 2015

@author: magusverma
"""
import sys

'''
for input:
1
2 3
T**
RRT

returns:
[[True, False, False], [True, True, True]] [[1, 0], [1, 1]] [[0, 0], [1, 2]]
- Freespace represented by True
- 0 based indexing
- Top Left 0,0
'''
def getProblemInstanceFrom(inputFile):
    print "Running for Test Case File",inputFile
    fileContent = open(inputFile).read().splitlines()
    print fileContent
    print "==> Test Case : %s " % fileContent[0]
    height, width = [int(x) for x in fileContent[1].split(" ")]
    print "==> Grid Size : %d X %d " % (height, width)
    grid = [[y!="*" for y in x] for x in fileContent[2:]]
    if len(grid) != height or len(grid[0]) != width:
        print "wrong height in test case actual dimensions ", len(grid),len(grid[0])
    robots = [[x-2,y] for x in range(2,len(fileContent)) for y in range(len(fileContent[x])) if fileContent[x][y] == "R"]
    targets =  [[x-2,y] for x in range(2,len(fileContent)) for y in range(len(fileContent[x])) if fileContent[x][y] == "T"]
    print "==> NR: %d , NT: %d" %(len(robots), len(targets))
    return grid, robots, targets

