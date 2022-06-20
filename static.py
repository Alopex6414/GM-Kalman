#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

from schedule import Schedule
from kalman import KalmanFilter


class StaticPartition(object):
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
        self.green = self.buffer * 1. / 3
        self.yellow = self.buffer * 2. / 3
        self.red = self.buffer
        self.status = dict()

    def static_analysis(self):
        buf_size = self.actual - self.real
        if buf_size < self.green:
            self.status.update({"{}".format(self.actual): "G"})
        elif buf_size < self.yellow:
            self.status.update({"{}".format(self.actual): "Y"})
        else:
            self.status.update({"{}".format(self.actual): "R"})
        print("hello")


if __name__ == '__main__':
    period = 15
    # generate schedule
    schedule = Schedule(period)
    schedule.gen()
    # kalman filter
    kalman = KalmanFilter(schedule.progress, schedule.velocity)
    kalman.filter()
    for i in range(period):
        s = StaticPartition(kalman.X, 5, i, period)
        s.static_analysis()
