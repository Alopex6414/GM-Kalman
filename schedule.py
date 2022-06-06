#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
