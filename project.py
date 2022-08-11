#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from schedule import Schedule
from kalman import KalmanFilter


class Active(object):
    def __init__(self, period, sigma=0.05) -> None:
        self.schedule = Schedule(period, sigma)
        self.schedule.gen()
        self.kalman = KalmanFilter(self.schedule.progress, self.schedule.velocity)
        self.kalman.filter()
        self.next = None


class Chain(object):
    def __init__(self, active=None) -> None:
        self.head = active
        self.period = None
        self.actual = None

    def is_empty(self):
        return self.head is None

    def length(self):
        cur = self.head
        count = 0
        while cur is not None:
            count += 1
            cur = cur.next
        return count

    def append(self, active):
        if self.is_empty():
            self.head = active
        else:
            cur = self.head
            while cur.next is not None:
                cur = cur.next
            cur.next = active

    def add(self, active):
        node = active
        node.next = self.head
        self.head = node

    def insert(self, pos, active):
        if pos <= 0:
            self.add(active)
        elif pos > self.length() - 1:
            self.append(active)
        else:
            pre = self.head
            count = 0
            while count < pos - 1:
                count += 1
                pre = pre.next
            node = active
            node.next = pre.next
            pre.next = node

    def gen(self):
        cur = self.head
        self.period = 0
        self.actual = 0
        while cur is not None:
            self.period += cur.schedule.period
            self.actual += cur.schedule.actual
            cur = cur.next


class Project(object):
    def __init__(self) -> None:
        pass


if __name__ == '__main__':
    active1 = Active(15, 0.05)
    active2 = Active(20, 0.02)
    chain1 = Chain(active1)
    chain1.append(active2)
    chain1.gen()
    print("hello")
