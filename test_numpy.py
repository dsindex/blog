#!/usr/bin/env python2.7
#-*- coding: utf8 -*-

import os
import sys
import re
from   optparse import OptionParser

import theano
import theano.tensor as T
import numpy as np
import scipy


# --verbose
VERBOSE = 0

def open_file(filename, mode) :
    try : fid = open(filename, mode)
    except :
        sys.stderr.write("open_file(), file open error : %s\n" % (filename))
        exit(1)
    else :
        return fid

def close_file(fid) :
    fid.close()
    
def type_test() :
    m = np.asarray([[1., 2], [3, 4], [5, 6]])
    print m
    print m.shape # shape is tuple (3,2)
    print m[2,0]

    x = np.float32(1.0)
    print x
    y = np.int_([1,2,4])
    print y
    z = np.array([1,2,3], dtype=np.int8)
    print z
    print z.dtype
    z = np.float16(z)
    print z
    print z.dtype
    z = z.astype(np.int_) # or z.astype(int)
    print z
    print z.dtype
    print np.issubdtype(z.dtype,float)

def array_test() :
    x = np.array([2, 3, 1, 0])
    print x
    x = np.array([[1,2.0],[0,0],(1+1j,3.)])
    print x
    x = np.array([[ 1.+0.j, 2.+0.j], [ 0.+0.j, 0.+0.j], [ 1.+1.j, 3.+0.j]])
    print x
    x = np.zeros((2, 3))
    print x
    x = np.ones((2, 3))
    print x
    print np.arange(10)
    print np.arange(2, 10, dtype=np.float)
    print np.arange(2, 3, 0.1)
    print np.linspace(1., 4., 6)
    print np.indices((3,3))
    
if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("--verbose", action="store_const", const=1, dest="verbose", help="verbose mode")
    (options, args) = parser.parse_args()

    if options.verbose == 1 : VERBOSE = 1

    type_test()
    array_test()
