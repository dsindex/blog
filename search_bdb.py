#!/usr/bin/env python
#-*- coding: utf8 -*-

import os
import sys
import re
from   optparse import OptionParser
import time
from   bsddb3 import db

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("--verbose", action="store_const", const=1, dest="verbose", help="verbose mode")
    parser.add_option("-d", "--dir", dest="dir",help="home directory", metavar="DIR")
    parser.add_option("-b", "--bdb", dest="bdbfile",help="bdb file name", metavar="BDB")
    (options, args) = parser.parse_args()

    if options.verbose == 1 : VERBOSE = 1

    dir_path = options.dir
    if dir_path == None :
        parser.print_help()
        sys.exit(1)

    bdb_file = options.bdbfile
    if bdb_file == None :
        parser.print_help()
        sys.exit(1)

    dbenv = db.DBEnv()
    if dbenv.open(dir_path, db.DB_CREATE | db.DB_INIT_MPOOL) :
        sys.stderr.write("DBEnv.open() fail\n")
        sys.exit(1)
    d = db.DB(dbenv)
    if d.open(bdb_file, db.DB_BTREE, db.DB_RDONLY) :
        sys.stderr.write("DB.open() fail\n")
        sys.exit(1)

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

        v = d.get(key)
        if v :
            print v

    durationTime = time.time() - startTime
    sys.stderr.write("duration time = %f\n" % durationTime)

    d.close()
    dbenv.close()
