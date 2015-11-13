# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 13:02:55 2015

@author: magusverma
"""

def reached_limit(current, limit):
    for i in range(len(current)):
        if current[i] != limit[i]-1:
            return False
    return True

def increment(current, limit):
    for i in range(len(current)-1,-1,-1):
        if current[i] < limit[i]-1:
            current[i]+=1
            break
        current[i] = 0
