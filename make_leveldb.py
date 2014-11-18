#!/usr/bin/env python
#-*- coding: utf8 -*-

import os
import sys
import re
from   optparse import OptionParser
import time
import leveldb

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("--verbose", action="store_const", const=1, dest="verbose", help="verbose mode")
    parser.add_option("-d", "--db", dest="dbdir",help="db dir path", metavar="DB")
    (options, args) = parser.parse_args()

    if options.verbose == 1 : VERBOSE = 1

    db_dir = options.dbfile
    if db_dir == None :
        parser.print_help()
        sys.exit(1)

    startTime = time.time()

    db = leveldb.LevelDB(db_dir)

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

        db.Put(key,value)

    durationTime = time.time() - startTime
    sys.stderr.write("duration time = %f\n" % durationTime)
