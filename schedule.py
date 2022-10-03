#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np


class Schedule(object):
    def __init__(self, period, sigma=0.05):
        """
        :param period: schedule period(eg. 15d or 20d)
        :param period: variation coefficient(eg. 0.05)
        """
        self.period = period
        self.sigma = sigma
        self.mu = 1 / period
        self.actual = None
        self.velocity = None
        self.progress = None

    def gen(self):
        """
        :function: generate random normal distribute project schedule
        """
        self.velocity = np.random.normal(self.mu, self.sigma, self.period)
        # velocity should not less than zero
        for i in range(0, len(self.velocity)):
            if self.velocity[i] < 0.:
                self.velocity[i] = 0.
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
        # calculate actual time
        b = False
        for i in range(0, len(self.progress)):
            if self.progress[i] >= 1.:
                b = True
                self.actual = i
                break
        if not b:
            self.actual = len(self.progress)

    def gen_beta(self):
        """
        :function: generate random beta distribute project schedule
        """
        self.velocity = np.random.beta(1, 1, self.period)


if __name__ == '__main__':
    period = 15
    sigma = 1
    number = 1000000
    arr_t = np.random.normal(period, sigma, number)
    arr_v = np.zeros(number)
    for i in range(len(arr_t)):
        if arr_t[i] < 0.01:
            arr_t[i] = 0.01
        arr_v[i] = np.around(1./arr_t[i], 3)
    # arr = np.around(np.random.normal(period, sigma, number), 1)
    # arr = np.sort(arr)
    # dist calc
    dist = dict()
    keys = np.unique(arr_v)
    for k in keys:
        v = arr_v[arr_v == k].size
        dist[k] = v
    # plot figure
    plt.figure()
    plt.plot(dist.keys(), dist.values(), color="lightskyblue", marker="x", linestyle="--", label="Beta")
    plt.legend()
    plt.grid(True)
    plt.xlabel("number")
    plt.ylabel("value")
    plt.title("Beta Distribution")
    plt.show()
    pass
