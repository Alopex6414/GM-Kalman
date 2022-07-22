#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import copy

from schedule import Schedule
from kalman import KalmanFilter


class SBMA(object):
    def __init__(self, array, buffer, n, t):
        self.array = array
        self.buffer = buffer
        self.period = t
        self.actual = n
        self.current = array[0, :n]
        self.SLT = np.zeros(10)
        self.SUT = np.zeros(10)
        self.simcount = 100
        self.alpha = 0.1
    
    def sbma_simulate(self):
        """simulate activities distribution"""
        # simulate project
        arr_cost = np.empty(shape=(0, 10))
        for i in range(0, self.simcount):
            # generate schedule
            schedule = Schedule(self.period)
            schedule.gen()
            # kalman filter
            kalman = KalmanFilter(schedule.progress, schedule.velocity)
            kalman.filter()
            # linear interpolation
            time = np.arange(len(kalman.X[0]))
            rate = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            cost = np.interp(rate, kalman.X[0], time)
            arr_cost = np.row_stack((arr_cost, np.array(cost)))
        # calculate control line
        for j in range(0, 10):
            cost = np.empty(shape=(0, self.simcount))
            for i in range(0, self.simcount):
                cost = np.append(cost, arr_cost[i, j])
            cost_sort = np.sort(cost)
            self.SLT[j] = cost_sort[int(self.simcount * self.alpha)]
            self.SUT[j] = cost_sort[int(self.simcount * (1. - self.alpha))]
    
    def sbma_analysis(self):
        """analysis buffer cost"""
        # analysis buffer cost
        time = np.arange(len(self.current))
        rate = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        cost = np.interp(rate, self.current, time)
        n = 0
        for i in range(0, len(cost)):
            if cost[i] == self.actual - 1:
                n = i
                break
        cost = cost[:n]
        # evaluate buffer cost
        n = len(cost) - 1
        if cost[-1] < self.SLT[n]:
            result = 0
        elif cost[-1] < self.SUT[n]:
            result = 1
        else:
            result = 2
        return result


class SBMAC(SBMA):
    def __init__(self, array, buffer, n, t):
        super(SBMAC, self).__init__(array, buffer, n, t)


if __name__ == '__main__':
    period = 15
    # generate schedule
    schedule = Schedule(period)
    schedule.gen()
    # kalman filter
    kalman = KalmanFilter(schedule.progress, schedule.velocity)
    kalman.filter()
    # setup SBMA
    sbma = SBMA(kalman.X, 5, 12, period)
    sbma.sbma_simulate()
    sbma.sbma_analysis()
