#!/usr/bin/env python
# -*- coding:UTF-8 -*-
import re
def search(raw, reg_c):
    rreg,rdata = None,None
    for reg,reg_c in reg_c:
        match = reg_c.search(raw)
        if match != None:
            t1, t2  = reg, match.span()[1]
            if rdata == None or t2 > rdata:
                rreg, rdata = reg, t2
    return (rreg,rdata)

regexps = [r'[0-9]+', r'[\n]', r'[\+\-\*\/\%]', r'.', r'[0-9]*\.[0-9]+', r'[a-zA-Z][a-zA-Z0-9]*', ]
regexps_c = [(r, re.compile('^' + r)) for r in regexps]
input = ''

#start content1
input = 'hello%2%31.211'

#end content1

#main loop
while True:
    if len(input) == 0:break
    reg, data = search(input, regexps_c)
    if reg == None:
        raise SyntaxError
    else:
        yytext = input[:data]
        input = input[data:]
        if 1 == 0:
            pass

        elif reg == r'[0-9]+':
            print 'integer',

        elif reg == r'[\n]':
            print 'newline',

        elif reg == r'[\+\-\*\/\%]':
            print 'operator',

        elif reg == r'.':
            print yytext,

        elif reg == r'[0-9]*\.[0-9]+':
            print 'float',

        elif reg == r'[a-zA-Z][a-zA-Z0-9]*':
            print 'alpha',


#end main loop

#start content2
print "Hello"

#end content2