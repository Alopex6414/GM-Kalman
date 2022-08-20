#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    data = np.random.lognormal(1, 1, 10000)
    print(data)
    # plot picture
    plt.figure()
    plt.plot(data, marker="o", linestyle="--", color="lightcoral", label="Schedule Distribution")
    plt.legend()
    plt.grid(True)
    plt.xlabel("Time")
    plt.ylabel("Number")
    plt.title("Schedule Distribution")
    plt.show()
