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
        self.ave_ex = None
        self.ave_cc = None
        self.ave_gm = None
        self.std_cc = None
        self.std_gm = None
        self.dist_cc = dict()
        self.dist_gm = dict()
        self.eva_cc = dict()
        self.eva_gm = dict()

        super(SimulatorMultiple, self).__init__(period)

    def simulate(self):
        # fill all data
        for i in range(0, self.number):
            super(SimulatorMultiple, self).simulate()
            self.arr_ex = np.append(self.arr_ex, self.time_expect)
            self.arr_cc = np.append(self.arr_cc, self.time_cc)
            self.arr_gm = np.append(self.arr_gm, self.time_gm)
        # calculate evaluation index
        self.ave_ex = self.time_expect
        self.ave_cc = np.mean(self.arr_cc)
        self.std_cc = np.std(self.arr_cc)
        self.ave_gm = np.mean(self.arr_gm)
        self.std_gm = np.std(self.arr_gm)
        # statistical evaluation
        keys = np.unique(self.arr_cc)
        for k in keys:
            v = self.arr_cc[self.arr_cc == k].size
            self.dist_cc[k-0.2] = v
        keys = np.unique(self.arr_gm)
        for k in keys:
            v = self.arr_gm[self.arr_gm == k].size
            self.dist_gm[k+0.2] = v
        # summary evaluation
        self.eva_cc["overdue"] = np.sum(self.arr_cc > self.time_expect)
        self.eva_cc["on_schedule"] = np.sum(self.arr_cc <= self.time_expect)
        self.eva_gm["overdue"] = np.sum(self.arr_gm > self.time_expect)
        self.eva_gm["on_schedule"] = np.sum(self.arr_gm <= self.time_expect)
        print("hello")

    def show(self):
        # plot preparation
        x = np.arange(self.number)
        """
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
        """
        # subplot3 bar (Finish Time Distribution Statistic)
        plt.figure()
        plt.bar(self.dist_cc.keys(), self.dist_cc.values(), width=0.4, color="lightcoral", label="Critical Chain")
        plt.bar(self.dist_gm.keys(), self.dist_gm.values(), width=0.4, color="lightskyblue", label="Gray Model")
        plt.legend()
        plt.grid(True)
        plt.xlabel("Time")
        plt.ylabel("Number")
        plt.title("Project Finish Time Distribution Statistic")
        # plt.savefig("./figure/dist.png")
        plt.show()
        # subplot4 bar(Finish Time Overdue & On Schedule)
        plt.figure()
        plt.bar("CC", self.eva_cc.get("on_schedule"), width=0.4, color="lightskyblue")
        plt.bar("CC", self.eva_cc.get("overdue"), bottom=self.eva_cc.get("on_schedule"), width=0.4, color="lightcoral")
        plt.bar("GM", self.eva_gm.get("on_schedule"), width=0.4, color="lightskyblue")
        plt.bar("GM", self.eva_gm.get("overdue"), bottom=self.eva_gm.get("on_schedule"), width=0.4, color="lightcoral")
        plt.grid(True)
        plt.xlabel("Schedule Management Method")
        plt.ylabel("Number")
        plt.title("Project Finish Time Overdue & On Schedule")
        # plt.savefig("./figure/overdue.png")
        plt.show()


if __name__ == '__main__':
    s = SimulatorMultiple(15, 10000)
    s.simulate()
    s.show()
