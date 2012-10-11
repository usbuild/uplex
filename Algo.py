#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class Operand:
    def __init__(self, input_chr):
        if type(input_chr).__name__ == 'list':
            self.rule = ''.join(input_chr)
        else:
            self.rule = input_chr

    def validate(self, char):
        return True


class Operator:
    priority_table = {'|': 1, '.': 2, '*': 3, '+': 3, '{': 3, '(': 0, ')': 0}
    single = ('*', '+')

    def __init__(self, input_chr):
        if type(input_chr).__name__ == 'list':
            self.rule = ''.join(input_chr)
        else:
            self.rule = input_chr
        self.priority = self.priority_table[input_chr[0]]

    def isLeftBracket(self):
        return self.rule == '('

    def isRightBracket(self):
        return self.rule == ')'

    def isSingle(self):
        return self.rule in self.single


class RE:
    def __init__(self, input_str):
        self.input = input_str
        self.tokenList = []

    @classmethod
    def isOperand(cls, num):
        num = str(num)
        if num.isalpha() or num.isalnum():
            return True
        return False

    @classmethod
    def readToken(cls, tokenList):
        if isinstance(tokenList[0], Operator) or isinstance(tokenList[0], Operand):
            return tokenList[0], tokenList[1:]

        if tokenList[0] == '{':
            endPos = tokenList.index('}')
            oper = Operator(tokenList[0:endPos + 1])
            if endPos == len(tokenList) - 1:
                return oper, ''
            return oper, tokenList[tokenList.index('}') + 1:]

        if tokenList[0] == '[':
            endPos = tokenList.index(']')
            oper = Operand(tokenList[0:endPos + 1])
            if endPos == len(tokenList) - 1:
                return oper, ''
            return oper, tokenList[tokenList.index(']') + 1:]

        if tokenList[0] == '\\':
            return Operand(tokenList[0:2]), tokenList[2:]

        if cls.isOperand(tokenList[0]):
            oper = Operand(tokenList[0])
        else:
            oper = Operator(tokenList[0])
        return oper, tokenList[1:]#(token,返回的list)

    def midToPost(self):
        prechar = False
        opstack = []
        midfix = list(self.input)
        while len(midfix) > 0:
            (oper, midfix) = self.readToken(midfix)
            if isinstance(oper, Operand):
                if prechar:
                    midfix.insert(0, oper)
                    midfix.insert(0, Operator('.'))
                    prechar = False
                else:
                    self.tokenList.append(oper)
                    prechar = True
            else:
                prechar = False
                if oper.isLeftBracket():
                    opstack.append(oper)
                elif oper.isRightBracket():
                    while True:
                        c = opstack.pop()
                        if c.isLeftBracket():
                            break
                        else:
                            self.tokenList.append(c)
                else:
                    if oper.isSingle():
                        prechar = True
                    while len(opstack) != 0:
                        if oper.priority <= opstack[-1].priority:
                            self.tokenList.append(opstack.pop())
                        else:
                            break
                    opstack.append(oper)
        while len(opstack) != 0:
            self.tokenList.append(opstack.pop())


def main():
    st = '(a|[1-2])*\d{1,}'
    r = RE(st)
    r.midToPost()
    print [(s.rule, isinstance(s, Operator)) for s in r.tokenList]

if __name__ == '__main__':
    main()