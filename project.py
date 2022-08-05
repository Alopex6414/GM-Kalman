#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from list import Node, LinkList
from schedule import Schedule


class Active(Node):
    def __init__(self, period, sigma=0.05) -> None:
        self.schedule = Schedule(period, sigma)
        super(Active, self).__init__(period)


class Chain(LinkList):
    def __init__(self, active):
        super(Chain, self).__init__(active)

    def is_empty(self):
        super(Chain, self).is_empty()

    def travel(self):
        super(Chain, self).travel()

    def length(self):
        super(Chain, self).length()

    def append(self, item):
        super(Chain, self).append(item)

    def add(self, item):
        super(Chain, self).add(item)

    def insert(self, pos, item):
        super(Chain, self).insert(pos, item)


class Project(object):
    def __init__(self) -> None:
        pass


if __name__ == '__main__':
    active1 = Active(15, 0.05)
    active2 = Active(20, 0.25)
    chain1 = Chain(active1)
    chain1.append(active2)
    print("hello")
