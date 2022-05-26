#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np


class GM(object):
    def __init__(self, array, n):
        """
        :param array: project schedule progress status array (numpy array type) (2x2)
        :param n: project schedule progress status array actual length
        """
        self.array = array
        self.D0 = self.array[0, 0:n]
        self.D1 = np.zeros(len(self.D0))
        self.Z1 = np.zeros(len(self.D0))
        self.F = np.zeros(len(self.array[0]))
        self.G = np.zeros(len(self.array[0]))
        self.a = None  # gray develop coefficient
        self.b = None  # gray offset
        self.c = None  # gray matrix

    def _ratio_check(self):
        lamb = np.zeros(len(self.D0))
        lower = np.exp(-2 / (len(self.D0) + 1))
        upper = np.exp(2 / (len(self.D0) + 1))
        # ratio calculate
        for i in range(1, len(self.D0)):
            lamb[i] = self.D0[i - 1]/self.D0[i]
        lamb = lamb[1:len(lamb)]
        # ratio check
        b = True
        n = 0
        for i in range(0, len(lamb)):
            if lamb[i] < lower or lamb[i] > upper:
                b = False
                n = i
                break
        return b, n

    def gray_predict(self):
        # pre-condition before ratio check
        self.D0 = self.D0 + 1
        # ratio check for origin sequence
        b, n = self._ratio_check()
        if not b:
            print("Ratio check not pass: array[{}]".format(n))
            return
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
        self.F[0] = self.D0[0]
        self.F[1] = self.D0[1]
        for i in range(2, len(self.array[0])):
            self.F[i] = (self.D0[1] - self.b / self.a) / np.exp(self.a * (i - 1)) + self.b / self.a
        # restore the original prediction array
        self.G[0] = self.F[0]
        self.G[1] = self.F[1]
        for i in range(2, len(self.array[0])):
            self.G[i] = self.F[i] - self.F[i - 1]
        # restore pre-condition
        self.G = self.G - 1


if __name__ == '__main__':
    pass
