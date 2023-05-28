import random

import networkx as nx
import matplotlib.pyplot as plt
from random import randrange
import math
class Graph(object):

    countOfNodes = 0
    matrix = []
    newG = nx.DiGraph()

    def __init__(self, countOfNodes):
        self.countOfNodes = countOfNodes
        self.matrix = self.generateGraph(countOfNodes)

    def generateGraph(self,countOfNodes):
        matrix = [[0]*countOfNodes for i in range(countOfNodes)]

        for i in range(0, len(matrix)):
            for j in range(0, len(matrix)):
                if i != j:
                    flag = random.randint(1,2)
                    randInt = random.randint(7,30)
                    if flag == 1:
                        randInt = math.inf
                    matrix[i][j] = randInt
                    matrix[j][i] = matrix[i][j]

        return matrix


    def removeEdge(self, start, end):
        self.matrix[start-1][end-1] = math.inf
        self.matrix[end-1][start-1] = math.inf

    def addEdge(self, start, end, weight):
        if self.matrix[start-1][end-1] == math.inf:
            self.matrix[start-1][end-1] = weight
            self.matrix[end-1][start-1] = weight

    def showGraphMatrix(self):
        strForShowMatrix = "\t"
        for i in range(0, len(self.matrix)):
            strForShowMatrix += "{}\t".format(i+1)
        print(strForShowMatrix)

        for i in range(0, len(self.matrix)):
            str = "\t"
            for j in range(0, len(self.matrix)):
                str += "{}\t".format(self.matrix[i][j])
            print(i+1,str)

    def arg_min(self,T, S):
        amin = -1
        m = math.inf  # максимальное значение
        for i, t in enumerate(T):
            if t < m and i not in S:
                m = t
                amin = i

        return amin

    def visualGraph(self):
        G = nx.DiGraph()
        for i in range(0, len(self.matrix)):
            for j in range(0, len(self.matrix)):
                if i != j and self.matrix[i][j] != math.inf:
                    G.add_edge(i+1, j+1, weight=self.matrix[i][j])
        # Определение позиций узлов
        pos = nx.spring_layout(G)

        # Получение весов ребер
        edge_labels = nx.get_edge_attributes(G, 'weight')

        plt.figure("Изначальный граф")
        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        nx.draw_networkx_labels(G, pos)

        plt.show()

    def deykstra(self, start, end):
        # Визуализация изначального графа
        self.visualGraph()

        N = len(self.matrix)  # число вершин в графе
        T = [math.inf] * N  # последняя строка таблицы

        v = start
        S = {v}  # просмотренные вершины
        T[v] = 0  # нулевой вес для стартовой вершины
        M = [0] * N  # оптимальные связи между вершинами

        while v != -1:
            for j, dw in enumerate(self.matrix[v]):  # перебираем все связанные вершины с вершиной v
                if j not in S:  # если вершина еще не просмотрена
                    w = T[v] + dw  # формируем вес по формуле -> вес вершины + вес дуги
                    if w < T[j]:
                        T[j] = w
                        M[j] = v  # связываем вершину j с вершиной v

            v = self.arg_min(T, S)  # выбираем следующий узел с наименьшим весом
            if v >= 0:  # выбрана очередная вершина
                S.add(v)  # добавляем новую вершину в рассмотрение

        print("Кратчайшие маршруты из {} в остальные вершины\n".format(start+1))
        for i in range (1, len(T)):
            print("В {}: {}".format(i+1, T[i]))


        # формирование оптимального маршрута:
        P = [end]
        while end != start:
            end = M[P[-1]]
            P.append(end)

        for i in range(0, len(P)):
            P[i] += 1
        P = list(reversed(P))

        print("Оптимальный маршрут:",end=" ")
        perfectRoad = "{}".format(P[0])
        for i in range(1,len(P)):
            perfectRoad += " -> {}".format(P[i])
            self.newG.add_edge(P[i-1],P[i],weight=self.matrix[P[i-1]-1][P[i]-1])
        print(perfectRoad)

        # Определение позиций узлов
        pos = nx.spring_layout(self.newG)

        # Получение весов ребер
        edge_labels = nx.get_edge_attributes(self.newG, 'weight')

        plt.figure("Дерево оптимального маршрута")
        nx.draw_networkx_nodes(self.newG, pos)
        nx.draw_networkx_edges(self.newG, pos)
        nx.draw_networkx_edge_labels(self.newG, pos, edge_labels=edge_labels)
        nx.draw_networkx_labels(self.newG, pos)
        plt.show()



с = int(input("Введите кол-во вершин: "))
graph = Graph(с)
graph.showGraphMatrix()
start = int(input("Введите стартвую вершину: ")) - 1
end = int(input("Введите конечную вершину: ")) - 1
if start == end or start < 0 or start > с-1 or end < 0 or end > с-1:
    print("Вершины указаны некорректно")
else:
    graph.deykstra(start, end)

graph.removeEdge(3,5)
graph.removeEdge(1,2)
graph.addEdge(3,4, 20)
graph.showGraphMatrix()
#graph.visualGraph()
