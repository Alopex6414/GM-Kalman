#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from list import Node
from schedule import Schedule


class Active(Node):
    def __init__(self, period, sigma=0.05) -> None:
        self.schedule = Schedule(period, sigma)
        super().__init__(period)


class Project(object):
    def __init__(self) -> None:
        pass


if __name__ == '__main__':
    pass
