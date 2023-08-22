# Author: Christian Careaga (christian.careaga7@gmail.com)
# A* Pathfinding in Python (2.7)
# Please give credit if used
# (Modified from original)

from heapq import *
from openrct2 import SEGMENTS

def get_grid_dx(current):
    deltas = [(0,1),(0,-1),(1,0),(-1,0)]
    return [(current[0] + i, current[1] + j) for i, j in deltas]

def astar(start, goal, out_of_bounds_func=None, neighbor_func=None, heuristic=None, eq_func=None):
    closed_set = set() # set of nodes already evaluated
    came_from = {} # set of discovered nodes to be evaluated
    gscore = {start:0} # cost of going from start to start is 0
    fscore = {start:heuristic(start, goal)} # cost from start to goal starts at heuristic estimate
    open_heap = []

    heappush(open_heap, (fscore[start], start)) # add start node to open set along with best guess
    
    ct=0
    while open_heap: # while there are still nodes on the open heap
        ct+=1
        if ct > 2000: break
        current = heappop(open_heap)[1] # get the smallest node in the heap ([1]->node instead of fscore)
                
        if eq_func(current, goal): # if reached goal 
            print("Reached goal:", current.v, goal.v)
            data = []
            while current in came_from: # reconstruct path
                data.append(current)
                current = came_from[current]
            return data # finished

        closed_set.add(current) # add current node to explored set
        neighbors = neighbor_func(current)
        #print("Current:", current.v.pt, current.pieces[-1], len(neighbors))
        for neighbor in neighbors: # for each neighbor of the current node
            if out_of_bounds_func and out_of_bounds_func(neighbor):
                continue

            #tentative_g_score = gscore[current] + heuristic(current, neighbor) # get cost from start node to n
            tentative_g_score = heuristic(current, neighbor) # get cost from start node to n
                        
            if neighbor in closed_set: # and tentative_g_score >= gscore.get(neighbor, 0):
                continue # explored already and we reached it cheaper than current gscore
                
            # https://stackoverflow.com/questions/62531674/speed-up-a-implementation-in-python
            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in fscore: # not in [i[1] for i in open_heap]:
                # we didn't discover this neighbor before or we can get to it cheaper than before
                came_from[neighbor] = current # update the parent list
                gscore[neighbor] = tentative_g_score
                #fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                fscore[neighbor] = heuristic(neighbor, goal)
                #print(ct, "Neighbor:", neighbor.s, fscore[neighbor], neighbor.v.pt, neighbor.pieces[-1], SEGMENTS[neighbor.pieces[-1][0]])
                heappush(open_heap, (fscore[neighbor], neighbor)) # add neighbor to the open set
        #input("done neighbors")
                
    return False # couldn't find a path
