import json
import networkx as nx
import matplotlib.pyplot as plt

DATA = '../data/github-follower-graph.json'

with open(DATA, 'r') as f:
    db = json.load(f)

nodes = []
edges = []

for user in db:
    if user['id'] not in nodes:
        nodes.append(user['id'])
    for follower in user['followers']:
        if (follower, user['id']) not in edges:
            edges.append((follower, user['id']))

G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

centrality = nx.eigenvector_centrality(G)
results = {node: centrality[node] for node in centrality}
s = [(k, results[k]) for k in sorted(results, key=results.get, reverse=True)]
for k, v in s:
    print((k, v))
nx.draw_random(G)
plt.show()
