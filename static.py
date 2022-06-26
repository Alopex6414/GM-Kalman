#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import copy

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
    X = None

    def __init__(self, array, buffer, n, t):
        """
        :param array: project schedule progress status array (numpy array type) (2x2)
        :param buffer: project schedule progress feeding or project buffer
        :param n: project schedule progress status array actual length
        :param t: project schedule progress periodic
        """
        super(StaticPartitionControl, self).__init__(array, buffer, n, t)

    @staticmethod
    def setup_array(array):
        StaticPartitionControl.X = copy.deepcopy(array)

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

    def static_control(self):
        result = super(StaticPartitionControl, self).static_analysis()
        # project buffer consume result
        if result == 0:
            StaticPartitionControl.X[1, self.actual] = StaticPartitionControl.X[1, self.actual]
        elif result == 1:
            StaticPartitionControl.X[1, self.actual] = StaticPartitionControl.X[1, self.actual] + 0.05 * (1. - self.array[0, self.actual])
        else:
            StaticPartitionControl.X[1, self.actual] = StaticPartitionControl.X[1, self.actual] + 0.075 * (1. - self.array[0, self.actual])
        # update current progress
        if self.actual > 0:
            StaticPartitionControl.X[0, self.actual] = StaticPartitionControl.X[0, self.actual - 1] + StaticPartitionControl.X[1, self.actual]
        if StaticPartitionControl.X[0, self.actual] > 1.:
            StaticPartitionControl.X[0, self.actual] = 1.


if __name__ == '__main__':
    period = 15
    # generate schedule
    schedule = Schedule(period)
    schedule.gen()
    # kalman filter
    kalman = KalmanFilter(schedule.progress, schedule.velocity)
    kalman.filter()
    # setup array
    StaticPartitionControl.setup_array(kalman.X)
    for i in range(len(kalman.X[0])):
        s = StaticPartitionControl(kalman.X, 5, i, period)
        s.static_analysis()
        s.static_control()
    # static safe buffer progress
    green = np.zeros(len(kalman.X[0]))
    yellow = np.zeros(len(kalman.X[0]))
    red = np.zeros(len(kalman.X[0]))
    for i in range(len(kalman.X[0])):
        # green buffer
        green[i] = i * 1. / (s.period + s.green)
        if green[i] > 1.:
            green[i] = 1.
        # yellow buffer
        yellow[i] = i * 1. / (s.period + s.yellow)
        if yellow[i] > 1.:
            yellow[i] = 1.
        # red buffer
        red[i] = i * 1. / (s.period + s.red)
        if red[i] > 1.:
            red[i] = 1.
    # static safe buffer consume
    buf_G = np.zeros(len(kalman.X[0]))
    buf_Y = np.zeros(len(kalman.X[0]))
    buf_R = np.zeros(len(kalman.X[0]))
    status = np.zeros(len(kalman.X[0]))
    for i in range(len(kalman.X[0])):
        buf_G[i] = s.green
        buf_Y[i] = s.yellow
        buf_R[i] = s.red
        status[i] = s.Status.get("{}".format(i))["delta"]
    # subplot1 line (Progress)
    x = np.arange(len(s.array[0]))
    plt.figure()
    plt.plot(x, s.array[0], color="lightskyblue", marker="o", linestyle="--", label="Actual Progress")
    plt.plot(x, s.X[0], color="red", marker="o", linestyle="--", label="Control Progress")
    plt.plot(x, green, color="lightgreen", marker="o", linestyle="--", label="Green Progress")
    plt.plot(x, yellow, color="orange", marker="o", linestyle="--", label="Yellow Progress")
    plt.plot(x, red, color="lightcoral", marker="o", linestyle="--", label="Red Progress")
    plt.legend()
    plt.grid(True)
    plt.xlabel("Time")
    plt.ylabel("Progress")
    plt.title("Project Progress Status")
    # plt.savefig("./figure/deviation.png")
    plt.show()
    # subplot1 line (Buffer Consume)
    plt.figure()
    plt.plot(x, status, color="lightskyblue", marker="o", linestyle="--", label="Actual Buffer Consume")
    plt.plot(x, buf_G, color="lightgreen", marker="o", linestyle="--", label="Green Buffer")
    plt.plot(x, buf_Y, color="orange", marker="o", linestyle="--", label="Yellow Buffer")
    plt.plot(x, buf_R, color="lightcoral", marker="o", linestyle="--", label="Red Buffer")
    plt.legend()
    plt.grid(True)
    plt.xlabel("Time")
    plt.ylabel("Buffer")
    plt.title("Project Buffer Consume")
    # plt.savefig("./figure/deviation.png")
    plt.show()
