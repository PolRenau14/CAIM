from igraph import *
import matplotlib.pyplot as plt

# 1era part
points = 15
separation = 4/points
probabilities = []
var = 0
for i in range(0, points+1):
    probabilities.insert(0,10**-var)
    var += separation
	
watts = Graph.Watts_Strogatz(1, 1000, 4, 0)
L0 = watts.average_path_length(unconn=True)
C0 = watts.transitivity_undirected()
L = []
C = []
for i in range(0, points+1):
    watts = Graph.Watts_Strogatz(1, 1000, 4, probabilities[i])
    L.append(watts.average_path_length(unconn=True)/L0)
    C.append(watts.transitivity_undirected()/C0)
    
plt.plot(probabilities, C, 's', probabilities, L, 'o')
plt.xlabel('Probability')
plt.xscale('log')
#plt.savefig('plot_task_1.png', bbox_inches='tight')
plt.show()
