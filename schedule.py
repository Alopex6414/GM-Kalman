#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy
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

    def gen_log_norm(self):
        """
        :function: generate random log normal distribute project schedule
        """
        pass

    def gen_beta(self):
        """
        :function: generate random beta distribute project schedule
        """
        self.velocity = np.random.beta(1, 1, self.period)
        pass


if __name__ == '__main__':
    period = 25
    sigma = 0.1
    number = 1000000
    dist_t = dict()
    dist_v = dict()
    # generate log normal distribution data
    arr_t = np.random.lognormal(np.log(period), sigma, number)
    arr_v = np.around(1/arr_t, 3)
    arr_t = np.around(arr_t, 1)
    # update data to dictionary
    keys = np.unique(arr_t)
    for k in keys:
        v = arr_t[arr_t == k].size
        dist_t[k] = v
    keys = np.unique(arr_v)
    for k in keys:
        v = arr_v[arr_v == k].size
        dist_v[k] = v
    # plot figure(project time cost)
    plt.figure()
    plt.plot(dist_t.keys(), dist_t.values(), color="lightskyblue", marker="x", linestyle="--", label="time")
    plt.legend()
    plt.grid(True)
    plt.xlabel("number")
    plt.ylabel("value")
    plt.title("Project Time Cost Log Normal Distribution")
    plt.show()
    # plot figure(project activities velocity)
    plt.figure()
    plt.plot(dist_v.keys(), dist_v.values(), color="lightcoral", marker="x", linestyle="--", label="velocity")
    plt.legend()
    plt.grid(True)
    plt.xlabel("number")
    plt.ylabel("value")
    plt.title("Project Activities Velocity Log Normal Distribution")
    plt.show()
    pass
