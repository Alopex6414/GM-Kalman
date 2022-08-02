#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Node(object):
    def __init__(self, value) -> None:
        self.value = value
        self.next = None


class LinkList(object):
    def __init__(self, node=None) -> None:
        self.head = None

    def is_empty(self):
        return self.head is None

    def travel(self):
        cur = self.head
        while cur is not None:
            print(cur.value)
            cur = cur.next

    def length(self):
        cur = self.head
        count = 0
        while cur is not None:
            count += 1
            cur = cur.next
        return count

    def append(self, item):
        node = Node(item)
        if self.is_empty():
            self.head = node
        else:
            cur = self.head
            while cur.next is not None:
                cur = cur.next
            cur.next = node

    def add(self, item):
        node = Node(item)
        node.next = self.head
        self.head = node

    def insert(self, pos, item):
        if pos <= 0:
            self.add(item)
        elif pos > self.length() - 1:
            self.append(item)
        else:
            pre = self.head
            count = 0
            while count < pos - 1:
                count += 1
                pre = pre.next
            node = Node(item)
            node.next = pre.next
            pre.next = node

    def search(self, item):
        cur = self.head
        while cur is None:
            if cur.value == item:
                return True
            else:
                cur = cur.next
        return False

    def remove(self, item):
        cur = self.head
        if cur.value == item:
            self.head = cur.next
        else:
            while cur.next.value != item:
                cur = cur.next
            cur.next = cur.next.next


if __name__ == '__main__':
    pass
