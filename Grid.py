#coding=utf-8Ы
import networkx as nx
import matplotlib.pyplot as plt


#pass
#numrow = 5
#numcol = 10

# Процедура создания сеточного графа
# numrow - количнство рядов, numcol - колонок
# obstacles - список препятсвий. Стиреть узлы
def CreateGridGraph(numrow, numcol, obstacles):
    G = nx.Graph() # 0 - 1 -2 ... 9
    # Добавляем вершины графа сетки
    for row in range(numrow):
        for col in range(numcol):
            G.add_node((row,col))
        for col in range(numcol-1):
            G.add_edge((row, col),(row,col+1))
    for row in range(numrow-1):
        for col in range(numcol):
            G.add_edge((row, col),(row+1,col))
        for col in range(numcol-1):
            G.add_edge((row, col),(row+1,col+1))
            G.add_edge((row, col+1),(row+1,col))
    for r,c in obstacles:
        G.remove_node((r,c))
    return G

#print G.nodes

# Прорисовка сетки
def PlotGrid(G):
    for v in G.nodes:
        r, c = v
        #plt.scatter([c],[r],300, c ='k', marker=r'$\clubsuit$')
        plt.scatter([c], [r], 500, c='k', marker='o')
    for e in G.edges:
        v1,v2 = e
        r1,c1 = v1
        r2,c2 = v2
        plt.plot([c1,c2],[r1,r2],'k')
    plt.plot([1,1,1],[1,2,3],'b',linewidth=10, solid_capstyle='round')
    plt.show()

# Прорисовка трассы
def PlotTrace(G,trace):
    for v in G.nodes:
        r, c = v
        plt.scatter([c],[r])
    x = []
    y =[]
    for row, col in trace:
        x.append(col)
        y.append(row)

    plt.plot(x, y, color='black')
    plt.show()

#G= CreateGridGraph(5,10)
#PlotGrid(G)
#def L(n):
#    return  [(n,y,x)for y in range(2) for x in range(3)]

#t = [(0,0,0),(0,0,1),(0,0,2), (0,1,0),(0,1,1),(0,1,2), (1,0,0),(1,0,1),(1,0,2), (1,1,0),(1,1,1),(1,1,2),'res']
#t2 = [(n,y,x)for n in range(2) for y in range(2) for x in range(3)]+['res']
#t2 = [(0,y,x)for y in range(2) for x in range(3)]+[(1,y,x)for y in range(2) for x in range(3)]+['res']
#t2 = L(0)+L(1)+['res']
#print t
#print t2
