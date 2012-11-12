#!/usr/bin/env python
# -*- coding: UTF-8 -*-
pack= [([0, 1, 2, 3, 4, 5, 6, 7], [[(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6), (10, 4)], [(14, 2)], [(12, 7)], [(13, 1)], [(11, 5)], [(12, 3)], [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7), (9, 7)], []], ['8', '9', '6', '7', '4', '5', '2', '3', '0', '1', 'i', 'f', 'e', 'l', 's'], 0, [6, 7]), ([0, 1, 2], [[(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1)], [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2)], []], ['8', '9', '6', '7', '4', '5', '2', '3', '0', '1'], 0, [1, 2]), ([0, 1, 2, 3, 4, 5, 6], [[(0, 4)], [(4, 2)], [(2, 6)], [(3, 1)], [(1, 5)], [(2, 3)], []], ['i', 'f', 'e', 'l', 's'], 0, [6])]






class DFAPack:
    def __init__(self, pack):
        self.graph, self.trans, self.oplist, self.start, self.end = pack

    def getNext(self, state, edge):
        trans = self.trans[state]
        try:
            idx = self.oplist.index(edge)
        except:
            return None
        for (x, y) in trans:
            if x == idx:
                return y
        return None
    def isEnd(self, s):
        return s in self.end


class DFAInstance:
    def __init__(self, pack, input_str):
        self.pack = pack
        self.state = pack.start
        self.input = input_str

    def validate(self):
        state = self.state
        i = 0
        for s in self.input:
            state = self.pack.getNext(state, s)
            if state is None:
                return self.input[0:i]
            i += 1
        if self.pack.isEnd(state):
            return self.input
        else:
            return ''


class REList:
    def __init__(self, pack):
        self.pack = [DFAPack(x) for x in pack]

    def validate(self, line):
        i = 0
        max_len = 0
        while i < len(self.pack):
            if i == 0:
                max_len = len(DFAInstance(self.pack[i], line).validate())
                if max_len == 0: return (0, None)
            else:
                if len(DFAInstance(self.pack[i], line).validate()) == max_len:
                    return (max_len, i)
            i += 1


def main():
    print REList(pack).validate('12457')


if __name__ == '__main__':
    main()
