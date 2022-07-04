#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

from schedule import Schedule
from kalman import KalmanFilter
from gm import GM, GMControl
from static import SP, SPControl
from relative import RP, RPControl
from dynamic import DP, DPControl


class Experiment(object):
    def __init__(self):
        pass


class ExperimentSingle(object):
    def __init__(self, period, buffer):
        """
        :param period: please input schedule period
        :param buffer: please input schedule buffer
        """
        self.period = period
        self.buffer = buffer
        self.time_expect = self.period
        self.time_cc = 0
        self.time_gm = 0
        self.time_sp = 0
        self.time_rp = 0
        self.time_dp = 0
        self.schedule = None
        self.kalman = None
        self.gm = None
        self.gmc = None
        self.spc = None
        self.rpc = None
        self.dpc = None

    def simulate(self):
        # generate schedule
        self.schedule = Schedule(self.period)
        self.schedule.gen()
        # kalman filter
        self.kalman = KalmanFilter(self.schedule.progress, self.schedule.velocity)
        self.kalman.filter()
        # GM/SP/RP/DP baseline
        GMControl.setup_array(self.kalman.X)
        SPControl.setup_array(self.kalman.X)
        RPControl.setup_array(self.kalman.X)
        DPControl.setup_array(self.kalman.X)
        # GM/SP/RP/DP predict
        for i in range(5, len(self.kalman.X[0])):
            self.gm = GM(self.kalman.X, self.buffer, i)
            self.gm.gray_predict2()
            self.gmc = GMControl(self.kalman.X, self.buffer, i, self.period)
            self.gmc.gray_predict2()
            self.spc = SPControl(self.kalman.X, self.buffer, i, self.period)
            self.spc.static_control()
            self.rpc = RPControl(self.kalman.X, self.buffer, i, self.period)
            self.rpc.relative_control()
            self.dpc = DPControl(self.kalman.X, self.buffer, i, self.period)
            self.dpc.dynamic_control()
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
        # static partition finish time
        b = False
        for i in range(0, len(SPControl.X[0, :])):
            if SPControl.X[0, i] >= 1.:
                b = True
                self.time_sp = i
                break
        if not b:
            self.time_sp = len(SPControl.X[0, :])
        # relative partition finish time
        b = False
        for i in range(0, len(RPControl.X[0, :])):
            if RPControl.X[0, i] >= 1.:
                b = True
                self.time_rp = i
                break
        if not b:
            self.time_rp = len(RPControl.X[0, :])
        # dynamic partition finish time
        b = False
        for i in range(0, len(DPControl.X[0, :])):
            if DPControl.X[0, i] >= 1.:
                b = True
                self.time_dp = i
                break
        if not b:
            self.time_dp = len(DPControl.X[0, :])


class ExperimentMultiple(ExperimentSingle):
    def __init__(self, period, buffer, number):
        """
        :param period: please input schedule period
        :param buffer: please input schedule buffer
        :param number: please input total number
        """
        self.number = number
        # project finish time array
        self.arr_ex = np.empty(shape=(0, 0))
        self.arr_cc = np.empty(shape=(0, 0))
        self.arr_gm = np.empty(shape=(0, 0))
        self.arr_sp = np.empty(shape=(0, 0))
        self.arr_rp = np.empty(shape=(0, 0))
        self.arr_dp = np.empty(shape=(0, 0))
        # statistic distribution
        self.dist_cc = dict()
        self.dist_gm = dict()
        self.dist_sp = dict()
        self.dist_rp = dict()
        self.dist_dp = dict()
        # on schedule & overdue
        self.dist_over_cc = dict()
        self.dist_over_gm = dict()
        self.dist_over_sp = dict()
        self.dist_over_rp = dict()
        self.dist_over_dp = dict()
        super(ExperimentMultiple, self).__init__(period, buffer)

    def simulate(self):
        # collect all data
        for i in range(0, self.number):
            super(ExperimentMultiple, self).simulate()
            self.arr_ex = np.append(self.arr_ex, self.time_expect)
            self.arr_cc = np.append(self.arr_cc, self.time_cc)
            self.arr_gm = np.append(self.arr_gm, self.time_gm)
            self.arr_sp = np.append(self.arr_sp, self.time_sp)
            self.arr_rp = np.append(self.arr_rp, self.time_rp)
            self.arr_dp = np.append(self.arr_dp, self.time_dp)
        # statistical evaluation
        keys = np.unique(self.arr_cc)
        for k in keys:
            v = self.arr_cc[self.arr_cc == k].size
            self.dist_cc[k] = v
        keys = np.unique(self.arr_gm)
        for k in keys:
            v = self.arr_gm[self.arr_gm == k].size
            self.dist_gm[k] = v
        keys = np.unique(self.arr_sp)
        for k in keys:
            v = self.arr_sp[self.arr_sp == k].size
            self.dist_sp[k] = v
        keys = np.unique(self.arr_rp)
        for k in keys:
            v = self.arr_rp[self.arr_rp == k].size
            self.dist_rp[k] = v
        keys = np.unique(self.arr_dp)
        for k in keys:
            v = self.arr_dp[self.arr_dp == k].size
            self.dist_dp[k] = v
        # on schedule & overdue
        self.dist_over_cc["overdue"] = np.sum(self.arr_cc > self.time_expect + self.buffer)
        self.dist_over_cc["on_schedule"] = np.sum(self.arr_cc <= self.time_expect)
        self.dist_over_cc["in_buffer"] = len(self.arr_cc) - self.dist_over_cc["overdue"] - self.dist_over_cc[
            "on_schedule"]
        self.dist_over_gm["overdue"] = np.sum(self.arr_gm > self.time_expect + self.buffer)
        self.dist_over_gm["on_schedule"] = np.sum(self.arr_gm <= self.time_expect)
        self.dist_over_gm["in_buffer"] = len(self.arr_gm) - self.dist_over_gm["overdue"] - self.dist_over_gm[
            "on_schedule"]
        self.dist_over_sp["overdue"] = np.sum(self.arr_sp > self.time_expect + self.buffer)
        self.dist_over_sp["on_schedule"] = np.sum(self.arr_sp <= self.time_expect)
        self.dist_over_sp["in_buffer"] = len(self.arr_sp) - self.dist_over_sp["overdue"] - self.dist_over_sp[
            "on_schedule"]
        self.dist_over_rp["overdue"] = np.sum(self.arr_rp > self.time_expect + self.buffer)
        self.dist_over_rp["on_schedule"] = np.sum(self.arr_rp <= self.time_expect)
        self.dist_over_rp["in_buffer"] = len(self.arr_rp) - self.dist_over_rp["overdue"] - self.dist_over_rp[
            "on_schedule"]
        self.dist_over_dp["overdue"] = np.sum(self.arr_dp > self.time_expect + self.buffer)
        self.dist_over_dp["on_schedule"] = np.sum(self.arr_dp <= self.time_expect)
        self.dist_over_dp["in_buffer"] = len(self.arr_dp) - self.dist_over_dp["overdue"] - self.dist_over_dp[
            "on_schedule"]

    def show(self):
        # plot preparation
        x = np.arange(self.number)
        # subplot1 bar (Project Finish Time Distribution Statistic)
        plt.figure()
        plt.plot(self.dist_cc.keys(), self.dist_cc.values(), marker="o", linestyle="--", color="lightcoral",
                 label="Critical Chain")
        plt.plot(self.dist_gm.keys(), self.dist_gm.values(), marker="o", linestyle="--", color="lightskyblue",
                 label="Gray Model")
        plt.plot(self.dist_sp.keys(), self.dist_sp.values(), marker="o", linestyle="--", color="orange",
                 label="Static Partition")
        plt.plot(self.dist_rp.keys(), self.dist_rp.values(), marker="o", linestyle="--", color="lightgreen",
                 label="Relative Partition")
        plt.plot(self.dist_dp.keys(), self.dist_dp.values(), marker="o", linestyle="--", color="violet",
                 label="Dynamic Partition")
        plt.legend()
        plt.grid(True)
        plt.xlabel("Time")
        plt.ylabel("Number")
        plt.title("Project Finish Time Distribution Statistic")
        plt.show()
        # subplot4 bar(Finish Time Overdue & On Schedule)
        plt.figure()
        plt.bar("CC", self.dist_over_cc.get("on_schedule"), width=0.4, color="lightgreen")
        plt.bar("CC", self.dist_over_cc.get("in_buffer"), bottom=self.dist_over_cc.get("on_schedule"), width=0.4,
                color="lightyellow")
        plt.bar("CC", self.dist_over_cc.get("overdue"),
                bottom=self.dist_over_cc.get("on_schedule") + self.dist_over_cc.get("in_buffer"), width=0.4,
                color="lightcoral")
        plt.bar("GM", self.dist_over_gm.get("on_schedule"), width=0.4, color="lightgreen")
        plt.bar("GM", self.dist_over_gm.get("in_buffer"), bottom=self.dist_over_gm.get("on_schedule"), width=0.4,
                color="lightyellow")
        plt.bar("GM", self.dist_over_gm.get("overdue"),
                bottom=self.dist_over_gm.get("on_schedule") + self.dist_over_gm.get("in_buffer"), width=0.4,
                color="lightcoral")
        plt.bar("SP", self.dist_over_sp.get("on_schedule"), width=0.4, color="lightgreen")
        plt.bar("SP", self.dist_over_sp.get("in_buffer"), bottom=self.dist_over_sp.get("on_schedule"), width=0.4,
                color="lightyellow")
        plt.bar("SP", self.dist_over_sp.get("overdue"),
                bottom=self.dist_over_sp.get("on_schedule") + self.dist_over_sp.get("in_buffer"), width=0.4,
                color="lightcoral")
        plt.bar("RP", self.dist_over_rp.get("on_schedule"), width=0.4, color="lightgreen")
        plt.bar("RP", self.dist_over_rp.get("in_buffer"), bottom=self.dist_over_rp.get("on_schedule"), width=0.4,
                color="lightyellow")
        plt.bar("RP", self.dist_over_rp.get("overdue"),
                bottom=self.dist_over_rp.get("on_schedule") + self.dist_over_rp.get("in_buffer"), width=0.4,
                color="lightcoral")
        plt.bar("DP", self.dist_over_dp.get("on_schedule"), width=0.4, color="lightgreen")
        plt.bar("DP", self.dist_over_dp.get("in_buffer"), bottom=self.dist_over_dp.get("on_schedule"), width=0.4,
                color="lightyellow")
        plt.bar("DP", self.dist_over_dp.get("overdue"),
                bottom=self.dist_over_dp.get("on_schedule") + self.dist_over_dp.get("in_buffer"), width=0.4,
                color="lightcoral")
        plt.grid(True)
        plt.xlabel("Schedule Management Method")
        plt.ylabel("Number")
        plt.title("Project Finish Time Overdue & On Schedule")
        plt.show()


if __name__ == '__main__':
    s = ExperimentMultiple(15, 3, 10000)
    s.simulate()
    s.show()
