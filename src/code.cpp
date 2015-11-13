# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 21:26:02 2015

@author: magusverma
"""
import math
#n, c = 3, [[0, 0, 1],[ 3 ,1 ,1 ],[6 ,0 ,9]]
n = input()
c = [map(int, raw_input().strip().split()) for _ in range(n)]
visited = [[-1 for i in range(n)] for j in range(n)]

    
def dist(i,j):
    return math.sqrt((c[i][0]-c[j][0])**2 + (c[i][1]-c[j][1])**2)
    
def optTour(n, n_, cu):

    if visited[n][n_] != -1:
        return visited[n][n_]
    
    if n==0:
        cu += c[n][2]
        cu -= dist(n, n_)
        visited[n][n_] = cu
        
    else:
        visited[n][n_] = max([optTour(n-1, n_, cu), optTour(n-1, n, cu+c[n][2]-dist(n, n_))])
    
    return visited[n][n_]

if n == 1:
    print c[0][2]
else:
    print round(optTour(n-2, n-1, c[n-1][2]),6)