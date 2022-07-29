#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Node(object):
    def __init__(self, value) -> None:
        self.value = value
        self.next = None


class Linklist(object):
    def __init__(self, node=None) -> None:
        self.head = None
    
    def is_empty(self):
        return self.head == None
    
    def travel(self):
        cur = self.head
        while cur != None:
            print(cur.value)
            cur = cur.next
    
    def length(self):
        cur = self.head
        count = 0
        while cur != None:
            count += 1
            cur = cur.next
        return count



if __name__ == '__main__':
    pass
