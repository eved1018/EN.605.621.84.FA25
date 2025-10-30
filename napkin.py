

Ford–Fulkerson
function fold_fulkerson(G):
    flow, capacity = {}, {}
    for i in G.adj:
        for j in G.adj[i]:
            f[(i,j)] = 0
    while P := find_augmented_path(G):
        bottleneck = min([G.capacity[(i,j)] for (i,j) in P.edges])
        for (i,j) in P.edges:
            flow[(i,j)] += bottleneck
            flow[(j,i)] -= bottleneck

