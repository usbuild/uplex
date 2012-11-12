#!/usr/bin/env python
# -*- coding:UTF-8 -*-

from Lex import lex

f = open('sample.l', 'r')
ST_DEFAULT = 0
ST_RAW = 1
ST_MAIN = 2
ST_DEFINE = 3
state = ST_DEFAULT
with open('skeleton.skl', 'r') as skl:
    skl_str = skl.read()
output = ''
regexps = {}
main_status = (ST_MAIN, ST_RAW)
cur_regexp = ''
before_main = True
default_content1 = ''
default_content2 = ''
switch = ''
regexps_keys = []

def handle_default(line):
    global default_content1
    global default_content2
    if before_main:
        default_content1 += line + "\n"
    else:
        default_content2 += line + "\n"
    pass


def handle_raw(line):
    global cur_regexp
    global regexps
    regexps[cur_regexp] += " " * 12 + line + "\n"
    pass


def handle_main(line):
    pass


def handle_define(line):
    pass

handle_map = {
    ST_DEFAULT: lambda x: handle_default(x),
    ST_DEFINE: lambda x: handle_define(x),
    ST_RAW: lambda x: handle_raw(x),
    ST_MAIN: lambda x: handle_main(x),
}

for line in f:
    if len(line.strip()) == 0:
        continue

    line = line.rstrip()
    if line == '%#' and state != ST_DEFINE:
        state = ST_DEFINE
        continue

    elif line == '%#' and state == ST_DEFINE:
        state = ST_DEFAULT
        continue

    elif line == '%%' and state not in main_status:
        state = ST_MAIN
        continue

    elif line == '%%' and state in main_status:
        state = ST_DEFAULT
        before_main = False
        continue

    elif len(line) > 2 and line[0:2] == '->' and state in main_status:
        cur_regexp = line[2:]
        regexps[cur_regexp] = ''
        regexps_keys.append(cur_regexp)
        state = ST_RAW
        continue
    handle_map[state](line)
i = 0
for line in regexps_keys:
    switch += " " * 8 + "elif reg_pos == " + str(i) + ":\n" + regexps[line] + "\n"
    i += 1

result = skl_str.replace('%{content1}', default_content1)\
.replace('%{content2}', default_content2)\
.replace('%{switch}', switch)\
.replace('%{lex_packs}', "%r" % lex.DFA.pack(regexps_keys))

with open('yy.lex.py', 'w') as fw:
    fw.write(result)

f.close()
