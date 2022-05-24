#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np


class KalmanFilter(object):
    def __init__(self, progress, velocity):
        """
        :param progress: original project progress status
        :param velocity: original project velocity status
        """
        self.len = len(progress)
        self.Z = np.zeros((2, self.len))
        self.Z[0, :] = progress
        self.Z[1, :] = velocity
        self.K = np.zeros((1, self.len))
        self.X = np.zeros((2, self.len))
        self.P = np.array([[1., 0.], [0., 1.]])
        self.F = np.array([[1., 1.], [0., 1.]])
        self.U = 0.001
        self.V = 0.002
        self.Q = np.array([[self.U, 0.], [0., self.U]])
        self.R = np.array([[self.V, 0.], [0., self.V]])
        self.E = np.eye(2)

    def filter(self):
        for i in range(1, self.len):
            self.X[:, i] = np.dot(self.F, self.X[:, i - 1])
            self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q
            self.K = np.dot(self.P, np.linalg.inv(self.P + self.R))
            self.X[:, i] = self.X[:, i - 1] + np.dot(self.K, (self.Z[:, i] - self.X[:, i]))
            self.X[0, i] = self.X[0, i - 1] + self.X[1, i]
            self.P = np.dot((self.E - self.K), self.P)


if __name__ == '__main__':
    pass
