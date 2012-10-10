#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import re

def search(raw, reg_c):
    rreg,  rdata = None, None

    for reg,reg_c in reg_c:
        match = reg_c.search(raw)
        if match != None:
            t1, t2 = reg_c, match.span()[1]
            if rdata == None or t2 > rdata:
                rreg,  rdata = reg,  t2
    return (rreg, rdata)

regexps = [r'[\n]',
           r'[0-9]+',
           r'[0-9]*\.[0-9]+',
           r'[a-zA-Z][a-zA-Z0-9]*',
           r'[\+\-\*\/\%]',
           r'.', ]

regexps_c = [(r, re.compile('^' + r)) for r in regexps]

input = 'hello %2%31.211'
#for a in regexps.keys():
#    print 'elif reg == \'',a,'\':'
#    print '\t',regexps[a]

while True:
    if len(input) == 0:break
    reg, data = search(input, regexps_c)
    if reg == None:
        raise SyntaxError
    else:
        input = input[data:]