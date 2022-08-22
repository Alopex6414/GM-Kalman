#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np


def lognorm_params(mode, stddev):
    p = np.poly1d([1, -1, 0, 0, -(stddev / mode) ** 2])
    r = p.roots
    sol = r[(r.imag == 0) & (r.real > 0)].real
    shape = np.sqrt(np.log(sol))
    scale = mode * sol
    return shape, scale


if __name__ == '__main__':
    sigma, scale = lognorm_params(1, 0.1)
    mu = np.log(scale)
    data = np.random.lognormal(mu, sigma, 10000)
    data = np.sort(data)
    # plot picture
    plt.figure()
    plt.plot(data, marker="o", linestyle="--", color="lightcoral", label="Schedule Distribution")
    plt.legend()
    plt.grid(True)
    plt.xlabel("Time")
    plt.ylabel("Number")
    plt.title("Schedule Distribution")
    plt.show()
