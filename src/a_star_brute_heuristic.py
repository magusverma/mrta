import random
import sys
from Queue import PriorityQueue
from collections import defaultdict
from math import sqrt
from itertools import permutations
from heapq import heappop, heappush
from collections import defaultdict
import time
import sys
import resource
connectedness = 5
height, width = 10,10
inf = 99999999999

def blocked(i,j):
    global grid
    return grid[i][j] == "*"

def get_grid(side_size, num_of_robots, num_of_targets, grid_poss, robot_target):
    h, w, ra, ta = side_size, side_size, num_of_robots, num_of_targets
    x,p  = grid_poss, robot_target
    r = []
    t = []
    g = []
    
    for i in range(h):
    	for j in range(w):
    		g.append([i,j])
    
    random.shuffle(g)
    r = g[:ra]
    t = g[ra:ra+ta]
    
    grid = []
    s = ""
    print h, w
    for i in range(h):
        grid.append([])
        for j in range(w):
            if [i,j] in r:
                s+= "R"
                grid[-1].append("R")
            elif [i,j] in t:
                s+= "T"
                grid[-1].append("T")
            else:
                c = x[random.randint(0,len(x)-1)]
                s+= c
                grid[-1].append(c)
        s += "\n"
    print s
    print 
    return grid, r, t

def getY(p, n):
    return p%n

def getX(p, n):
    return (( p - getY(p, n))/n);

def getP(i, j, n):
    return (i*n)+j;

def precompute_target_distances(grid, target_pos_list):
    grid_size = len(grid)
    #initialize cost grids which needs to be computed
    precomps = { }
    for k in range(len(target_pos_list)):
        precomps[k] = [[inf for i in range(grid_size)] for j in range(grid_size)]
    
    for t, target in enumerate(target_pos_list):
        # computing smallest distance of each point to target using dijkstra
        q = PriorityQueue()
        visited = defaultdict(lambda:False)
        
        c = getP(target[0], target[1], grid_size)
        q.put([c,0], 0)
        
        while(not q.empty()):
            #print q.queue
            position, cost = q.get()
            
            if not visited[position]:
                visited[position] = True
                x,y = getX(position, grid_size), getY(position, grid_size)
                #print i, x, y
                if precomps[t][x][y] > cost:
                    precomps[t][x][y] = cost
                
                # Expand this state
                for i in range(-1,2):
                    for j in range(-1,2):
                        if (i==0 or j==0):
                            if 0<= x+i < grid_size and 0<= y+j < grid_size and grid[x+i][y+j] != "*":
                                new_pos = getP(x+i, y+j, grid_size)
                                if not visited[new_pos]:
                                    dis = round(sqrt((i*i)+(j*j)),2)
                                    q.put([new_pos,cost+dis], cost+dis)
    return precomps

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


def get_all_allocation_combination(robot_pos_list, target_pos_list):
    # i'th target is allocated to which value robot
    base = [0 for i in range(len(target_pos_list))]
    limit = [len(robot_pos_list) for i in range(len(target_pos_list))]
    allocations = []
    while(True):
        allocations.append([[] for i in range(len(robot_pos_list))])
        for target, robot in enumerate(base):
            allocations[-1][robot].append(target)
        if reached_limit(base, limit):
            break
        increment(base, limit)
    return allocations
    
def get_tsp_cost(robot, targets, target_pos_list, precomputed_distances, show_best = False):
    if len(targets) == 0:
        return 0
    possible_visit_orders = list(permutations(targets,len(targets)))
    best_cost = inf
    best_combin = []
    for order in possible_visit_orders:
        order_cost = precomputed_distances[order[0]][robot[0]][robot[1]]
        for i,v in enumerate(order):
            if i!=0:
                # to go from target i-1 to target i
                order_cost += precomputed_distances[order[i]][target_pos_list[order[i-1]][0]][target_pos_list[order[i-1]][1]]
        if order_cost < best_cost:
            best_cost = order_cost
            best_combin = order
   # if show_best:
    if best_cost ==0:
        print "For Robot at", robot, " with allocs ", targets, " best tsp order : ", best_combin, " , cost = ", best_cost
    return best_cost

def get_best_allocation_cost(allocations, robot_pos_list, target_pos_list, precomputed_distances, show_best = False):
    best_alloc_cost, best_alloc = inf, []
    for allocation in allocations:
        alloc_cost = 0
        for i, robot in enumerate(robot_pos_list):
            alloc_cost += get_tsp_cost(robot, allocation[i], target_pos_list, precomputed_distances, show_best= False)
        if alloc_cost < best_alloc_cost:
            best_alloc_cost, best_alloc = alloc_cost, allocation
    #if show_best:
    #print "Best Allocation : ", best_alloc, ", with cost:", best_alloc_cost
    for r in range(len(best_alloc)):
        for t in range(len(best_alloc[r])):
            best_alloc[r][t] = target_pos_list[best_alloc[r][t]]
    return [best_alloc_cost,best_alloc]
    
'''
grid, robot_pos_list, target_pos_list = get_grid(grid_size,robots, targets,["-","-","*"],["R","T"])
print "Robots:"
for i, v in enumerate(robot_pos_list):
    print i, ":", v,"  ",
print

print "Targets:"
for i, v in enumerate(target_pos_list):
    print i, ":", v,"  ",
print
print 
'''

'''
precomputed_distances = precompute_target_distances(grid, target_pos_list)
allocations = get_all_allocation_combination(robot_pos_list, target_pos_list)
print get_best_allocation_cost(allocations, robot_pos_list, target_pos_list, precomputed_distances, show_best= True)
'''

def get_best_allocation_cost_heuristic(robot_pos_list, target_pos_list, show = False):
    global precomputed_distances
    # precomputed_distances must be computed 
    if len(precomputed_distances.keys()) < len(targets):
        print "Precomputation of distance needs to be done for this heuristic"
        return
    allocations = get_all_allocation_combination(robot_pos_list, target_pos_list)
    return get_best_allocation_cost(allocations, robot_pos_list, target_pos_list, precomputed_distances, show_best = show)

class state:
    def __init__(self, robots__, picked__=None,parent__=None):
        self.robots = robots__
        # Example : {'[4, 5]': [False, None], '[6, 7]': [True, None]}
        if picked__ is None:
            global targets
            self.picked = {str(i): [False,None] for i in targets}
        else:
            self.picked = picked__
        self.parent = parent__
        self.alloc = None
    
    def setAllocation(self,alloc):
        self.alloc = alloc
        
    def getPendingTargets(self):
        global targets
        pending = []
        for target in targets:
            if not self.picked[str(target)][0]:
                pending.append(target)
        return pending
            
    def isValidState(self):
        robos = [str(i) for i in self.robots]
        if len(robos) != len(set(robos)):
            #two robots on same grid cell
            return False
            
        for robo in self.robots:
            if (not(0<=robo[0]<height)) or (not(0<=robo[1]<width)):
                #outside grid
                return False
            if blocked(robo[0],robo[1]):
                # robot standing on a blocked cell
                return False
                
        return True
    
    def isGoalState(self):
        return reduce(lambda x, y: x and y, [k[0] for k in self.picked.values()])
        
    def transition(self, action):
        global connectedness
        
        move_map = {}
        if connectedness == 5:
            move_map[0] = [-1,0]
            move_map[1] = [0,-1]
            move_map[2] = [0,0]
            move_map[3] = [0,1]
            move_map[4] = [1,0]
            
        robots_ = [[j for j in i] for i in self.robots]
        picked_ = self.picked.copy()
        parent_ = self
        
        # move robots to new grid cells as per actions
        for i,move in enumerate(action):
            robots_[i][0] = robots_[i][0] + move_map[move][0]
            robots_[i][1] = robots_[i][1] + move_map[move][1]
        
        #print robots_, self.robots
        # pick newly found targets
        for i,robo in enumerate(robots_):
            if str(robo) in picked_.keys() and not picked_[str(robo)][0] :
                picked_[str(robo)] = [True,i]
        
        s_ = state(robots_,picked_,parent_) 
        
        #print "R:",s_.robots,self.robots
        
        return s_
                
    def getNeighbourStates(self):
        global connectedness
        
        neighbours = []
        
        moveCombinations = []
        
        base = [0 for i in range(len(self.robots))]
        limit = [connectedness for i in range(len(self.robots))]
        while(True):
            moveCombinations.append(base[:])
            if reached_limit(base, limit):
                break
            increment(base, limit)
            
        for move in moveCombinations:
            state = self.transition(move)
            if state.isValidState():
                neighbours.append(state)
        
        return neighbours
    
    def getDistance(self, other):
        distance = 0
        for i in range(len(self.robots)):
            for j in range(len(self.robots[i])):
                distance += sqrt(pow(self.robots[i][j] - other.robots[i][j],2))
        return distance
        
    def getRep(self):
        rep = ""
        for i in self.robots:
            rep += str(i)
        for i in self.picked.values():
            rep += str(i[0])[0]
        return rep

mem = 0
def ucs(start):
    visited = defaultdict(lambda: [False,-1])
    heap = []

    mem = 0
    start_time = time.time()
    states_expanded = 0
    
    heappush(heap,(0,start))
    while(heap):
        top = heappop(heap)
        current_state = top[1]
        cost = top[0]
        
        time_spent = time.time() - start_time
        mem = max(mem, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024*1024))

        if current_state.isGoalState():
            ans = cost
            if current_state.parent is not None:
                ans += visited[current_state.parent.getRep()][1]

            print "==>", ans, states_expanded,time_spent,mem," MB" 
            return current_state

        '''

        memory=max(memory,(long long)getMemoryUsage()/1024);
        clock_t end = clock();
        double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
        if(memory/1024 > 500){
            cout<<cost<<" "<<states_expanded<<" "<<time_spent<<" "<<memory<<" KB OOM\n";
            return make_pair(current_state, cost);
        }
        if(time_spent>2){
            cout<<cost<<" "<<states_expanded<<" "<<time_spent<<" "<<memory<<" KB TLE\n";
            return make_pair(current_state, cost);
        }
        '''
        # mem check 
        # time check
        if time_spent > 60:
            # more than 100 secs elapsed
            print "==>",-1, states_expanded,time_spent,mem," MB TLE" 
            return current_state

        if mem > 1000:
            # more than 1000 megs used
            print "==>",-1, states_expanded,time_spent,mem," MB OOM" 
            return current_state
            
        elif not visited[current_state.getRep()][0]: 
            visited[current_state.getRep()][0] = True
            visited[current_state.getRep()][1] = cost
            if current_state.parent is not None:
                visited[current_state.getRep()][1] += visited[current_state.parent.getRep()][1]
            states_expanded += 1
            
            neighbours = current_state.getNeighbourStates()
            for neighbour in neighbours:
                g = current_state.getDistance(start)
                #if current_state.parent is not None:
                #    g += visited[current_state.parent.getRep()][1]
                h = get_best_allocation_cost_heuristic(neighbour.robots, neighbour.getPendingTargets())
                print "heuristic:",g,h[0]
                if h[0]<2:
                    print current_state.robots, current_state.picked,h[1]
                f = g+4*h[0]
                neighbour.setAllocation(h[1])
                heappush(heap,(f,neighbour,h[1]))
    return start;

grid_size = 500
height, width = grid_size,grid_size
robots = 2
targets = 2

def takeInput():
    test_case = input()
    print "==> Test Case : %d " % test_case
    global height, width, grid_size

    height, width = map(int, raw_input().strip().split())
    print height, width 
    print "==> Grid Size : %d X %d " % (height, width)
    grid = []
    for i in range(height):
        grid.append([x for x in raw_input().strip()])
    print grid
    #print grid
    robot_pos_list = []
    target_pos_list = []
    for i in range(height):
        for j in range(width):
            if grid[i][j] == "R":
                robot_pos_list.append([i,j])
            if grid[i][j] == "T":
                target_pos_list.append([i,j])
    print "==> NR: %d , NT: %d" %(len(robot_pos_list), len(target_pos_list))
    return grid, robot_pos_list, target_pos_list

#grid, robot_pos_list, target_pos_list = get_grid(grid_size,robots, targets,["-","-","*"],["R","T"])
grid, robot_pos_list, target_pos_list = takeInput()
targets = target_pos_list
precomputed_distances = precompute_target_distances(grid, target_pos_list)
s = state(robot_pos_list)
g = ucs(s)
soln = [g]
while(soln[-1] != None):
    soln.append(soln[-1].parent)
soln = soln[::-1][1:]

init = None
'''
for state in soln:
    if init is None:
        init = state.alloc
    else:
        for r in range(len(init)):
            for t in state.alloc[r]:
                if t not in init[r]:
                    print "==> ALLOCATION CHANGED"
    print state.robots, state.picked, state.alloc
'''

'''

n = s.getNeighbourStates()
print
for i in n:
    print s.robots,i.robots, s.getDistance(i)
'''