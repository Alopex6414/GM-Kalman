#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from schedule import Schedule


class Active(object):
    def __init__(self, period, sigma=0.05) -> None:
        self.schedule = Schedule(period, sigma)
        self.next = None


class Chain(object):
    def __init__(self, active=None) -> None:
        self.head = active
        self.period = None
        self.actual = None

    def is_empty(self):
        return self.head is None

    def append(self, active):
        if self.is_empty():
            self.head = active
        else:
            cur = self.head
            while cur.next is not None:
                cur = cur.next
            cur.next = active

    def gen(self):
        cur = self.head
        self.period = 0
        self.actual = 0
        while cur is not None:
            cur.schedule.gen()
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
