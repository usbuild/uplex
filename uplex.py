#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import  re

f = open('sample.l', 'r')
ST_DEFAULT = 0
ST_MACRO = 1
ST_RAW = 2
ST_MAIN = 3
state = ST_MACRO

def handle_macro(line):
    print line


def handle_raw(line):
    print '''\
re = hello\
    '''
    pass


def handle_main(line):
    print line

main_status = (ST_MAIN, ST_RAW)
cur_regexp = ''

handle_map = {
    ST_DEFAULT: lambda x: None,
    ST_MACRO: lambda x: handle_macro(x),
    ST_RAW: lambda x: handle_raw(x),
    ST_MAIN: lambda x: handle_main(x),
}

for line in f:
    if len(line.strip()) == 0:
        continue

    line = line.rstrip()
    if line == '%%' and state not in main_status:
        state = ST_MAIN
        continue
    elif line == '%%' and state in main_status:
        state = ST_MACRO
        continue
    elif len(line) > 2 and line[0:2] == '->' and state in main_status:
        cur_regexp = line[2:]
        state = ST_RAW
        continue

    handle_map[state](line)

f.close()

