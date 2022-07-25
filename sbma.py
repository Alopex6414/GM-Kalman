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
        self.current = array[0, n]
        self.SLT = np.zeros(11)
        self.SUT = np.zeros(11)
        self.CL = 0.0
        self.CU = 0.0
        self.CV = 0.0
        self.simcount = 100
        self.alpha = 0.1
    
    def sbma_simulate(self):
        """simulate activities distribution(Simulate)"""
        # simulate project
        arr_cost = np.empty(shape=(0, 11))
        for i in range(0, self.simcount):
            # generate schedule
            schedule = Schedule(self.period)
            schedule.gen()
            # kalman filter
            kalman = KalmanFilter(schedule.progress, schedule.velocity)
            kalman.filter()
            # linear interpolation
            time = np.arange(len(kalman.X[0]))
            rate = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            cost = np.interp(rate, kalman.X[0], time)
            arr_cost = np.row_stack((arr_cost, np.array(cost)))
        # calculate control line
        for j in range(0, 11):
            cost = np.empty(shape=(0, self.simcount))
            for i in range(0, self.simcount):
                cost = np.append(cost, arr_cost[i, j])
            cost_sort = np.sort(cost)
            self.SLT[j] = cost_sort[int(self.simcount * self.alpha)]
            self.SUT[j] = cost_sort[int(self.simcount * (1. - self.alpha))]
    
    def sbma_analysis(self):
        """analysis buffer cost"""
        self.sbma_simulate()
        # analysis buffer cost
        time = np.arange(11)
        current = np.array([self.current])
        rate = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        self.CV = np.interp(current, rate, time)
        self.CL = np.interp(self.CV, time, self.SLT)
        self.UL = np.interp(self.CV, time, self.SUT)
        # evaluate buffer cost
        if self.actual <= self.CL:
            result = 0
        elif self.actual <= self.UL:
            result = 1
        else:
            result = 2
        return result


class SBMAC(SBMA):
    X = None
    Cost = None
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
        SBMAC.Cost = np.empty(shape=(0, 0))
        SBMAC.Count = 0
        SBMAC.Status = dict()
    
    def sbma_analysis(self):
        result = super(SBMAC, self).sbma_analysis()
        SBMAC.Cost = np.append(SBMAC.Cost, self.CV)
        if result == 0:
            SBMAC.Status.update({"{}".format(self.actual): {"CV": self.CV, "CL": self.CL, "CU": self.CU, 
                                                            "status": "L", "risk": "low", "control": 0}})
        elif result == 1:
            SBMAC.Status.update({"{}".format(self.actual): {"CV": self.CV, "CL": self.CL, "CU": self.CU,
                                                            "status": "M", "risk": "medium", "control": 1}})
        else:
            SBMAC.Status.update({"{}".format(self.actual): {"CV": self.CV, "CL": self.CL, "CU": self.CU,
                                                            "status": "U", "risk": "high", "control": 1}})
        return result
    
    def sbma_control(self):
        result = self.sbma_analysis()
        # project buffer consume result
        if result == 0:
            SBMAC.X[1, self.actual] = SBMAC.X[1, self.actual]
        elif result == 1:
            SBMAC.X[1, self.actual] = SBMAC.X[1, self.actual]
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
    # setup array
    SBMAC.setup_array(kalman.X)
    for i in range(len(kalman.X[0])):
        s = SBMAC(kalman.X, 5, i, period)
        s.sbma_control()
    # subplot1 line (Progress)
    x = np.arange(11)
    plt.figure()
    plt.plot(x, s.SUT, color="lightcoral", marker="o", linestyle="--", label="SLT")
    plt.plot(x, s.SLT, color="lightgreen", marker="o", linestyle="--", label="sut")
    plt.legend()
    plt.grid(True)
    plt.xlabel("Progress")
    plt.ylabel("Time")
    plt.title("Project Progress Time Cost")
    plt.show()
