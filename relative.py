#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import copy

from schedule import Schedule
from kalman import KalmanFilter


class RelativePartition(object):
    def __init__(self, array, buffer, n, t):
        """
        :param array: project schedule progress status array (numpy array type) (2x2)
        :param buffer: project schedule progress feeding or project buffer
        :param n: project schedule progress status array actual length
        :param t: project schedule progress periodic
        """
        self.array = array
        self.buffer = buffer
        self.period = t
        self.actual = n
        self.real = array[0, n] * t
        self.delta = self.actual - self.real
        self.green = self.buffer * 0.15 + array[0, n] * (0.75 - 0.15)
        self.yellow = self.buffer * 0.3 + array[0, n] * (0.9 - 0.3)
        self.red = self.buffer
        self.status = dict()

    def static_analysis(self):
        buf_size = self.actual - self.real
        if buf_size < self.green:
            result = 0
        elif buf_size < self.yellow:
            result = 1
        else:
            result = 2
        return result


class RelativePartitionControl(RelativePartition):
    Status = dict()
    X = None

    def __init__(self, array, buffer, n, t):
        """
        :param array: project schedule progress status array (numpy array type) (2x2)
        :param buffer: project schedule progress feeding or project buffer
        :param n: project schedule progress status array actual length
        :param t: project schedule progress periodic
        """
        super(RelativePartitionControl, self).__init__(array, buffer, n, t)

    @staticmethod
    def setup_array(array):
        RelativePartitionControl.X = copy.deepcopy(array)


if __name__ == '__main__':
    pass
