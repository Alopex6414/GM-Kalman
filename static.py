#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
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
        self.delta = self.actual - self.real
        self.green = self.buffer * 1. / 3
        self.yellow = self.buffer * 2. / 3
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


class StaticPartitionControl(StaticPartition):
    Status = dict()

    def __init__(self, array, buffer, n, t):
        """
        :param array: project schedule progress status array (numpy array type) (2x2)
        :param buffer: project schedule progress feeding or project buffer
        :param n: project schedule progress status array actual length
        :param t: project schedule progress periodic
        """
        super(StaticPartitionControl, self).__init__(array, buffer, n, t)

    def static_analysis(self):
        result = super(StaticPartitionControl, self).static_analysis()
        if result == 0:
            StaticPartitionControl.Status.update({"{}".format(self.actual): {"real": self.real, "actual": self.actual,
                                                                             "delta": self.delta, "status": "G"}})
        elif result == 1:
            StaticPartitionControl.Status.update({"{}".format(self.actual): {"real": self.real, "actual": self.actual,
                                                                             "delta": self.delta, "status": "Y"}})
        else:
            StaticPartitionControl.Status.update({"{}".format(self.actual): {"real": self.real, "actual": self.actual,
                                                                             "delta": self.delta, "status": "R"}})
        print(result)


if __name__ == '__main__':
    period = 15
    # generate schedule
    schedule = Schedule(period)
    schedule.gen()
    # kalman filter
    kalman = KalmanFilter(schedule.progress, schedule.velocity)
    kalman.filter()
    for i in range(len(kalman.X[0])):
        s = StaticPartitionControl(kalman.X, 5, i, period)
        s.static_analysis()
    # subplot line
    x = np.arange(len(s.array[0]))
    plt.figure()
    plt.plot(x, s.array[0], color="lightskyblue", marker="o", linestyle="--", label="Actual Progress")
    plt.legend()
    plt.grid(True)
    plt.xlabel("Time")
    plt.ylabel("Progress")
    plt.title("Project Progress Status")
    # plt.savefig("./figure/deviation.png")
    plt.show()
