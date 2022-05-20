#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np


class Schedule(object):
    def __init__(self, period):
        """
        :param period: please input schedule period
        """
        self.period = period
        self.sigma = 0.01
        self.mu = 1 / period
        self.velocity = self.sigma * np.random.randn(self.period) + self.mu
        self.progress = np.cumsum(self.velocity)


if __name__ == '__main__':
    s = Schedule(15)
    print("velocity:{}", s.velocity)
    plt.figure()
    plt.plot(s.velocity, 'bo')
    plt.plot(s.progress, 'rx--')
    plt.show()
    pass
