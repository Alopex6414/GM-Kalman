#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import copy


class GM(object):
    def __init__(self, array, buffer, n):
        """
        :param array: project schedule progress status array (numpy array type) (2x2)
        :param buffer: project schedule progress feeding or project buffer
        :param n: project schedule progress status array actual length
        """
        self.array = array
        self.buffer = buffer
        self.D0 = self.array[0, 0:n]
        self.D1 = np.zeros(len(self.D0))
        self.Z1 = np.zeros(len(self.D0))
        self.F = np.zeros(len(self.array[0]))
        self.G = np.zeros(len(self.array[0]))
        self.L = np.zeros(len(self.D0))  # ratio check
        self.a = None  # gray develop coefficient
        self.b = None  # gray offset
        self.c = None  # gray matrix
        self.E = None  # epsilon array
        self.Ebar = None  # epsilon average
        self.Eeva = None  # evaluate model (epsilon)
        self.R = None  # rou array
        self.Rbar = None  # rou average
        self.Reva = None  # evaluate model (rou)
        self.S = None  # variance proportion
        self.P = None  # small probability

    def _ratio_check(self):
        lamb = np.zeros(len(self.D0))
        lower = np.exp(-2 / (len(self.D0) + 1))
        upper = np.exp(2 / (len(self.D0) + 1))
        # ratio calculate
        for i in range(1, len(self.D0)):
            lamb[i] = self.D0[i - 1]/self.D0[i]
        lamb = lamb[1:len(lamb)]
        self.L = lamb
        # ratio check
        b = True
        n = 0
        for i in range(0, len(lamb)):
            if lamb[i] < lower or lamb[i] > upper:
                b = False
                n = i
                break
        return b, n

    def _error_check(self):
        # remain error check
        G0 = self.G[1:len(self.D0)]
        for i in range(1, len(self.D0)):
            if self.D0[i] == 0.:
                self.D0[i] = 0.0001
        self.E = np.abs(self.D0[1:] - G0) / self.D0[1:]
        self.Ebar = np.mean(self.E)
        # evaluate model accuracy (epsilon)
        if self.Ebar < 0.1:
            self.Eeva = "E model evaluate result very good."
        elif self.Ebar < 0.2:
            self.Eeva = "E model evaluate result can be accepted."
        else:
            self.Eeva = "E model evaluate result can not be accepted."
        # ratio proportion error check
        lamb = np.zeros(len(self.D0))
        # ratio calculate
        for i in range(1, len(self.D0)):
            lamb[i] = self.D0[i - 1] / self.D0[i]
        lamb = lamb[1:len(lamb)]
        self.R = np.zeros(len(lamb))
        for i in range(0, len(lamb)):
            self.R[i] = 1. - (1. - 0.5 * self.a) / (1. + 0.5 * self.a) * lamb[i]
        self.Rbar = np.mean(self.R[1:len(self.E)])
        # evaluate model accuracy (rou)
        if self.Rbar < 0.1:
            self.Reva = "R model evaluate result very good."
        elif self.Rbar < 0.2:
            self.Reva = "R model evaluate result can be accepted."
        else:
            self.Reva = "R model evaluate result can not be accepted."
        # variance ratio proportion error check
        self.S = np.var(self.E) / np.var(self.D0[1:len(self.D0)])
        # small probability error check
        std = np.std(self.D0[1:len(self.D0)])
        count = 0
        for i in range(0, len(self.E)):
            if self.E[i] <= std:
                count = count + 1
        self.P = count / len(self.E[1:])

    def gray_predict(self):
        # pre-condition before ratio check
        self.D0 = self.D0 + 1
        # ratio check for origin sequence
        b, n = self._ratio_check()
        """
        if not b:
            print("Ratio check not pass: array[{}]".format(n))
            return
        """
        # sequence cumulative generation
        self.D1 = np.cumsum(self.D0)
        # sequence next-to-average generation
        for i in range(1, len(self.D0)):
            self.Z1[i] = (self.D1[i] + self.D1[i - 1]) / 2
        self.Z1 = self.Z1[1:len(self.Z1)]
        # construct data matrix B
        B = np.array([-self.Z1[0:len(self.Z1)], np.ones(len(self.Z1))])
        # construct result matrix Y
        Y = np.transpose(np.array([self.D0[1:len(self.D0)]]))
        # calculate coefficient matrix C
        self.c = np.dot(np.dot(np.linalg.inv(np.dot(B, B.T)), B), Y)
        self.c = np.transpose(self.c)
        self.a = self.c[0, 0]
        self.b = self.c[0, 1]
        # predictive curve fitting
        for i in range(0, len(self.array[0])):
            self.F[i] = (self.D0[1] - self.b / self.a) / np.exp(self.a * i) + self.b / self.a
        # restore the original prediction array
        self.G[0] = self.F[0]
        for i in range(1, len(self.array[0])):
            self.G[i] = self.F[i] - self.F[i - 1]
        # restore pre-condition
        # self.G[0] = self.D0[0]
        self.G = self.G - 1
        self.D0 = self.D0 - 1
        # error check for predict sequence
        self._error_check()

    def gray_predict2(self):
        """Use latest 5 times data to calculate GM prediction result"""
        # pre-condition before ratio check
        self.D0 = self.D0 + 1
        # ratio check for origin sequence
        b, n = self._ratio_check()
        """
        if not b:
            print("Ratio check not pass: array[{}]".format(n))
            return
        """
        # sequence cumulative generation
        self.D1 = np.cumsum(self.D0)
        for i in range(1, len(self.D0)):
            self.Z1[i] = (self.D1[i] + self.D1[i - 1]) / 2
        self.Z1 = self.Z1[1:len(self.Z1)]
        # construct data matrix B
        B = np.array([-self.Z1[-4:], np.ones(4)])
        # construct result matrix Y
        Y = np.transpose(np.array([self.D0[-4:]]))
        # calculate coefficient matrix C
        self.c = np.dot(np.dot(np.linalg.inv(np.dot(B, B.T)), B), Y)
        self.c = np.transpose(self.c)
        self.a = self.c[0, 0]
        self.b = self.c[0, 1]
        # predictive curve fitting
        for i in range(0, len(self.array[0])):
            self.F[i] = (self.D0[-4] - self.b / self.a) / np.exp(self.a * i) + self.b / self.a
        # restore the original prediction array
        self.G[0] = self.F[0]
        for i in range(1, len(self.array[0])):
            self.G[i] = self.F[i] - self.F[i - 1]
        # restore pre-condition
        self.G[0] = self.G[1]
        self.G = self.G - 1
        self.D0 = self.D0 - 1
        # error check for predict sequence
        self._error_check()


class GMControl(GM):
    X = None

    def __init__(self, array, buffer, n, t):
        """
        :param array: project schedule progress status array (numpy array type) (2x2)
        :param buffer: project schedule progress feeding or project buffer
        :param n: project schedule progress status array actual length
        :param t: project schedule progress periodic
        """
        super(GMControl, self).__init__(array, buffer, n)
        self.t = t
        self.t_safe = t + buffer

    @staticmethod
    def setup_array(array):
        GMControl.X = copy.deepcopy(array)

    def gray_predict(self):
        super(GMControl, self).gray_predict()
        # whether prediction will have delay?
        if len(self.D0) < self.t:
            if self.G[self.t] < 1.:
                # check active predict with buffer
                index = -1
                if self.t_safe < len(self.G):
                    index = self.t_safe
                # control progress...
                if self.G[index] < 1.:
                    GMControl.X[1, len(self.D0)] = GMControl.X[1, len(self.D0)] + 0.75 * (1. - self.G[self.t])
                else:
                    GMControl.X[1, len(self.D0)] = GMControl.X[1, len(self.D0)] + 0.5 * (1. - self.G[self.t])
                # print(len(self.D0))
        else:
            if self.G[-1] < 1.:
                # check active predict with buffer
                index = -1
                if self.t_safe < len(self.G):
                    index = self.t_safe
                # control progress...
                if self.G[index] < 1.:
                    GMControl.X[1, len(self.D0)] = GMControl.X[1, len(self.D0)] + 0.75 * (1. - self.G[-1])
                else:
                    GMControl.X[1, len(self.D0)] = GMControl.X[1, len(self.D0)] + 0.5 * (1. - self.G[-1])
                # print(len(self.D0))
        # update current progress
        GMControl.X[0, len(self.D0)] = GMControl.X[0, len(self.D0) - 1] + GMControl.X[1, len(self.D0) - 1]
        if GMControl.X[0, len(self.D0)] > 1.:
            GMControl.X[0, len(self.D0)] = 1.

    def gray_predict2(self):
        super(GMControl, self).gray_predict2()
        # whether prediction will have delay?
        if len(self.D0) < self.t:
            if self.G[self.t] < 1.:
                GMControl.X[1, len(self.D0)] = GMControl.X[1, len(self.D0)] + 0.5 * (1. - self.G[self.t])
                # print(len(self.D0))
        else:
            if self.G[-1] < 1.:
                GMControl.X[1, len(self.D0)] = GMControl.X[1, len(self.D0)] + 0.5 * (1. - self.G[-1])
                # print(len(self.D0))
        # update current progress
        GMControl.X[0, len(self.D0)] = GMControl.X[0, len(self.D0) - 1] + GMControl.X[1, len(self.D0) - 1]
        if GMControl.X[0, len(self.D0)] > 1.:
            GMControl.X[0, len(self.D0)] = 1.


if __name__ == '__main__':
    pass
