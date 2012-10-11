#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import re

regexps = [r'[\n]',
           r'[0-9]+',
           r'[0-9]*\.[0-9]+',
           r'[a-zA-Z][a-zA-Z0-9]*',
           r'[\+\-\*\/\%]',
           r'.', ]
strs = ['newline', 'int', 'float', 'alpha', 'operator', 'unknown']
regexps_c = [re.compile('^' + c) for c in regexps]

def find_match(raw, reg_c=regexps_c):
    result = []
    global regexps
    for reg in reg_c:
        if reg.match(raw):
            result.append(reg)
    return result


def search(raw, reg_c=regexps_c):
    rreg = None
    rdata = None
    for reg in reg_c:
        match = reg.search(raw)
        if match != None:
            t1, t2  = reg, match.span()[1]
            if rdata == None or t2 > rdata:
                rreg, rdata = reg, t2
    return (rreg,rdata)


input = 'hello %2%31.211'
tmp = input
tokens = []
symbol = []
while True:
    if len(tmp) == 0:
        break
    reg, data = search(tmp)
    if reg == None:
        exit(0)
    else:
        tokens.append(tmp[:data])
        symbol.append(strs[regexps_c.index(reg)])
        tmp = tmp[data:]

print tokens
print symbol




#tokens = []
#token = ''
#search_list = regexps_c
#while len(input_list) > 0:
#    a = input_list.pop(0)
#    if len(token) == 0:
#        tokens.append(token)
#        search_list = regexps_c
#    token += a
#    search_list = find_match(token, search_list)
#    print a
#    if len(search_list) == 0:
#        if len(token) == 1:
#            raise SyntaxError
#        token = ''
#        input_list.insert(0, a)
#        print tokens[-1]
#    else:
#        tokens[-1] = token
