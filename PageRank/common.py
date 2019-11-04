import numpy as np


class Graph:
    def __init__(self, edges, ):
        self.__nodes_map = dict(enumerate(sorted(set([n for e in edges for n in e]))))
        self.__size = len(self.__nodes_map)
        self.__M = self.__init_M(edges)

    def __init_M(self, edges):
        adjacency = np.zeros((self.__size, self.__size))
        nodes_map = {iv[1]: iv[0] for iv in dict(enumerate(sorted(set([n for e in edges for n in e])))).items()}
        for sink, source in edges:
            adjacency[nodes_map[sink]][nodes_map[source]] = 1
        return adjacency.T

    def __normalize(self, matrix):
        options = np.count_nonzero(matrix == 1., axis=0)
        options[options == 0] = 1
        return matrix * (1 / options)

    def __damping_factor(self, matrix, damping):
        return damping * self.__normalize(matrix.copy()) + ((1. - damping) / self.__size) * np.ones(
            (self.__size, self.__size))

    def page_rank(self, damping, limit):
        damping_m = self.__damping_factor(self.__M, damping)
        error = np.inf
        prob = (np.zeros((self.__size, 1)) + (1 / self.__size))

        while error > limit:
            old_prob = prob.copy()
            prob = np.dot(damping_m, prob)
            error = ((old_prob - prob) ** 2).mean(axis=None)

        return {self.__nodes_map[i]: v for i, v in enumerate(prob.T[0])}
