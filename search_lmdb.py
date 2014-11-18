#!/usr/bin/env python
#-*- coding: utf8 -*-

import os
import sys
import re
from   optparse import OptionParser
import time
import lmdb

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("--verbose", action="store_const", const=1, dest="verbose", help="verbose mode")
    parser.add_option("-d", "--db", dest="dbpath",help="db path", metavar="DB")
    (options, args) = parser.parse_args()

    if options.verbose == 1 : VERBOSE = 1

    db_path = options.dbpath
    if db_path == None :
        parser.print_help()
        sys.exit(1)


    # env == db coz max_dbs=0
    env = lmdb.Environment(db_path,map_size=24*(1023**3),subdir=False,readonly=True,create=False,max_dbs=0,lock=False)
    txn = lmdb.Transaction(env,db=None,write=False)

    startTime = time.time()
    
    linecount = 0
    while 1 :
        try : line = sys.stdin.readline()
        except KeyboardInterrupt : break
        if not line : break
        try : line = line.strip()
        except : continue
        if not line : continue
        linecount += 1
        if linecount % 1000 == 0 :
            sys.stderr.write("[linecount]" + "\t" + str(linecount) + "\n")

        key,value = line.split('\t',1)
        if not key or not value : continue

        ret = txn.get(key,default=None)
        if ret :
            print ret

    durationTime = time.time() - startTime
    sys.stderr.write("duration time = %f\n" % durationTime)

    txn.abort()
    env.close()
