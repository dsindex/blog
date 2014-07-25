#!/usr/bin/env python
#-*- coding: utf8 -*-

import os
import sys
import re
from   optparse import OptionParser

VERBOSE = 0

def swap(eoj_list, x, y) :
    temp = eoj_list[x]
    eoj_list[x] = eoj_list[y]
    eoj_list[y] = temp

'''
algorithm form http://www.geeksforgeeks.org/write-a-c-program-to-print-all-permutations-of-a-given-string/
'''
def permute(eoj_list, i, n, ret) :
    if i == n :
        ret.append(' '.join(eoj_list))
    else :
        for j in xrange(i,n+1) :
            swap(eoj_list, i, j)
            permute(eoj_list, i+1, n, ret)
            swap(eoj_list, i, j) # backtrack

'''
i should not be composed with zero : 103 (x)
i's decimal points should be equal to dp : 123, 321, ...
i's element should not be greater than dp : 114 (x)
each digit should be distinct : 12345 (o), 22344(x)
'''
def sum_digit(i, dp) :
    str_i = str(i)
    if len(str_i) != dp : return 0
    sum = 0
    distinct = {}
    for ch in str_i :
        if ch == '0' : return 0
        int_ch = int(ch)
        if int_ch > dp : return 0
        distinct[ch] = int_ch
        sum += int_ch
    if len(distinct) != dp : return 0
    return sum    

'''
dp  = 3
digit_sum = 1+2+3 = 6
'''
def get_digit_sum(dp) :
    digit_sum = 0
    for i in xrange(dp+1) : # 0 1 2 3
        digit_sum += i
    return digit_sum

'''
dp  = 3
max = 321+1
'''
def get_max(dp) :
    s = []
    for i in reversed(xrange(dp+1)) : # 3 2 1 0
        if i : s.append(str(i))
    return int(''.join(s)) + 1

def get_string(eoj_list, str_i) :
    ret = []
    for ch in str_i :
        i = int(ch) - 1
        ret.append(eoj_list[i])
    return ' '.join(ret)

'''
algorithm from http://marknelson.us/2002/03/01/next-permutation/
start : starting number for searching
max : maximum number
digit_sum : sumation of each digit
dp  : decimal points
example) for 'abc'
start = 0
max = 321+1
digit_sum = 1+2+3 = 6 = sum(dp)
dp  = 3
'''
def permuation(start, max, digit_sum, dp) :
    ret = []
    for i in xrange(start, max) :
        sum = sum_digit(i, dp)
        if sum == digit_sum :
            ret.append(str(i))
    return ret

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("--verbose", action="store_const", const=1, dest="verbose", help="verbose mode")
    (options, args) = parser.parse_args()

    if options.verbose == 1 : VERBOSE = 1

    while 1:
        try:
            line = sys.stdin.readline()
        except KeyboardInterrupt:
            break
        if not line:
            break
        line = line.strip()
        eoj_list = line.split()
        dp = len(eoj_list)
        if dp == 1 : continue

        # 어절단위로 순서를 바꿔서 출력(recursive)
        ret = []
        permute(eoj_list, 0, dp-1, ret)
        for ext in ret :
            print ext

        # 어절단위로 순서를 바꿔서 출력(non-recursive)
        eoj_list = line.split()
        dp = len(eoj_list)
        digit_sum = get_digit_sum(dp)
        max = get_max(dp)
        ret = permuation(0, max, digit_sum, dp)
        for str_i in ret :
            print get_string(eoj_list, str_i)
