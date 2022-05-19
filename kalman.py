#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    arr1 = np.random.random(10)
    print("arr1:{}", arr1)
    plt.figure()
    plt.plot(arr1)
    plt.show()
    pass
