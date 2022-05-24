# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import matplotlib.pyplot as plt
from schedule import Schedule
from kalman import KalmanFilter


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    s = Schedule(15)
    s.gen()
    kf = KalmanFilter(s.progress, s.velocity)
    kf.filter()
    print("progress:", s.progress)
    print("velocity:", s.velocity)
    plt.figure()
    plt.plot(s.progress, 'rx--')
    plt.plot(s.velocity, 'bo')
    plt.plot(kf.X[0, :], 'gx--')
    plt.plot(kf.X[1, :], 'yo')
    plt.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
