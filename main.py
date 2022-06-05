# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import matplotlib.pyplot as plt
from schedule import Schedule
from kalman import KalmanFilter
from gm import GM, GMControl


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # generate schedule
    t = 15
    s = Schedule(t)
    s.gen()
    print("progress(original):", s.progress)
    print("velocity(original):", s.velocity)
    # kalman filter
    kf = KalmanFilter(s.progress, s.velocity)
    kf.filter()
    print("progress(filter):", kf.X[0])
    print("velocity(filter):", kf.X[1])
    # gm = GM(kf.X, 5)
    # gm.gray_predict()
    # gm = GMControl(kf.X, 5)
    # gm.gray_predict()
    GMControl.setup_array(kf.Z)
    plt.figure()
    """Plot1 Kalman Filter"""
    plt.subplot(2, 2, 1)
    plt.plot(s.progress, 'rx--')
    plt.plot(s.velocity, 'bo:')
    plt.plot(kf.X[0, :], 'gx--')
    plt.plot(kf.X[1, :], 'yo:')
    # plt.plot(gm.G, 'mx--')
    # plot title & axis & grid label
    plt.grid(linestyle='--', linewidth=1.0)
    plt.xlabel("time")
    plt.ylabel("progress")
    plt.title("Kalman Filter")
    # predict
    """Plot3 GM Predict Control"""
    plt.subplot(2, 2, 2)
    plt.plot(kf.Z[0, :], 'gx--')
    plt.plot(kf.Z[1, :], 'yo:')
    for i in range(5, len(kf.Z[0])):
        gm = GM(kf.Z, i)
        gm.gray_predict()
        plt.plot(gm.G, 'cx--')
        gmc = GMControl(kf.Z, i, t)
        gmc.gray_predict()

    plt.plot(GMControl.X[0, :], 'mx--')
    print("progress(control):", GMControl.X[0])
    print("velocity(control):", GMControl.X[1])
    # plot title & axis & grid label
    plt.grid(linestyle='--', linewidth=1.0)
    plt.xlabel("time")
    plt.ylabel("progress")
    plt.title("GM Predict Control")
    """Plot3 Tasks Finish Time"""
    to = 0  # original finish time
    b = False
    # original finish time
    for i in range(0, len(s.progress)):
        if s.progress[i] >= 1.:
            b = True
            to = i
            break
    if not b:
        print("Can not get original finish time")
    # control finish time
    tc = 0  # control finish time
    b = False
    for i in range(0, len(GMControl.X[0, :])):
        if GMControl.X[0, i] >= 1.:
            b = True
            tc = i
            break
    if not b:
        print("Can not get control finish time")
    plt.subplot(2, 2, 3)
    plt.bar("original", to)
    plt.bar("control", tc)
    # plot title & axis & grid label
    plt.grid(linestyle='--', linewidth=1.0)
    plt.xlabel("methods")
    plt.ylabel("time")
    plt.title("Task Finish Time")
    # plot show
    plt.show()
    print('hello')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
