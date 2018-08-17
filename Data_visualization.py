import networkx as nx
import numpy as np
import matplotlib.pylab as plt

# Create a graph
G = nx.Graph()

# distances
D = np.array([(0, 0.3, 0.4, 0.7),
               (0.3, 0, 0.9, 0.2),
               (0.4, 0.9, 0, 0.1),
               (0.7, 0.2, 0.1, 0)
               ])*10

labels = {}
for n in range(len(D)):
    for m in range(len(D)-(n+1)):
        G.add_edge(n,n+m+1)
        labels[ (n,n+m+1) ] = str(D[n][n+m+1])

pos=nx.spring_layout(G)

nx.draw(G, pos)
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels,font_size=30)


plt.show()