import sys
from heapq import heapify , heappush, heappop 
def permutation(lst):
 
    if len(lst) == 0:
        return []
 
    if len(lst) == 1:
        return [lst]
    l = [] # empty list that will store current permutation
 
    for i in range(len(lst)):
       m = lst[i]

       remLst = lst[:i] + lst[i+1:]
 
       for p in permutation(remLst):
           l.append([m] + p)
    return l
 
def dst(lst , src = (0,0)):
    dist = ((src[0]-lst[0][0])**2+(src[1]-lst[0][1])**2)**0.5
    for i in range(len(lst)-1):
        dist+= ((lst[i][0]-lst[i+1][0])**2+(lst[i][1]-lst[i+1][1])**2)**0.5

    return dist


def graph(lst,src):
    permutation_ = permutation(lst)
    path = []
    src_ = []
    src_.append(src)
    distance_minimum = dst(permutation_[0],src)
    for i in permutation_:
        x = dst(i,src)
        if x < distance_minimum:
            distance_minimum = x
            path = i
    
    return src_ + path


    
"""
def dijkstra(graph,source,destination):
    inf = sys.maxsize
    node_data = {}
    for i in range(5):
        node_data[f"{i}"]={'cost':inf , 'pred':[]}
    
    node_data[source]['cost'] = 0
    visited = []
    temp = source

    for i in range(5):
        if temp not in visited:
            visited.append(temp)
            min_heap = []
            for j in graph[temp]:
                if j not in visited:
                    cost = node_data[temp]['cost']+graph[temp][j]
                    if cost < node_data[j]['cost']:
                        node_data[j]['cost'] = cost
                        node_data[j]['pred']=node_data[temp]['pred']+list(temp)
                    heappush(min_heap,(node_data[j]['cost'],j))
        heapify(min_heap)
        temp=min_heap[0][1]

        return str(node_data[destination]['pred']+list(destination))
"""