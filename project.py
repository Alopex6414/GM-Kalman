#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from schedule import Schedule
from kalman import KalmanFilter
from gm import GMControl
from static import SPControl
from relative import RPControl
from dynamic import DPControl


class Active(object):
    def __init__(self, period, sigma=0.05) -> None:
        self.schedule = Schedule(period, sigma)
        self.schedule.gen()
        self.kalman = KalmanFilter(self.schedule.progress, self.schedule.velocity)
        self.kalman.filter()
        self.time_cc = 0
        self.time_gm = 0
        self.time_sp = 0
        self.time_rp = 0
        self.time_dp = 0
        self.gmc = None
        self.spc = None
        self.rpc = None
        self.dpc = None
        self.next = None

    def simulate(self):
        # GM/SP/RP/DP baseline
        GMControl.setup_array(self.kalman.X)
        SPControl.setup_array(self.kalman.X)
        RPControl.setup_array(self.kalman.X)
        DPControl.setup_array(self.kalman.X)
        # GM/SP/RP/DP predict
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


class Chain(object):
    def __init__(self, active=None) -> None:
        self.head = active
        self.period = None
        self.actual = None

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

    def gen(self):
        cur = self.head
        self.period = 0
        self.actual = 0
        while cur is not None:
            self.period += cur.schedule.period
            self.actual += cur.schedule.actual
            cur = cur.next


class Project(object):
    def __init__(self) -> None:
        pass


if __name__ == '__main__':
    active1 = Active(15, 0.05)
    active2 = Active(20, 0.02)
    chain1 = Chain(active1)
    chain1.append(active2)
    chain1.gen()
    print("hello")
