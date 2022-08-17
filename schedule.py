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

    def gen_log_normal(self):
        """
        :function: generate random log normal distribute project schedule
        """
        self.velocity = np.random.lognormal(self.mu, self.sigma, self.period) - 1
        print(self.velocity)
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
            velocity = abs(np.random.lognormal(self.mu, self.sigma))
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


if __name__ == '__main__':
    period = 15
    times = 10000
    arr_period = np.empty(shape=(0, 0))
    dist_period = dict()
    # generate schedule
    for i in range(0, times):
        schedule = Schedule(period, sigma=0.05)
        schedule.gen()
        # schedule.gen_log_normal()
        arr_period = np.append(arr_period, len(schedule.progress) - 1)
    # statistic distribution
    keys = np.unique(arr_period)
    for k in keys:
        v = arr_period[arr_period == k].size
        dist_period[k] = v
    # plot picture
    plt.figure()
    plt.plot(dist_period.keys(), dist_period.values(), marker="o", linestyle="--", color="lightcoral",
             label="Schedule Distribution")
    plt.legend()
    plt.grid(True)
    plt.xlabel("Time")
    plt.ylabel("Number")
    plt.title("Schedule Distribution")
    plt.show()
