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


if __name__ == '__main__':
    pass
