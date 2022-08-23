#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import lognorm


if __name__ == '__main__':
    s = 0.954
    mean, var, skew, kurt = lognorm.stats(s, moments='mvsk')
    x = np.linspace(lognorm.ppf(0.01, s), lognorm.ppf(0.99, s), 100)
    r = lognorm.rvs(s, size=1000)
    # plot picture
    plt.figure()
    plt.plot(r, marker="o", linestyle="--", color="lightcoral", label="Schedule Distribution")
    plt.legend()
    plt.grid(True)
    plt.xlabel("Time")
    plt.ylabel("Number")
    plt.title("Schedule Distribution")
    plt.show()
