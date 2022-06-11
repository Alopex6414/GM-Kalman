#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

from schedule import Schedule
from kalman import KalmanFilter
from gm import GM, GMControl


class SimulatorSingle(object):
    def __init__(self, period):
        """
        :param period: please input schedule period
        """
        self.period = period
        self.buffer = 0
        self.time_expect = self.period
        self.time_cc = 0
        self.time_gm = 0
        self.schedule = None
        self.kalman = None
        self.gm = None
        self.gmc = None

    def simulate(self):
        # generate schedule
        self.schedule = Schedule(self.period)
        self.schedule.gen()
        # kalman filter
        self.kalman = KalmanFilter(self.schedule.progress, self.schedule.velocity)
        self.kalman.filter()
        # GM baseline
        GMControl.setup_array(self.kalman.X)
        # GM predict
        for i in range(5, len(self.kalman.X[0])):
            self.gm = GM(self.kalman.X, i)
            self.gm.gray_predict()
            self.gmc = GMControl(self.kalman.X, i, self.period)
            self.gmc.gray_predict()
        # calculate project finish time...
        # critical chain finish time
        b = False
        for i in range(0, len(self.schedule.progress)):
            if self.schedule.progress[i] >= 1.:
                b = True
                self.time_cc = i
                break
        if not b:
            self.time_cc = len(self.schedule.progress)
        # gray model finish time
        b = False
        for i in range(0, len(GMControl.X[0, :])):
            if GMControl.X[0, i] >= 1.:
                b = True
                self.time_gm = i
                break
        if not b:
            self.time_gm = len(GMControl.X[0, :])


class SimulatorMultiple(SimulatorSingle):
    def __init__(self, period, number):
        """
        :param period: please input schedule period
        """
        self.number = number
        self.arr_ex = np.empty(shape=(0, 0))
        self.arr_cc = np.empty(shape=(0, 0))
        self.arr_gm = np.empty(shape=(0, 0))
        super(SimulatorMultiple, self).__init__(period)

    def simulate(self):
        for i in range(0, self.number):
            super(SimulatorMultiple, self).simulate()
            self.arr_ex = np.append(self.arr_ex, self.time_expect)
            self.arr_cc = np.append(self.arr_cc, self.time_cc)
            self.arr_gm = np.append(self.arr_gm, self.time_gm)

    def show(self):
        # plot preparation
        x = np.arange(self.number)
        # subplot1 bar
        plt.figure()
        plt.bar(x, self.arr_ex, color="lightcoral", label="expect")
        plt.bar(x, self.arr_cc, color="lightskyblue", label="critical chain")
        plt.bar(x, self.arr_gm, color="lightgreen", label="gray model")
        plt.legend()
        plt.grid(linestyle='--', linewidth=1.0)
        plt.xlabel("number")
        plt.ylabel("time")
        plt.title("Project Finish Time")
        plt.show()
        # subplot2 line
        plt.figure()
        plt.plot(x, self.arr_ex, color="lightcoral", marker="x", linestyle="--", label="expect")
        plt.plot(x, self.arr_cc, color="lightskyblue", marker="o", linestyle="--", label="critical chain")
        plt.plot(x, self.arr_gm, color="lightgreen", marker="o", linestyle="--", label="gray model")
        plt.legend()
        plt.grid(True)
        plt.xlabel("number")
        plt.ylabel("time")
        plt.title("Project Finish Distribution")
        plt.show()


if __name__ == '__main__':
    s = SimulatorMultiple(15, 25)
    s.simulate()
    s.show()
