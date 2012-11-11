#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from Queue import Queue

class Operand:
    special = ('|', '.', ']', '[', '+', '*', '?', '(', ')', '\\', '^', '{', '}')
    E = 0
    DOT = 1
    WORD = 2
    DIGIT = 3
    SPACE = 4

    def __init__(self, input_chr):
        if type(input_chr).__name__ == 'list':
            input_chr = ''.join(input_chr)
        if input_chr == '.':
            self.rule = self.DOT
        elif input_chr == '\w':
            self.rule = self.WORD
        elif input_chr == '\d':
            self.rule = self.DIGIT
        elif input_chr == '\s':
            self.rule = self.SPACE
        elif input_chr == self.E:
            self.rule = self.E
        elif input_chr[0] == '\\' and input_chr[1] in self.special:
            self.rule = input_chr[1:]
        else:
            self.rule = input_chr

    @staticmethod
    def getEEdge():
        return Operand(0)

    def isEEdge(self):
        return self.rule == self.E

    def __eq__(self, other):
        return self.rule == other.rule


class Operator:
    priority_table = {'|': 1, '.': 2, '*': 3, '+': 3, '?': 3, '{': 3, '(': 0, ')': 0, 'e': 0}
    single = ('*', '+', '?')

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
        if self.isPeriod():
            return True
        return self.rule in self.single

    def isOr(self):
        return self.rule == '|'

    def isAnd(self):
        return self.rule == '.'

    def isCircle(self):
        return self.rule == '*'

    def isEONE(self):
        return self.rule == '?'

    def isPlus(self):
        return self.rule == '+'

    def isPeriod(self):
        return self.rule[0] == '{'

    def getPeriod(self):
        data = self.rule[1:-1]
        start, end = tuple(data.split(','))
        start = start.strip()
        end = end.strip()
        if len(start) == 0:
            start = 0
        else:
            start = int(start)

        if len(end) == 0:
            end = None
        else:
            end = int(end)
        return start, end


class RE:
    def __init__(self, input_str):
        self.input = input_str
        self.tokenList = []

    @classmethod
    def isOperand(cls, num):
        num = str(num)
        if num not in Operand.special or num in ('.'):
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
                if not oper.isLeftBracket():
                    prechar = False
                if oper.isLeftBracket():
                    if prechar:
                        midfix.insert(0, oper)
                        midfix.insert(0, Operator('.'))
                        continue
                    opstack.append(oper)
                    prechar = False

                elif oper.isRightBracket():
                    while True:
                        c = opstack.pop()
                        if c.isLeftBracket():
                            break
                        else:
                            self.tokenList.append(c)
                    prechar = True
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
        elif isinstance(param, FA):
            self.graph = list(param.graph)
        self.operandList = []

    def getOperandList(self):
        if len(self.operandList) == 0:
            for l in self.graph:
                for x, y in l:
                    if not x.isEEdge() and x not in self.operandList:
                        self.operandList.append(x)

        return self.operandList

    def getEndState(self):
        return len(self.graph) - 1

    def resetOperandList(self):
        self.operandList = []
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

    def mergeEONE(self):
        graph = self.expand()
        len1 = len(self.graph)
        graph[0].append((Operand.getEEdge(), 1))
        graph[len1].append((Operand.getEEdge(), len1 + 1))
        graph[0].append((Operand.getEEdge(), len1 + 1))
        return FA(graph)


    def mergePlus(self):
        return self.mergeCircle().mergeAnd(self)

    def mergePeriod(self, start, end):
        if end is None:
            nfa = self.mergeCircle()
            for i in range(0, start):
                nfa = nfa.mergeAnd(self)
            return nfa
        else:
            eone = end - start
            nfa = self.mergeEONE()
            for i in range(1, eone):
                nfa = nfa.mergeAnd(self.mergeEONE())
            for i in range(0, start):
                nfa = nfa.mergeAnd(self)
            return nfa


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
                elif token.isEONE():
                    nfaStack.append(nfaStack.pop().mergeEONE())
                elif token.isPlus():
                    nfaStack.append(nfaStack.pop().mergePlus())
                elif token.isOr():
                    nfa2 = nfaStack.pop()
                    nfa1 = nfaStack.pop()
                    nfaStack.append(nfa1.mergeOr(nfa2))
                elif token.isAnd():
                    nfa2 = nfaStack.pop()
                    nfa1 = nfaStack.pop()
                    nfaStack.append(nfa1.mergeAnd(nfa2))
                elif token.isPeriod():
                    start, end = token.getPeriod()
                    nfaStack.append(nfaStack.pop().mergePeriod(start, end))

        return nfaStack


class DFA:
    def __init__(self, nfa):
        self.nfa = nfa.compile()[0]
        self.compile()

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
        result = []

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

    def compile(self):
        dfaStateID = []
        dfaState = []
        opList = self.nfa.getOperandList()
        endState = self.nfa.getEndState()
        endStates = []
        q = Queue()
        start = self.closure(0)
        q.put(start)
#        self.nfa.echo()
        if endState in start:#开始状态即为结束状态
            endStates.append(0)

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

        for s in cutStates:#清除空的组
            if len(s) == 0:
                cutStates.remove(s)

        self.endStates = list(endStates)
        self.maxDFA = list(startStates)
        self.maxDFA.extend(endStates)

        self.miniGroup = self.minimize(cutStates, dfaStateID)
        self.transGraph = dfaStateID

        sortedStates = []#分好的组
        for s in self.miniGroup:
            if 0 in s:#0为开始组
                sortedStates.insert(0, s)
            elif  len([val for val in s if val in self.endStates]) > 0:
                sortedStates.append(s)
            else:
                if len(s) > 0:
                    sortedStates.insert(1, s)
                else:
                    sortedStates.append(s)
        self.miniGroup = list(sortedStates)

        self.generateDFA()
        return dfaStateID, dfaState

    def innerFind(self, l, element):
        for x in range(0, len(l)):
            if element in l[x]:
                return x
        return None

    def generateDFA(self):
        miniGroup = self.miniGroup
        transMatrix = self.transGraph
        self.dfa = range(0, len(miniGroup))
        self.start = self.innerFind(miniGroup, 0)
        self.end = list(set([self.innerFind(miniGroup, x) for x in self.endStates]))

        trans = [[] for x in self.dfa]
        for x in range(0, len(self.maxDFA)):
            transRow = transMatrix[x]
            newRow = []
            for t in transRow:
                newRow.append(self.innerFind(miniGroup, t))
            trans[self.innerFind(miniGroup, x)] = newRow
        self.trans = trans


    def minimize(self, cutStates, trans):
        change = True#多次划分防止遗漏，向后看
        while change:
            change = False
            oldState = list(cutStates)
            for i in range(0, len(self.nfa.getOperandList())):
                for l in cutStates:
                    x = 0
                    if len(l) <= 1:
                        continue
                    newStates = {}
                    while x < len(l):
                        next = trans[l[x]][i]
                        if l[0] == 1:
                            pass
                        if next is None:
                            if not newStates.has_key(-1):
                                newStates[-1] = []
                            newStates[-1].append(l[x])#for none state

                        elif next not in l:
                            for tmp in cutStates:
                                if next in tmp:
                                    idx = tmp
                                    break

                            idx = ','.join([str(ix) for ix in idx])#生成唯一标识key
                            if newStates.has_key(idx) == False:
                                newStates[idx] = []
                            newStates[idx].append(l[x])
                        x += 1
                    if len(newStates) == 0:
                        continue

                    if len(newStates) ==1:
                        if len(l) == len(newStates[newStates.keys()[0]]):
                            continue
                    cutStates.remove(l)
                    for key in newStates.keys():
                        if newStates[key] not in cutStates:
                            cutStates.append(newStates[key])
                        for st in newStates[key]:
                            l.remove(st)
                    if len(l) > 0:
                        cutStates.insert(0, l)

            if len(oldState) != len(cutStates):
                change = True
        return cutStates

    def getOperatorList(self):
        return self.nfa.getOperandList()


    def getNext(self, state, edge):
        trans = self.trans[state]
        idx = 0
        try:
            if isinstance(edge, Operand):
                idx = self.getOperatorList().index(edge)
            elif isinstance(edge, str):
                idx = self.getOperatorList().index(Operand(edge))
            else:
                idx = int(edge)
        except:
            return None
        if len(trans) <= idx:
            return None
        return trans[idx]

    def isEnd(self, s):
        return s in self.end


class DFAInstance:
    def __init__(self, fa, input_str):
        self.fa = fa
        self.state = fa.start
        self.input = input_str

    def validate(self):
        state = self.state
        for s in self.input:
            state = self.fa.getNext(state, s)
            if state is None:
                return False
        if self.fa.isEnd(state):
            return True
        else:
            return False


def main():
    st = 'aa*((bab*a)*(a|b)b*)*'
    r = RE(st)
    print [ x.rule for x in r.getTokenList()]
    dfa = DFA(NFA(RE(st)))
    ins = DFAInstance(dfa, "ababbaababbbb")
    print ins.validate()
    print '========'
    print dfa.dfa
    print dfa.trans
    print dfa.start
    print dfa.end


if __name__ == '__main__':
    main()
