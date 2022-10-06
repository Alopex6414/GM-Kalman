#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy
import numpy as np


class Schedule(object):
    def __init__(self, period, sigma=0.05):
        """
        :param period: schedule period(eg. 15d or 20d)
        :param sigma: variation coefficient(eg. 0.05)
        """
        self.period = period
        self.sigma = sigma
        self.mu = 1 / period
        self.actual = None
        self.velocity = None
        self.progress = None
        self.upper = None
        self.lower = None

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

    def gen_log_norm(self, upper, lower):
        """
        :function: generate random log normal distribute project schedule
        :param upper: optimistic period (eg. 20d if most possible time is 15d)
        :param lower: pessimistic period (eg. 10d if most possible time is 15d)
        """
        self.upper = upper
        self.lower = lower
        self.velocity = np.empty(shape=(0, 0))
        velocity = np.reciprocal(np.random.lognormal(np.log(self.period), self.sigma, self.period))
        # velocity should be restricted when sigma is large...
        for i in range(0, len(velocity)):
            if 1./upper <= velocity[i] <= 1./lower:
                self.velocity = np.append(self.velocity, velocity[i])
        self.progress = np.insert(np.cumsum(self.velocity), 0, 0.0)
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
            velocity = np.reciprocal(np.random.lognormal(np.log(self.period), self.sigma))
            # velocity should be restricted when sigma is large...
            if velocity < 1. / upper or velocity > 1. / lower:
                continue
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
        pass


if __name__ == '__main__':
    period = 25
    sigma = 0.3
    upper = 40
    lower = 10
    number = 10000
    arr_t = np.empty(shape=(0, 0))
    arr_v = np.empty(shape=(0, 0))
    dist_t = dict()
    dist_v = dict()
    # generate log normal distribution data
    arr = np.random.lognormal(np.log(period), sigma, number)
    for i in range(0, len(arr)):
        if lower < arr[i] < upper:
            arr_t = np.append(arr_t, arr[i])
    arr_v = np.around(np.reciprocal(arr_t), 3)
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
