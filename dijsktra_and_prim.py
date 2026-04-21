# quick_demo_jayanagar.py
import heapq
from collections import defaultdict, deque

edges = [
    ('JAYANAGAR','JPNAGAR', 5, 15, 20, 'bus'),
    ('JPNAGAR','JAIN_UNIVERSITY', 6, 18, 25, 'bus'),
    ('JAYANAGAR','NICE_ROAD', 8, 12, 60, 'taxi'),
    ('NICE_ROAD','JAIN_UNIVERSITY', 3, 8, 30, 'taxi'),
]

def build_graph(edges):
    g = defaultdict(list)
    nodes = set()
    for u,v,dist,t,cost,mode in edges:
        g[u].append((v, {'distance':dist,'time':t,'cost':cost,'mode':mode}))
        g[v].append((u, {'distance':dist,'time':t,'cost':cost,'mode':mode}))
        nodes.add(u); nodes.add(v)
    return g, nodes

def dijkstra(g, src, metric):
    dist = {n: float('inf') for n in g}
    prev = {n: None for n in g}
    dist[src]=0
    pq=[(0,src)]
    while pq:
        d,u = heapq.heappop(pq)
        if d>dist[u]: continue
        for v,attrs in g[u]:
            w = attrs[metric]
            nd = d + w
            if nd < dist[v]:
                dist[v]=nd; prev[v]=(u,attrs)
                heapq.heappush(pq,(nd,v))
    return dist, prev

def reconstruct(prev, src, tgt):
    if prev.get(tgt) is None and src!=tgt: return None
    path=[]; cur=tgt
    while cur!=src:
        p = prev[cur]
        if p is None: return None
        path.append((p[0], cur, p[1]))
        cur = p[0]
    path.reverse()
    return path

def prim_mst(g, nodes):
    if not nodes: return [],0
    start = next(iter(nodes))
    visited = {start}
    pq=[]
    for v,attrs in g[start]:
        heapq.heappush(pq,(attrs['cost'], start, v, attrs))
    mst=[]; total=0
    while pq and len(visited)<len(nodes):
        cost,u,v,attrs = heapq.heappop(pq)
        if v in visited: continue
        visited.add(v); mst.append((u,v,attrs)); total+=cost
        for nb,nb_attrs in g[v]:
            if nb not in visited:
                heapq.heappush(pq,(nb_attrs['cost'], v, nb, nb_attrs))
    # complete forest if disconnected
    for node in nodes:
        if node not in visited:
            visited.add(node)
            for v,attrs in g[node]:
                if v not in visited:
                    heapq.heappush(pq,(attrs['cost'], node, v, attrs))
            while pq and len(visited)<len(nodes):
                cost,u,v,attrs = heapq.heappop(pq)
                if v in visited: continue
                visited.add(v); mst.append((u,v,attrs)); total+=cost
                for nb,nb_attrs in g[v]:
                    if nb not in visited:
                        heapq.heappush(pq,(nb_attrs['cost'], v, nb, nb_attrs))
    return mst, total

g, nodes = build_graph(edges)
src = 'JAYANAGAR'; tgt = 'JAIN_UNIVERSITY'

# distance
dist_d, prev_d = dijkstra(g, src, 'distance')
path_d = reconstruct(prev_d, src, tgt)
print("Distance A->B:", dist_d[tgt], "km")
print("Path by distance:", path_d)

# time
dist_t, prev_t = dijkstra(g, src, 'time')
path_t = reconstruct(prev_t, src, tgt)
print("Time A->B:", dist_t[tgt], "min")
print("Path by time:", [(u,v,attrs['mode']) for u,v,attrs in (path_t or [])])

# cost
dist_c, prev_c = dijkstra(g, src, 'cost')
path_c = reconstruct(prev_c, src, tgt)
print("Cost A->B:", dist_c[tgt])
print("Path by cost:", [(u,v,attrs['mode'], attrs['cost']) for u,v,attrs in (path_c or [])])

# Prim MST
mst, total = prim_mst(g, nodes)
print("MST total cost:", total)
print("MST edges:", [(u,v,attrs['mode'],attrs['cost']) for u,v,attrs in mst])
