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
    plt.plot(s.progress, 'rx--')
    plt.plot(s.velocity, 'bo:')
    # plt.plot(kf.X[0, :], 'gx--')
    # plt.plot(kf.X[1, :], 'yo:')
    # plt.plot(gm.G, 'mx--')
    # test
    for i in range(5, len(kf.Z[0])):
        gm = GM(kf.Z, i)
        gm.gray_predict()
        plt.plot(gm.G, 'cx--')
        gmc = GMControl(kf.Z, i, t)
        gmc.gray_predict()

    plt.plot(GMControl.X[0, :], 'mx--')
    print("progress(control):", GMControl.X[0])
    print("velocity(control):", GMControl.X[1])
    # plot title & axis label
    plt.xlabel("time")
    plt.ylabel("progress")
    plt.title("GM-Kalman Simulation")

    # plot grid
    plt.grid(linestyle='--', linewidth=1.0)

    plt.show()
    print('hello')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
