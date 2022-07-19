#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from asyncio.windows_events import NULL
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
    
    def sbma_simulate(self):
        """simulate activities distribution"""
        # generate schedule
        schedule = Schedule(self.period)
        schedule.gen()
        pass


class SBMAC(SBMA):
    def __init__(self, array, buffer, n, t):
        super(SBMAC, self).__init__(array, buffer, n, t)


if __name__ == '__main__':
    pass
