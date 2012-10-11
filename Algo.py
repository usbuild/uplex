#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class Operand:
    def __init__(self, input_chr):
        self.rule = input_chr

class Operator:

    def __init__(self, input_chr):
        self.rule = input_chr

    def validate(self, char):
        return True

class RE:
    def __init__(self, input_str):
        self.input = input_str
        self.post_stack = []
        self.tokenList = []

    @classmethod
    def isOperand(cls, num):
        num = str(num)
        if num.isalpha() or num.isalnum():
            return True
        return False

    @classmethod
    def readToken(cls, tokenList):
        if cls.isOperand(tokenList[0]):
            oper = Operand(tokenList[0])
        else:
            oper = Operator(tokenList[0])
        tokenList.pop(0)
        return (oper, tokenList)#(token,返回的list)

    def midToPost(self):
        single = ('*', '+')
        pritable = {'|': 1, '.': 2, '*': 3, '+': 3, '(': 0, ')': 0}
        prechar = False
        opstack = []
        midfix = list(self.input)

        while len(midfix) > 0:
            (oper, midfix) = self.readToken(midfix)

            if isinstance(oper, Operand):
                if prechar:
                    midfix.insert(0, oper.rule)
                    midfix.insert(0,'.')
                else:
                    self.post_stack.append(oper.rule)
                    self.tokenList.append(oper)
                prechar = True
            else:
                prechar = False
                if oper.rule == '(':
                    opstack.append(oper.rule)
                elif oper.rule == ')':
                    while True:
                        c = opstack.pop()
                        if c == '(':
                            break
                        else:
                            self.post_stack.append(c)
                else:
                    if oper.rule in single:
                        prechar = True
                    while len(opstack) != 0:
                        if pritable[oper.rule] <= pritable[opstack[-1]]:
                            self.post_stack.append(opstack.pop())
                        else:
                            break
                    opstack.append(oper.rule)
        while len(opstack) != 0:
            self.post_stack.append(opstack.pop())

def main():
    st = '(a|b)'
    r = RE(st)
    r.midToPost()
    print r.post_stack

if __name__ == '__main__':
    main()