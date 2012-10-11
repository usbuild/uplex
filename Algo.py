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
    priority_table = {'|': 1, '.': 2, '*': 3, '+': 3, '{': 3, '(': 0, ')': 0, 'e': 0}
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

    def getTokenList(self):
        if len(self.tokenList) == 0:
            self.midToPost()
        return self.tokenList


class FA:#行经过节点到列
    def __init__(self, param):
        if isinstance(param, Operand):
            self.graph = [[None, param], [None, None]]
        elif type(param).__name__ == 'list':
            self.graph = param

    def merge(self, fa):
        len1 = len(self.graph)
        len2 = len(fa.graph)
        totalLen = len1 + len2
        graph = []
        for row in range(0, totalLen):
            rown = []
            if row < len1:
                rown = self.graph[row]
                rown.extend([None for x in range(len1, totalLen)])
            else:
                rown = [None for x in range(0, len1)]
                rown.extend(fa.graph[row - len1])
            graph.append(rown)
        return graph

    def mergeOr(self, fa):
        graph = self.merge(fa)
        return FA(graph)

    def mergeAnd(self, fa, op):
        len1 = len(self.graph)
        len2 = len(fa.graph)
        totalLen = len1 + len2
        graph = []
        for row in range(0, totalLen):
            rown = []
            if row < len1:
                rown = self.graph[row]
                rown.extend([None for x in range(len1, totalLen)])
            else:
                rown = [None for x in range(0, len1)]
                rown.extend(fa.graph[row - len1])
            graph.append(rown)

        graph[len1 - 1][len1] = op

        return FA(graph)

    def mergeCircle(self, fa):
        graph = self.merge(fa)
        return FA(graph)

    def echo(self):
        for l in self.graph:
            for a in l:
                if a is None:
                    print 'X',
                else:
                    print a.rule,
            print ''


class NFA:
    def __init__(self, postReg):
        self.tokens = postReg.getTokenList()

    def compile(self):
        fa1 = FA(Operand('a'))
        fa2 = FA(Operand('b'))
        fa1.mergeAnd(fa2, Operand('c')).echo()


def main():
    st = '(a|[1-2])*\d{1,}'
    nfa = NFA(RE(st))
    nfa.compile()

if __name__ == '__main__':
    main()