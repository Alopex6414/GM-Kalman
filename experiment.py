#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

from schedule import Schedule
from kalman import KalmanFilter
from gm import GMControl
from static import SPControl
from relative import RPControl
from dynamic import DPControl


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
        # GM/SP/RP/DP/SBMA baseline
        GMControl.setup_array(self.kalman.X)
        SPControl.setup_array(self.kalman.X)
        RPControl.setup_array(self.kalman.X)
        DPControl.setup_array(self.kalman.X)
        # GM/SP/RP/DP/SBMA predict
        for i in range(5, len(self.kalman.X[0])):
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
        # buffer cost
        self.arr_buf_cc = np.empty(shape=(0, 0))
        self.arr_buf_gm = np.empty(shape=(0, 0))
        self.arr_buf_sp = np.empty(shape=(0, 0))
        self.arr_buf_rp = np.empty(shape=(0, 0))
        self.arr_buf_dp = np.empty(shape=(0, 0))
        self.dist_buf_cc = dict()
        self.dist_buf_gm = dict()
        self.dist_buf_sp = dict()
        self.dist_buf_rp = dict()
        self.dist_buf_dp = dict()
        # control frequency
        self.arr_ctrl_gm = np.empty(shape=(0, 0))
        self.arr_ctrl_sp = np.empty(shape=(0, 0))
        self.arr_ctrl_rp = np.empty(shape=(0, 0))
        self.arr_ctrl_dp = np.empty(shape=(0, 0))
        self.dist_ctrl_gm = dict()
        self.dist_ctrl_sp = dict()
        self.dist_ctrl_rp = dict()
        self.dist_ctrl_dp = dict()
        # buffer colors count
        self.dist_color_gm = dict({"R": 0, "Y": 0, "G": 0})
        self.dist_color_sp = dict({"R": 0, "Y": 0, "G": 0})
        self.dist_color_rp = dict({"R": 0, "Y": 0, "G": 0})
        self.dist_color_dp = dict({"R": 0, "Y": 0, "G": 0})
        # discovery deviation time
        self.arr_dev_gm = np.empty(shape=(0, 0))
        self.arr_dev_sp = np.empty(shape=(0, 0))
        self.arr_dev_rp = np.empty(shape=(0, 0))
        self.arr_dev_dp = np.empty(shape=(0, 0))
        self.dist_dev_gm = dict()
        self.dist_dev_sp = dict()
        self.dist_dev_rp = dict()
        self.dist_dev_dp = dict()
        super(ExperimentMultiple, self).__init__(period, buffer)

    def simulate(self):
        # collect all data
        for i in range(0, self.number):
            super(ExperimentMultiple, self).simulate()
            # statistic distribution
            self.arr_ex = np.append(self.arr_ex, self.time_expect)
            self.arr_cc = np.append(self.arr_cc, self.time_cc)
            self.arr_gm = np.append(self.arr_gm, self.time_gm)
            self.arr_sp = np.append(self.arr_sp, self.time_sp)
            self.arr_rp = np.append(self.arr_rp, self.time_rp)
            self.arr_dp = np.append(self.arr_dp, self.time_dp)
            # buffer cost
            self.arr_buf_cc = np.append(self.arr_buf_cc, (self.time_cc - self.time_expect))
            self.arr_buf_gm = np.append(self.arr_buf_gm, (self.time_gm - self.time_expect))
            self.arr_buf_sp = np.append(self.arr_buf_sp, (self.time_sp - self.time_expect))
            self.arr_buf_rp = np.append(self.arr_buf_rp, (self.time_rp - self.time_expect))
            self.arr_buf_dp = np.append(self.arr_buf_dp, (self.time_dp - self.time_expect))
            # control frequency
            self.arr_ctrl_gm = np.append(self.arr_ctrl_gm, GMControl.Count)
            self.arr_ctrl_sp = np.append(self.arr_ctrl_sp, SPControl.Count)
            self.arr_ctrl_rp = np.append(self.arr_ctrl_rp, RPControl.Count)
            self.arr_ctrl_dp = np.append(self.arr_ctrl_dp, DPControl.Count)
            # buffer colors count
            b_dev_gm = False
            for k, v in GMControl.Status.items():
                if not b_dev_gm and v["control"] == 1:
                    b_dev_gm = True
                    self.arr_dev_gm = np.append(self.arr_dev_gm, int(k))
                if v["status"] == "R":
                    self.dist_color_gm["R"] = self.dist_color_gm["R"] + 1
                if v["status"] == "Y":
                    self.dist_color_gm["Y"] = self.dist_color_gm["Y"] + 1
                if v["status"] == "G":
                    self.dist_color_gm["G"] = self.dist_color_gm["G"] + 1
            b_dev_sp = False
            for k, v in SPControl.Status.items():
                if not b_dev_sp and v["control"] == 1:
                    b_dev_sp = True
                    self.arr_dev_sp = np.append(self.arr_dev_sp, int(k))
                if v["status"] == "R":
                    self.dist_color_sp["R"] = self.dist_color_sp["R"] + 1
                if v["status"] == "Y":
                    self.dist_color_sp["Y"] = self.dist_color_sp["Y"] + 1
                if v["status"] == "G":
                    self.dist_color_sp["G"] = self.dist_color_sp["G"] + 1
            b_dev_rp = False
            for k, v in RPControl.Status.items():
                if not b_dev_rp and v["control"] == 1:
                    b_dev_rp = True
                    self.arr_dev_rp = np.append(self.arr_dev_rp, int(k))
                if v["status"] == "R":
                    self.dist_color_rp["R"] = self.dist_color_rp["R"] + 1
                if v["status"] == "Y":
                    self.dist_color_rp["Y"] = self.dist_color_rp["Y"] + 1
                if v["status"] == "G":
                    self.dist_color_rp["G"] = self.dist_color_rp["G"] + 1
            b_dev_dp = False
            for k, v in DPControl.Status.items():
                if not b_dev_dp and v["control"] == 1:
                    b_dev_dp = True
                    self.arr_dev_dp = np.append(self.arr_dev_dp, int(k))
                if v["status"] == "R":
                    self.dist_color_dp["R"] = self.dist_color_dp["R"] + 1
                if v["status"] == "Y":
                    self.dist_color_dp["Y"] = self.dist_color_dp["Y"] + 1
                if v["status"] == "G":
                    self.dist_color_dp["G"] = self.dist_color_dp["G"] + 1
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
        # buffer cost evaluation
        for i in range(self.number):
            if self.arr_buf_cc[i] < 0:
                self.arr_buf_cc[i] = 0
        for i in range(self.number):
            if self.arr_buf_gm[i] < 0:
                self.arr_buf_gm[i] = 0
        for i in range(self.number):
            if self.arr_buf_sp[i] < 0:
                self.arr_buf_sp[i] = 0
        for i in range(self.number):
            if self.arr_buf_rp[i] < 0:
                self.arr_buf_rp[i] = 0
        for i in range(self.number):
            if self.arr_buf_dp[i] < 0:
                self.arr_buf_dp[i] = 0
        keys = np.unique(self.arr_buf_cc)
        for k in keys:
            v = self.arr_buf_cc[self.arr_buf_cc == k].size
            self.dist_buf_cc[k] = v
        keys = np.unique(self.arr_buf_gm)
        for k in keys:
            v = self.arr_buf_gm[self.arr_buf_gm == k].size
            self.dist_buf_gm[k] = v
        keys = np.unique(self.arr_buf_sp)
        for k in keys:
            v = self.arr_buf_sp[self.arr_buf_sp == k].size
            self.dist_buf_sp[k] = v
        keys = np.unique(self.arr_buf_rp)
        for k in keys:
            v = self.arr_buf_rp[self.arr_buf_rp == k].size
            self.dist_buf_rp[k] = v
        keys = np.unique(self.arr_buf_dp)
        for k in keys:
            v = self.arr_buf_dp[self.arr_buf_dp == k].size
            self.dist_buf_dp[k] = v
        # control frequency evaluation
        keys = np.unique(self.arr_ctrl_gm)
        for k in keys:
            v = self.arr_ctrl_gm[self.arr_ctrl_gm == k].size
            self.dist_ctrl_gm[k] = v
        keys = np.unique(self.arr_ctrl_sp)
        for k in keys:
            v = self.arr_ctrl_sp[self.arr_ctrl_sp == k].size
            self.dist_ctrl_sp[k] = v
        keys = np.unique(self.arr_ctrl_rp)
        for k in keys:
            v = self.arr_ctrl_rp[self.arr_ctrl_rp == k].size
            self.dist_ctrl_rp[k] = v
        keys = np.unique(self.arr_ctrl_dp)
        for k in keys:
            v = self.arr_ctrl_dp[self.arr_ctrl_dp == k].size
            self.dist_ctrl_dp[k] = v
        # discovery deviation time
        keys = np.unique(self.arr_dev_gm)
        for k in keys:
            v = self.arr_dev_gm[self.arr_dev_gm == k].size
            self.dist_dev_gm[k] = v
        keys = np.unique(self.arr_dev_sp)
        for k in keys:
            v = self.arr_dev_sp[self.arr_dev_sp == k].size
            self.dist_dev_sp[k] = v
        keys = np.unique(self.arr_dev_rp)
        for k in keys:
            v = self.arr_dev_rp[self.arr_dev_rp == k].size
            self.dist_dev_rp[k] = v
        keys = np.unique(self.arr_dev_dp)
        for k in keys:
            v = self.arr_dev_dp[self.arr_dev_dp == k].size
            self.dist_dev_dp[k] = v

    def show(self):
        # plot preparation
        p = np.arange(self.number)
        # subplot1 line (Project Finish Time Statistic Distribution)
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
        plt.title("Project Finish Time Statistic Distribution")
        plt.show()
        # subplot2 bar(Finish Time Overdue & On Schedule)
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
        plt.title("Project Finish Time On Schedule & Overdue")
        plt.show()
        # subplot3 line(Finish Buffer Cost Distribution)
        plt.figure()
        plt.plot(self.dist_buf_cc.keys(), self.dist_buf_cc.values(), color="lightcoral", marker="o", linestyle="--",
                 label="Critical Chain")
        plt.plot(self.dist_buf_gm.keys(), self.dist_buf_gm.values(), color="lightskyblue", marker="o", linestyle="--",
                 label="Gray Model")
        plt.plot(self.dist_buf_sp.keys(), self.dist_buf_sp.values(), color="orange", marker="o", linestyle="--",
                 label="Static Partition")
        plt.plot(self.dist_buf_rp.keys(), self.dist_buf_rp.values(), color="lightgreen", marker="o", linestyle="--",
                 label="Relative Partition")
        plt.plot(self.dist_buf_dp.keys(), self.dist_buf_dp.values(), color="violet", marker="o", linestyle="--",
                 label="Dynamic Partition")
        plt.legend()
        plt.grid(True)
        plt.xlabel("Buffer")
        plt.ylabel("Number")
        plt.title("Project Finish Time Buffer Cost")
        plt.show()
        # subplot4 line (Project Control Frequency Statistic Distribution)
        plt.figure()
        plt.plot(self.dist_ctrl_gm.keys(), self.dist_ctrl_gm.values(), marker="o", linestyle="--", color="lightskyblue",
                 label="Gray Model")
        plt.plot(self.dist_ctrl_sp.keys(), self.dist_ctrl_sp.values(), marker="o", linestyle="--", color="orange",
                 label="Static Partition")
        plt.plot(self.dist_ctrl_rp.keys(), self.dist_ctrl_rp.values(), marker="o", linestyle="--", color="lightgreen",
                 label="Relative Partition")
        plt.plot(self.dist_ctrl_dp.keys(), self.dist_ctrl_dp.values(), marker="o", linestyle="--", color="violet",
                 label="Dynamic Partition")
        plt.legend()
        plt.grid(True)
        plt.xlabel("Time")
        plt.ylabel("Number")
        plt.title("Project Control Frequency Statistic Distribution")
        plt.show()
        # subplot5 bar(Project Buffer Colors Count Distribution)
        fig, ax = plt.subplots()
        labels = ["GM", "SP", "RP", "DP"]
        reds = [self.dist_color_gm.get("R"), self.dist_color_sp.get("R"), self.dist_color_rp.get("R"),
                self.dist_color_dp.get("R")]
        yellows = [self.dist_color_gm.get("Y"), self.dist_color_sp.get("Y"), self.dist_color_rp.get("Y"),
                   self.dist_color_dp.get("Y")]
        greens = [self.dist_color_gm.get("G"), self.dist_color_sp.get("G"), self.dist_color_rp.get("G"),
                  self.dist_color_dp.get("G")]
        x = np.arange(len(labels))
        width = 0.3
        ax.bar(x - width, reds, width=width, color="lightcoral")
        ax.bar(x, yellows, width=width, color="lightyellow")
        ax.bar(x + width, greens, width=width, color="lightgreen")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        plt.grid(True)
        plt.xlabel("Schedule Management Method")
        plt.ylabel("Number")
        plt.title("Project Buffer Colors Count Distribution")
        # plt.savefig("./figure/overdue.png")
        plt.show()
        # subplot6 line (Project Discovery Deviation Time Distribution)
        plt.figure()
        plt.plot(self.dist_dev_gm.keys(), self.dist_dev_gm.values(), marker="o", linestyle="--", color="lightskyblue",
                 label="Gray Model")
        plt.plot(self.dist_dev_sp.keys(), self.dist_dev_sp.values(), marker="o", linestyle="--", color="orange",
                 label="Static Partition")
        plt.plot(self.dist_dev_rp.keys(), self.dist_dev_rp.values(), marker="o", linestyle="--", color="lightgreen",
                 label="Relative Partition")
        plt.plot(self.dist_dev_dp.keys(), self.dist_dev_dp.values(), marker="o", linestyle="--", color="violet",
                 label="Dynamic Partition")
        plt.legend()
        plt.grid(True)
        plt.xlabel("Time")
        plt.ylabel("Number")
        plt.title("Project Discovery Deviation Time Distribution")
        plt.show()
        # subplot7 line (Project Finish Time Distribution)
        plt.figure()
        plt.plot(p, self.arr_cc, color="lightcoral", marker="o", linestyle="--", label="Critical Chain")
        plt.plot(p, self.arr_gm, color="lightskyblue", marker="o", linestyle="--", label="Gray Model")
        plt.plot(p, self.arr_sp, color="orange", marker="o", linestyle="--", label="Static Partition")
        plt.plot(p, self.arr_rp, color="lightgreen", marker="o", linestyle="--", label="Relative Partition")
        plt.plot(p, self.arr_dp, color="violet", marker="o", linestyle="--", label="Dynamic Partition")
        plt.legend()
        plt.grid(True)
        plt.xlabel("number")
        plt.ylabel("time")
        plt.title("Project Finish Distribution")
        plt.show()


if __name__ == '__main__':
    s = ExperimentMultiple(15, 3, 10000)
    s.simulate()
    s.show()
