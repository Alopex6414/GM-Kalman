#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np


class Schedule(object):
    def __init__(self, period):
        """
        :param period: please input schedule period
        """
        self.period = period
        self.sigma = 0.05
        self.mu = 1 / period
        self.velocity = None
        self.progress = None

    def gen(self):
        self.velocity = abs(np.random.normal(self.mu, self.sigma, self.period))
        self.progress = np.insert(np.cumsum(self.velocity), 0, 0.0)
        # self.velocity = np.append(self.velocity, 0.0)
        # if progress array has already reached 1.0
        b = False
        index = 0
        for i in range(self.progress.size):
            if self.progress[i] > 1.0:
                if not b:
                    b = True
                    index = i
                self.progress[i] = 1.0
        if b:
            for i in range(index, self.velocity.size):
                self.velocity[i] = 0.0
        # if progress array not reached 1.0
        while self.progress[-1] < 1.0:
            velocity = abs(np.random.normal(self.mu, self.sigma))
            progress = self.progress[-1] + velocity
            if progress > 1.0:
                progress = 1.0
            self.velocity = np.append(self.velocity, velocity)
            self.progress = np.append(self.progress, progress)
        self.velocity = np.append(self.velocity, 0.0)


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
        self.V = 0.005
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
    s = Schedule(15)
    s.gen()
    kf = KalmanFilter(s.progress, s.velocity)
    kf.filter()
    print("progress:", s.progress)
    print("velocity:", s.velocity)
    plt.figure()
    plt.plot(s.progress, 'rx--')
    plt.plot(s.velocity, 'bo')
    plt.plot(kf.X[0, :], 'gx--')
    plt.plot(kf.X[1, :], 'yo')
    plt.show()
    pass
