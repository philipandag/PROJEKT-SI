
from joblib import load as joblib_load
from sklearn.datasets import fetch_openml, load_digits
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

#mnist = joblib_load("mnist_64.joblib")
mnist = load_digits()
mnist.data = mnist.data * 16

mnist.data = 255 - mnist.data  # Odwróć kolory
mnist.data[mnist.data < 0] = 0  # Zamień wartości ujemne na 0
    
images = mnist['data']
import numpy as np
img = images[0].astype(np.float32) 


tempImg = []
for h in range(8):
    row = []
    for w in range(8):
        row.append(img[h*8+w])
    tempImg.append(row)
img = np.asarray(tempImg)
  
print(tempImg)


import scipy.ndimage
from skimage.segmentation import slic
from scipy.spatial.distance import cdist


superpixels = slic(img,n_segments=25, compactness=0.25, channel_axis=None)
print(superpixels)
sp_indices = np.unique(superpixels)
n_sp = len(sp_indices)  

sp_intensity = np.zeros((n_sp, 1), np.float32)
sp_coord = np.zeros((n_sp, 2), np.float32)  # row, col
for seg in sp_indices:
    mask = superpixels == seg
    sp_intensity[seg-1] = np.mean(img[mask])
    sp_coord[seg-1] = np.array(scipy.ndimage.measurements.center_of_mass(mask))


print(sp_intensity)


sp = superpixels
xlen = len(superpixels)
ylen = len(superpixels[0])
edges = []
def tryAddEdge(xind, yind):
    if xind<xlen and xind >= 0 and yind<ylen and yind >= 0 and sp[xind][yind] != ind:
        if(ind < sp[xind][yind]):
            edges.append( (ind, sp[xind][yind]) )
        else:
            edges.append( (sp[xind][yind], ind) )

for ind in sp_indices:
    for x in range(xlen):
        for y in range(ylen):
            if sp[x][y] == ind:
                tryAddEdge(x+1,y)
                tryAddEdge(x-1,y)
                tryAddEdge(x,y+1)
                tryAddEdge(x, y-1)
                tryAddEdge(x+1,y+1)
                tryAddEdge(x+1, y-1)
                tryAddEdge(x-1, y+1)
                tryAddEdge(x-1, y-1)

#edges = np.asarray(edges) 
#print(edges)              
#edges = np.unique(edges)
#print(edges)


edges = list(set(edges))
edges = np.asarray(edges)
edges = edges-1
print(edges)



G = nx.Graph()

for x in sp_intensity:
    G.add_node(x[0])
    
for E in edges:
    N1 = sp_intensity[E[0]][0]
    N2 = sp_intensity[E[1]][0]
    if N1 != N2:
        G.add_edge(N1, N2)

#G.add_edges_from(edges)
nx.draw_networkx(G)
plt.show()
                

                
