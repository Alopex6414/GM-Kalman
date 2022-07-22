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
    X = None
    Count = 0
    Status = dict()
    
    def __init__(self, array, buffer, n, t):
        """
        :param array: project schedule progress status array (numpy array type) (2x2)
        :param buffer: project schedule progress feeding or project buffer
        :param n: project schedule progress status array actual length
        :param t: project schedule progress periodic
        """
        super(SBMAC, self).__init__(array, buffer, n, t)
    
    @staticmethod
    def setup_array(array):
        SBMAC.X = copy.deepcopy(array)
        SBMAC.Count = 0
        SBMAC.Status = dict()
    
    def sbma_analysis(self):
        result = super(SBMAC, self).sbma_analysis()
        if result == 0:
            SBMAC.Status.update({"{}".format(self.actual): {"status": "G", "risk": "low", "control": 0}})
        elif result == 1:
            SBMAC.Status.update({"{}".format(self.actual): {"status": "Y", "risk": "medium", "control": 1}})
        else:
            SBMAC.Status.update({"{}".format(self.actual): {"status": "R", "risk": "high", "control": 1}})
        return result
    
    def sbma_control(self):
        result = self.sbma_analysis()
        # project buffer consume result
        if result == 0:
            SBMAC.X[1, self.actual] = SBMAC.X[1, self.actual]
        elif result == 1:
            SBMAC.X[1, self.actual] = SBMAC.X[1, self.actual] + 0.025 * (1. - self.array[0, self.actual])
            SBMAC.Count = SBMAC.Count + 1
        else:
            SBMAC.X[1, self.actual] = SBMAC.X[1, self.actual] + 0.05 * (1. - self.array[0, self.actual])
            SBMAC.Count = SBMAC.Count + 1
        # update current progress
        if self.actual > 0:
            SBMAC.X[0, self.actual] = SBMAC.X[0, self.actual - 1] + SBMAC.X[1, self.actual]
        if SBMAC.X[0, self.actual] > 1.:
            SBMAC.X[0, self.actual] = 1.


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
