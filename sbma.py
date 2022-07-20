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
        self.real = array[0, n] * t
        self.delta = self.actual - self.real
        self.simcount = 100
    
    def sbma_simulate(self):
        """simulate activities distribution"""
        # start simulate project finish time
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
        pass


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
    sbma = SBMA(kalman.X, 5, 0, period)
    sbma.sbma_simulate()
