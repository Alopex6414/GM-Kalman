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


if __name__ == '__main__':
    pass
