#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

from experiment import ExperimentSingle
from gm import GMControl
from static import SPControl
from relative import RPControl
from dynamic import DPControl


class Active(object):
    def __init__(self, period, buffer, sigma, upper, lower) -> None:
        self.active = ExperimentSingle(period, buffer, sigma, upper, lower)
        self.next = None

    def simulate(self):
        self.active.simulate()


class Chain(object):
    def __init__(self, active=None) -> None:
        self.head = active
        self.period = 0
        self.time_gm = 0
        self.time_sp = 0
        self.time_rp = 0
        self.time_dp = 0
        self.cost_gm = 0
        self.cost_sp = 0
        self.cost_rp = 0
        self.cost_dp = 0
        self.ctrl_gm = 0
        self.ctrl_sp = 0
        self.ctrl_rp = 0
        self.ctrl_dp = 0
        self.total_buffer = 0

    def is_empty(self):
        return self.head is None

    def length(self):
        cur = self.head
        count = 0
        while cur is not None:
            count += 1
            cur = cur.next
        return count

    def append(self, active):
        if self.is_empty():
            self.head = active
        else:
            cur = self.head
            while cur.next is not None:
                cur = cur.next
            cur.next = active

    def add(self, active):
        node = active
        node.next = self.head
        self.head = node

    def insert(self, pos, active):
        if pos <= 0:
            self.add(active)
        elif pos > self.length() - 1:
            self.append(active)
        else:
            pre = self.head
            count = 0
            while count < pos - 1:
                count += 1
                pre = pre.next
            node = active
            node.next = pre.next
            pre.next = node

    def clean(self):
        self.period = 0
        self.time_gm = 0
        self.time_sp = 0
        self.time_rp = 0
        self.time_dp = 0
        self.cost_gm = 0
        self.cost_sp = 0
        self.cost_rp = 0
        self.cost_dp = 0
        self.ctrl_gm = 0
        self.ctrl_sp = 0
        self.ctrl_rp = 0
        self.ctrl_dp = 0
        self.total_buffer = 0

    def simulate(self):
        cur = self.head
        self.clean()
        while cur is not None:
            cur.simulate()
            self.period += cur.active.time_expect
            self.time_gm += cur.active.time_gm
            self.time_sp += cur.active.time_sp
            self.time_rp += cur.active.time_rp
            self.time_dp += cur.active.time_dp
            self.cost_gm += cur.active.time_gm - cur.active.time_expect
            self.cost_sp += cur.active.time_sp - cur.active.time_expect
            self.cost_rp += cur.active.time_rp - cur.active.time_expect
            self.cost_dp += cur.active.time_dp - cur.active.time_expect
            self.ctrl_gm += GMControl.Count
            self.ctrl_sp += SPControl.Count
            self.ctrl_rp += RPControl.Count
            self.ctrl_dp += DPControl.Count
            self.total_buffer += cur.active.buffer
            cur = cur.next
        # End of Chain
        if self.cost_gm < 0:
            self.cost_gm = 0
        if self.cost_sp < 0:
            self.cost_sp = 0
        if self.cost_rp < 0:
            self.cost_rp = 0
        if self.cost_dp < 0:
            self.cost_dp = 0


class Project(object):
    def __init__(self) -> None:
        self.list_chain = list()

    def append(self, chain):
        self.list_chain.append(chain)

    def simulate(self):
        for i in range(len(self.list_chain)):
            self.list_chain[i].simulate()


class ProjectSimulator(object):
    def __init__(self, number) -> None:
        self.project = Project()
        self.number = number
        self.period_gm = np.empty(shape=(0, 0))
        self.period_sp = np.empty(shape=(0, 0))
        self.period_rp = np.empty(shape=(0, 0))
        self.period_dp = np.empty(shape=(0, 0))
        self.period = 0
        self.ave_gm = 0
        self.ave_sp = 0
        self.ave_rp = 0
        self.ave_dp = 0
        self.dist_gm = dict()
        self.dist_sp = dict()
        self.dist_rp = dict()
        self.dist_dp = dict()

    def append(self, chain):
        self.project.append(chain)

    def simulate(self):
        for i in range(self.number):
            self.project.simulate()
            # calc period of each project simulation
            period = self.period
            period_gm = self.project.list_chain[0].time_gm
            period_sp = self.project.list_chain[0].time_sp
            period_rp = self.project.list_chain[0].time_rp
            period_dp = self.project.list_chain[0].time_dp
            for i in range(len(self.project.list_chain)):
                if self.project.list_chain[i].period > period:
                    period = self.project.list_chain[i].period
                if self.project.list_chain[i].time_gm > period_gm:
                    period_gm = self.project.list_chain[i].time_gm
                if self.project.list_chain[i].time_sp > period_sp:
                    period_sp = self.project.list_chain[i].time_sp
                if self.project.list_chain[i].time_rp > period_rp:
                    period_rp = self.project.list_chain[i].time_rp
                if self.project.list_chain[i].time_dp > period_dp:
                    period_dp = self.project.list_chain[i].time_dp
            # period list append elements
            self.period = period
            self.period_gm = np.append(self.period_gm, period_gm)
            self.period_sp = np.append(self.period_sp, period_sp)
            self.period_rp = np.append(self.period_rp, period_rp)
            self.period_dp = np.append(self.period_dp, period_dp)
        # project data statistic
        self.ave_gm = np.average(self.period_gm)
        self.ave_sp = np.average(self.period_sp)
        self.ave_rp = np.average(self.period_rp)
        self.ave_dp = np.average(self.period_dp)
        # project finish diction
        keys = np.unique(self.period_gm)
        for k in keys:
            v = self.period_gm[self.period_gm == k].size
            self.dist_gm[k] = v
        keys = np.unique(self.period_sp)
        for k in keys:
            v = self.period_sp[self.period_sp == k].size
            self.dist_sp[k] = v
        keys = np.unique(self.period_rp)
        for k in keys:
            v = self.period_rp[self.period_rp == k].size
            self.dist_rp[k] = v
        keys = np.unique(self.period_dp)
        for k in keys:
            v = self.period_dp[self.period_dp == k].size
            self.dist_dp[k] = v


if __name__ == '__main__':
    # Project Activities
    activeA = Active(3, 1, 0.03, 8, 2)
    activeB = Active(1, 0.5, 0.01, 4, 1)
    activeC = Active(3, 1, 0.03, 8, 2)
    activeD = Active(2, 0.5, 0.02, 5, 2)
    activeE = Active(2, 0.5, 0.02, 5, 2)
    activeF = Active(1, 0.5, 0.01, 4, 1)
    activeG = Active(21, 7, 0.21, 56, 14)
    activeH = Active(15, 5, 0.15, 40, 10)
    activeI = Active(18, 6, 0.18, 48, 12)
    activeJ = Active(9, 3, 0.09, 24, 6)
    activeK = Active(5, 1.5, 0.05, 13, 4)
    activeL = Active(6, 2, 0.06, 16, 4)
    activeM = Active(1, 0, 0.01, 1, 1)
    activeN = Active(3, 2, 0.03, 13, 1)
    activeO = Active(2, 1, 0.02, 7, 1)
    activeP = Active(1, 0, 0.01, 1, 1)
    # Combine Activities
    activeABDF = Active(7, 3, 0.05, 22, 4)
    activeABCF = Active(8, 3, 0.05, 23, 5)
    activeABEF = Active(7, 3, 0.05, 22, 4)
    activeKM = Active(6, 5, 0.05, 31, 1)
    activeJM = Active(10, 3, 0.05, 25, 7)
    activeLM = Active(7, 5, 0.05, 32, 2)
    activeNOP = Active(6, 3, 0.05, 21, 3)
    # chain1
    chain1 = Chain(activeABDF)
    chain1.append(activeH)
    chain1.append(activeKM)
    chain1.append(activeNOP)
    # chain 2 (critical chain)
    chain2 = Chain(activeABCF)
    chain2.append(activeG)
    chain2.append(activeJM)
    chain2.append(activeNOP)
    # chain 3
    chain3 = Chain(activeABEF)
    chain3.append(activeI)
    chain3.append(activeLM)
    chain3.append(activeNOP)
    # project 1
    project1 = Project()
    project1.append(chain1)
    project1.append(chain2)
    project1.append(chain3)
    project1.simulate()
    # project simulator calculate
    number = 10000
    ps = ProjectSimulator(number)
    ps.append(chain1)
    ps.append(chain2)
    ps.append(chain3)
    ps.simulate()
    # project graphics charts
    # project graphics 1 (Project Time Cost Distribution)
    plt.figure()
    plt.plot(ps.dist_gm.keys(), ps.dist_gm.values(), color="lightskyblue", marker="o", linestyle="--",
             label="Gray Model")
    plt.plot(ps.dist_sp.keys(), ps.dist_sp.values(), color="orange", marker="o", linestyle="--",
             label="Static Partition")
    plt.plot(ps.dist_rp.keys(), ps.dist_rp.values(), color="lightgreen", marker="o", linestyle="--",
             label="Relative Partition")
    plt.plot(ps.dist_dp.keys(), ps.dist_dp.values(), color="violet", marker="o", linestyle="--",
             label="Dynamic Partition")
    plt.legend()
    plt.grid(True)
    plt.xlabel("Time")
    plt.ylabel("Number")
    plt.title("Project Finish Time Cost Distribution")
    # plt.savefig("./figure/project_simulate.png")
    plt.show()
    print("hello")
