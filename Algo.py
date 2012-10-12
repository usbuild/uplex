#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from Queue import Queue

class Operand:
    def __init__(self, input_chr):
        if type(input_chr).__name__ == 'list':
            self.rule = ''.join(input_chr)
        else:
            self.rule = input_chr

    def validate(self, char):
        return True

    @staticmethod
    def getEEdge():
        return Operand('e')

    def isEEdge(self):
        return self.rule == 'e'

    def __eq__(self, other):
        return self.rule == other.rule


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

    def isOr(self):
        return self.rule == '|'

    def isAnd(self):
        return self.rule == '.'

    def isCircle(self):
        return self.rule == '*'


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


class FA:
    def __init__(self, param):
        if type(param).__name__ == 'list':
            self.graph = param
        elif isinstance(param, Operand):
            self.graph = [[(param, 1)], []]

    def getOperandList(self):
        operandList = []
        for l in self.graph:
            for x, y in l:
                if not x.isEEdge() and x not in operandList:
                    operandList.append(x)

        return operandList

    def getEndState(self):
        return len(self.graph) - 1

    def merge(self, fa):
        len1 = len(self.graph)
        graph = list(self.graph)
        graph.extend([[(x, y + len1) for x, y in l] for l in fa.graph])
        return graph

    def expand(self):
        graph = [[(x, y + 1) for x, y in l] for l in self.graph]
        graph.insert(0, [])
        graph.append([])
        return graph

    def mergeAnd(self, fa):
        graph = self.merge(fa)
        len1 = len(self.graph)
        graph[len1 - 1].append((Operand.getEEdge(), len1))
        return FA(graph)

    def mergeOr(self, fa):
        graph = FA(self.merge(fa)).expand()
        len1 = len(self.graph)
        len2 = len(fa.graph)
        graph[0].extend([(Operand.getEEdge(), 1), (Operand.getEEdge(), len1 + 1)])
        graph[len1].append((Operand.getEEdge(), len1 + len2 + 1))
        graph[len1 + len2].append((Operand.getEEdge(), len1 + len2 + 1))
        return FA(graph)

    def mergeCircle(self):
        graph = self.expand()
        len1 = len(self.graph)
        graph[0].append((Operand.getEEdge(), 1))
        graph[len1].append((Operand.getEEdge(), len1 + 1))

        graph[len1].append((Operand.getEEdge(), 1))
        graph[0].append((Operand.getEEdge(), len1 + 1))
        return FA(graph)

    def echo(self):
        for l in self.graph:
            print self.graph.index(l), [(x.rule, y) for x, y in l]


class NFA:
    def __init__(self, postReg):
        self.tokens = postReg.getTokenList()

    def compile(self):
        nfaStack = []
        for token in self.tokens:
            if isinstance(token, Operand):
                nfaStack.append(FA(token))
            else:
                if token.isCircle():
                    nfaStack.append(nfaStack.pop().mergeCircle())
                elif token.isOr():
                    nfa2 = nfaStack.pop()
                    nfa1 = nfaStack.pop()
                    nfaStack.append(nfa1.mergeOr(nfa2))
                elif token.isAnd():
                    nfa2 = nfaStack.pop()
                    nfa1 = nfaStack.pop()
                    nfaStack.append(nfa1.mergeAnd(nfa2))
        return nfaStack


class DFA:
    def __init__(self, nfa):
        self.nfa = nfa.compile()[0]

    def closure(self, state):
        q = Queue()
        result = []
        if type(state).__name__ == 'list':
            for l in state:
                q.put(l)
        else:
            q.put(state)

        while q.empty() == False:
            state = q.get()
            if state not in result:
                result.append(state)
                for x, y in self.nfa.graph[state]:
                    if x.isEEdge():
                        q.put(y)
        return result

    def move(self, state, edge):
        q = Queue()
        result =[]

        orgin = list(state)
        for l in state:
            q.put(l)

        while q.empty() == False:
            state = q.get()
#            if state not in result:
            result.append(state)
            for x, y in self.nfa.graph[state]:
                if x == edge:
                    q.put(y)
        for s in orgin:
            result.remove(s)
        return result

    def getStates(self):
        dfaStateID = []
        dfaState = []
        opList = self.nfa.getOperandList()
        endState = self.nfa.getEndState()
        endStates = []
        q = Queue()
        start = self.closure(0)
        q.put(start)
#        self.nfa.echo()
        dfaState.append(start)
        while q.empty() == False:
            state = []
            curCol = q.get()
            for op in opList:
                col = self.closure(self.move(curCol, op))
                if col not in dfaState:
                    if len(col) == 0:
                        state.append(None)
                    else:
                        dfaState.append(col)
                        state.append(len(dfaState) - 1)
                        if endState in col:
                            endStates.append(len(dfaState) - 1)
                        q.put(col)
                else:
                    state.append(dfaState.index(col))
            dfaStateID.append(state)

        startStates = []

        for s in range(0, len(dfaStateID)):
            if s not in endStates:
                startStates.append(s)

        cutStates = [startStates, endStates]
        print self.minimize(cutStates, dfaStateID)
        print dfaState
        return dfaStateID, dfaState

    def cmpList(self, list1, list2):
        if len(list1) != len(list2):
            return False
        for l in list2:
            if l not in list2:
                return False
        return True

    def minimize(self, cutStates, trans):
        change = True#多次划分防止遗漏，向后看
        while change:
            change = False
            oldState = list(cutStates)

            for i in range(0, len(self.nfa.getOperandList())):
                for l in cutStates:
                    x = 0
                    if len(l) == 1:
                        continue
                    newStates = {}
                    unique = 0
                    while x < len(l):
                        next = trans[l[x]][i]
                        if next is None:
                            unique -= 1
                            newStates[unique] = [l[x]]

                        elif next not in l:
                            if newStates.has_key(next) == False:
                                newStates[next] = []
                            newStates[next].append(l[x])
                        x += 1

                    if len(newStates) == 0:
                        continue
                    cutStates.remove(l)
                    for key in newStates.keys():
                        if newStates[key] not in cutStates:
                            cutStates.append(newStates[key])
                        for st in newStates[key]:
                            l.remove(st)
                    if len(l) > 0:
                        cutStates.insert(0, l)

            if self.cmpList(oldState, cutStates) == False:
                change = True
        return cutStates




def main():
    st = '(a|b)*abc'
    nfa = NFA(RE(st))
    states = DFA(nfa).getStates()

if __name__ == '__main__':
    main()