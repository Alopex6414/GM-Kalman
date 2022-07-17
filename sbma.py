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
        self.LCL = (0.15 + array[0, n] * 0.6) * self.buffer # lower control line
        self.UCL = (0.3 + array[0, n] * 0.6) * self.buffer  # upper control line
    
    def sbma_analysis(self):
        buf_size = self.delta
        if buf_size < self.LCL:
            # opportunity area
            result = 0
        elif buf_size < self.UCL:
            # normal area
            result = 1
        else:
            # dangerous area
            result = 2
        return result


class SBMAC(SBMA):
    X = None
    Count = 0
    Status = dict()
    
    def __init__(self, array, buffer, n, t):
        super(SBMAC, self).__init__(array, buffer, n, t)

    @staticmethod
    def setup_array(array):
        SBMAC.X = copy.deepcopy(array)
        SBMAC.Count = 0
        SBMAC.Status = dict()

    def sbma_analysis(self):
        result = super(SBMAC, self).sbma_analysis()
        if result == 0:
            SBMAC.Status.update({"{}".format(self.actual): {"real": self.real, "actual": self.actual,
                                                            "delta": self.delta, "status": "G", "risk": "low",
                                                            "control": 0}})
        elif result == 1:
            SBMAC.Status.update({"{}".format(self.actual): {"real": self.real, "actual": self.actual,
                                                            "delta": self.delta, "status": "Y", "risk": "medium",
                                                            "control": 1}})
        else:
            SBMAC.Status.update({"{}".format(self.actual): {"real": self.real, "actual": self.actual,
                                                            "delta": self.delta, "status": "R", "risk": "high",
                                                            "control": 1}})
        return result

    def sbma_control(self):
        result = self.sbma_analysis()
        # project buffer consume result
        if result == 0:
            SBMAC.X[1, self.actual] = SBMAC.X[1, self.actual]
        elif result == 1:
            SBMAC.X[1, self.actual] = SBMAC.X[1, self.actual] + \
                                                       0.025 * (1. - self.array[0, self.actual])
            SBMAC.Count = SBMAC.Count + 1
        else:
            SBMAC.X[1, self.actual] = SBMAC.X[1, self.actual] + \
                                                       0.05 * (1. - self.array[0, self.actual])
            SBMAC.Count = SBMAC.Count + 1
        # update current progress
        if self.actual > 0:
            SBMAC.X[0, self.actual] = SBMAC.X[0, self.actual - 1] + \
                                                       SBMAC.X[1, self.actual]
        if SBMAC.X[0, self.actual] > 1.:
            SBMAC.X[0, self.actual] = 1.


if __name__ == '__main__':
    pass
