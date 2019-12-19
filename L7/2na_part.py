from igraph import *
import matplotlib.pyplot as plt
import argparse
import networkx as nx


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--steps', default=4,type=int,  help='Number of random steps in walktrap')
    parser.add_argument('--histogram', default="Output/histo",  help='src to save histogram')
    parser.add_argument('--graph', default="Output/graph",  help='src to save graph')
    parser.add_argument('--cgraph', default="Output/cgraph",  help='src to save communityGraph')

    args = parser.parse_args()
    steps = args.steps
    histSource = args.histogram
    graphSource = args.graph
    cgraphSource =args.cgraph

    g = Graph.Read_Edgelist("edges.txt", directed=False)


    # Plot del graf size proportional al PageRank
    graphPageRank = g.pagerank()
    prPlot = plot(g, vertex_size = [graphPageRank[i]*500 for i in range(0,len(g.vs))])

    communityGraph = Graph.Erdos_Renyi(20,0.3)
    comGraphPlot = plot(communityGraph, layout = communityGraph.layout_kamada_kawai(),target=cgraphSource+".png")


    wc = g.community_walktrap(steps=steps)
    clusters = wc.as_clustering()
    # get the membership vector
    membership = clusters.membership

    ## Fer el hisograma
    plt.hist(membership,bins=20)
    plt.savefig(histSource)
    plt.close()



    colors = ["Blue","Red","Green","Orange","Yellow","Purple","pink","Cyan"]
    g.vs["color"]=[colors[m] for m in membership]
    plot=plot(g)
    plot.save(graphSource)


    numedges = len(g.es)
    numvertices = len(g.vs)
    diameter = g.get_diameter()
    longDiameter = len(diameter)
    trans = g.transitivity_undirected()
    degreeDis= g.degree_distribution()
    grau = g.degree()

    f = open("Output/data.txt","w")
    f.write("Nombre d'arestes: "+ str(numedges) + "\n")
    f.write("Nombre de vertexs: "+ str(numvertices) + "\n")
    f.write("Longuitud del diàmetre: " + str(longDiameter)+ "\n")
    f.write("Resum de la transitivitat: \n")
    f.write(str(trans))
    f.write("\n Graus de llibertat: \n"+ str(degreeDis))
    f.write("\n Grau per vertex: \n"+ str(grau))
