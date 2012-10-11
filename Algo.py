#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def isopnum(num):
    num = str(num)
    if num.isalpha() or num.isalnum():
        return True
    return False


def midtopost(midfix):
    single = ('*', '+')
    pritable = {'|': 1, '.': 2, '*': 3, '+': 3, '(': 0, ')': 0}
    prechar = False
    opstack = []
    midfix = list(midfix)

    while len(midfix) > 0:
        char = midfix.pop(0)

        if isopnum(char):
            if prechar:
                midfix.insert(0, char)
                midfix.insert(0,'.')
            else:
                print char,
            prechar = True
        else:
            prechar = False
            if char == '(':
                opstack.append(char)
            elif char == ')':
                while True:
                    c = opstack.pop()
                    if c == '(':
                        break
                    else:
                        print c,
            else:
                if char in single:
                    prechar = True
                while len(opstack) != 0:
                    if pritable[char] <= pritable[opstack[-1]]:
                        print opstack.pop(),
                    else:
                        break
                opstack.append(char)
    while len(opstack) != 0:
        print opstack.pop(),


def main():
    midtopost('(a|b)*a')

if __name__ == '__main__':
    main()