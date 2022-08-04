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

    def append(self, item):
        super(Chain, self).append(item)


class Project(object):
    def __init__(self) -> None:
        pass


if __name__ == '__main__':
    active1 = Active(15, 0.05)
    active2 = Active(20, 0.25)
    chain1 = Chain(active1)
    chain1.append(active2)
    print("hello")
