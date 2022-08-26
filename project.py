#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from experiment import ExperimentSingle


class Active(object):
    def __init__(self, period, buffer, sigma=0.05) -> None:
        self.active = ExperimentSingle(period, buffer)
        self.next = None

    def simulate(self):
        self.simulate()


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

    def simulate(self):
        cur = self.head
        while cur is not None:
            cur.active.simulate()
            cur = cur.next


class Project(object):
    def __init__(self) -> None:
        pass


if __name__ == '__main__':
    active1 = Active(15, 3, 0.05)
    active2 = Active(20, 5, 0.02)
    active3 = Active(9, 3, 0.05)
    chain1 = Chain(active1)
    chain1.append(active2)
    chain1.append(active3)
    chain1.simulate()
    print("hello")
