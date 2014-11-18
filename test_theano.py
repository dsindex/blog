#!/usr/bin/env python2.7
#-*- coding: utf8 -*-

import os
import sys
import re
from   optparse import OptionParser

import cPickle, gzip
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

def shared_dataset(data_xy):
    data_x, data_y = data_xy
    shared_x = theano.shared(numpy.asarray(data_x, dtype=theano.config.floatX))
    shared_y = theano.shared(numpy.asarray(data_y, dtype=theano.config.floatX))
    return shared_x, T.cast(shared_y, 'int32')
    
if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("--verbose", action="store_const", const=1, dest="verbose", help="verbose mode")
    (options, args) = parser.parse_args()

    if options.verbose == 1 : VERBOSE = 1

    f = gzip.open('mnist.pkl.gz', 'rb')
    train_set, valid_set, test_set = cPickle.load(f)
    f.close()

    test_set_x, test_set_y = shared_dataset(test_set)
    valid_set_x, valid_set_y = shared_dataset(valid_set)
    train_set_x, train_set_y = shared_dataset(train_set)
    batch_size = 500 # size of the minibatch

    # accessing the third minibatch of the training set
    data = train_set_x[2 * 500: 3 * 500]
    label = train_set_y[2 * 500: 3 * 500]
