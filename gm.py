#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class GM(object):
    def __init__(self, status):
        """
        :param status: project schedule progress status (numpy array type)
        """
        self.status = status
        self.a = None  # gray develop coefficient
        self.b = None  # gray offset


if __name__ == '__main__':
    pass
