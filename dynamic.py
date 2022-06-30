#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import copy

from schedule import Schedule
from kalman import KalmanFilter


class DP(object):
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
        self.green = self.buffer * (1/3 + array[0, n] * (1. - 1/3))
        self.yellow = self.buffer * (2/3 + array[0, n] * (1. - 2/3))
        self.red = self.buffer
        self.status = dict()

    def dynamic_analysis(self):
        buf_size = self.actual - self.real
        if buf_size < self.green:
            result = 0
        elif buf_size < self.yellow:
            result = 1
        else:
            result = 2
        return result


class DPControl(DP):
    Status = dict()
    X = None
    Green = None
    Yellow = None
    Red = None
    STA = None

    def __init__(self, array, buffer, n, t):
        """
        :param array: project schedule progress status array (numpy array type) (2x2)
        :param buffer: project schedule progress feeding or project buffer
        :param n: project schedule progress status array actual length
        :param t: project schedule progress periodic
        """
        super(DPControl, self).__init__(array, buffer, n, t)

    @staticmethod
    def setup_array(array):
        DPControl.X = copy.deepcopy(array)
        DPControl.Green = np.zeros(len(array[0]))
        DPControl.Yellow = np.zeros(len(array[0]))
        DPControl.Red = np.zeros(len(array[0]))
        DPControl.STA = np.zeros(len(array[0]))

    def dynamic_analysis(self):
        result = super(DPControl, self).dynamic_analysis()
        if result == 0:
            DPControl.Status.update({"{}".format(self.actual): {"real": self.real, "actual": self.actual,
                                                                              "delta": self.delta, "status": "G"}})
        elif result == 1:
            DPControl.Status.update({"{}".format(self.actual): {"real": self.real, "actual": self.actual,
                                                                              "delta": self.delta, "status": "Y"}})
        else:
            DPControl.Status.update({"{}".format(self.actual): {"real": self.real, "actual": self.actual,
                                                                              "delta": self.delta, "status": "R"}})

    def dynamic_control(self):
        result = super(DPControl, self).dynamic_analysis()
        # calculate buffer size
        DPControl.Green[self.actual] = s.green
        DPControl.Yellow[self.actual] = s.yellow
        DPControl.Red[self.actual] = s.red
        DPControl.STA[self.actual] = s.Status.get("{}".format(i))["delta"]
        # project buffer consume result
        if result == 0:
            DPControl.X[1, self.actual] = DPControl.X[1, self.actual]
        elif result == 1:
            DPControl.X[1, self.actual] = DPControl.X[1, self.actual] + \
                                                         0.025 * (1. - self.array[0, self.actual])
        else:
            DPControl.X[1, self.actual] = DPControl.X[1, self.actual] + \
                                                         0.05 * (1. - self.array[0, self.actual])
        # update current progress
        if self.actual > 0:
            DPControl.X[0, self.actual] = DPControl.X[0, self.actual - 1] + \
                                                         DPControl.X[1, self.actual]
        if DPControl.X[0, self.actual] > 1.:
            DPControl.X[0, self.actual] = 1.


if __name__ == '__main__':
    period = 15
    # generate schedule
    schedule = Schedule(period)
    schedule.gen()
    # kalman filter
    kalman = KalmanFilter(schedule.progress, schedule.velocity)
    kalman.filter()
    # setup array
    DPControl.setup_array(kalman.X)
    for i in range(len(kalman.X[0])):
        s = DPControl(kalman.X, 5, i, period)
        s.dynamic_analysis()
        s.dynamic_control()
    # static safe buffer progress
    green = np.zeros(len(kalman.X[0]))
    yellow = np.zeros(len(kalman.X[0]))
    red = np.zeros(len(kalman.X[0]))
    for i in range(len(kalman.X[0])):
        # green buffer
        green[i] = i * 1. / (s.period + s.Green[i])
        if green[i] > 1.:
            green[i] = 1.
        # yellow buffer
        yellow[i] = i * 1. / (s.period + s.Yellow[i])
        if yellow[i] > 1.:
            yellow[i] = 1.
        # red buffer
        red[i] = i * 1. / (s.period + s.Red[i])
        if red[i] > 1.:
            red[i] = 1.
    # subplot1 line (Progress)
    x = np.arange(len(s.array[0]))
    plt.figure()
    plt.plot(x, s.array[0], color="lightskyblue", marker="o", linestyle="--", label="Actual Progress")
    plt.plot(x, s.X[0], color="slateblue", marker="o", linestyle="--", label="Control Progress")
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
    # subplot2 line (Buffer Consume)
    plt.figure()
    plt.plot(x, s.STA, color="lightskyblue", marker="o", linestyle="--", label="Actual Buffer Consume")
    plt.plot(x, s.Green, color="lightgreen", marker="o", linestyle="--", label="Green Buffer")
    plt.plot(x, s.Yellow, color="orange", marker="o", linestyle="--", label="Yellow Buffer")
    plt.plot(x, s.Red, color="lightcoral", marker="o", linestyle="--", label="Red Buffer")
    plt.legend()
    plt.grid(True)
    plt.xlabel("Time")
    plt.ylabel("Buffer")
    plt.title("Project Buffer Consume")
    # plt.savefig("./figure/deviation.png")
    plt.show()
