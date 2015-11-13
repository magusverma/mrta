# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 04:26:01 2015

@author: magusverma
"""

inf = 99999999999999999
from Queue import PriorityQueue
from collections import defaultdict
from math import sqrt
import json
from heapq import heappop, heappush

def getProcomputedDistancesFor(grid, target_pos_list):
    height, width = len(grid),len(grid[0])

    #initialize cost grids which needs to be computed
    precomps = { }
    for target in target_pos_list:
        precomps[str(target)] = [[inf for i in range(width)] for j in range(height)]
    
    for t, target in enumerate(target_pos_list):
        # computing smallest distance of each point to target using dijkstra
        q = []
        visited = defaultdict(lambda:False)
        
        heappush(q,(0,str(target)))
        
        while(q):
            #print q.queue
            cost, position  = heappop(q)
            print position, cost
            
            if not visited[position]:
                visited[position] = True
                x,y = json.loads(position)
                
                #print i, x, y
                if precomps[str(target)][x][y] > cost:
                    precomps[str(target)][x][y] = cost
                
                # Expand this state
                for i in range(-1,2):
                    for j in range(-1,2):
                        if (i==0 or j==0):
                            if 0<= x+i < height and 0<= y+j < width and grid[x+i][y+j]:
                                new_pos = str([x+i,y+j])
                                if not visited[new_pos]:
                                    dis = round(sqrt((i*i)+(j*j)),2)
                                    heappush(q,(cost+dis,str(new_pos)))
    return precomps
