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
        self.len = len(self.D0)
        self.a = None  # gray develop coefficient
        self.b = None  # gray offset
        self.c = None  # gray matrix

    def _ratio_check(self):
        lamb = np.zeros(self.len)
        lower = np.exp(-2 / (self.len + 1))
        upper = np.exp(2 / (self.len + 1))
        # ratio calculate
        for i in range(1, self.len):
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
        # ratio check for origin serials
        b, n = self._ratio_check()
        if not b:
            print("Ratio check not pass: array[{}]".format(n))
            return


if __name__ == '__main__':
    pass
