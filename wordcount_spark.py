#!/usr/bin/env python
#-*- coding: utf8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from   optparse import OptionParser

from   pyspark import SparkContext

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

def map_func(line) :
    words = line.split(' ')
    return map(lambda x: (x, 1), words)

def reduce_func(a,b) :
    return a+b

def map_func2(entry) :
    key,value = entry
    return (key,reduce(lambda a,b: a+b,value))
    
'''
usage : spark-submit --master yarn-client --total-executor-cores 100 --executor-memory 512M wordcount.py -f input_file_on_hdfs
'''
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--verbose", action="store_const", const=1, dest="verbose", help="verbose mode")
    parser.add_option("-f", "--file", dest="file",help="file path in HDFS", metavar="FILE")
    (options, args) = parser.parse_args()

    if options.verbose == 1 : VERBOSE = 1

    file_path = options.file
    if file_path == None :
        parser.print_help()
        sys.exit(1)

    sc = SparkContext(appName="PythonWordCount")

    '''
    # read from hdfs directory
    lines = sc.wholeTextFiles(file_path, 1)
    counts = lines.values().flatMap(lambda x: x.split(' ')) \
            .map(lambda x: (x, 1)) \
            .reduceByKey(lambda a, b: a + b) \
            .sortBy(lambda x: x[1],ascending=False)
    counts.saveAsHadoopFile("gensim/output","org.apache.hadoop.mapred.TextOutputFormat")
    '''

    lines = sc.textFile(file_path, 1)

    # save to hdfs
    counts = lines.flatMap(lambda x: x.split(' ')) \
            .map(lambda x: (x, 1)) \
            .reduceByKey(lambda a, b: a + b) \
            .sortBy(lambda x: x[1],ascending=False)
    counts.saveAsHadoopFile("gensim/output","org.apache.hadoop.mapred.TextOutputFormat")
    
    '''
    lines = sc.textFile(file_path, 1)
    # user defined map,reduce
    # map : string -> [(a,1),(b,1),..],[(a,1),(c,1),...],....
    # flatMap : list of list -> [(a,1),(b,1),....,(a,1),(c,1),....]
    # reduceByKey : goup by key -> [(a,(1,1,1,....)),(b,(1,1,1)),(c,1,1,1,1,...),...]
    #             : reduce value list -> [(a,10),(b,3),(c,17),....]
    # sortBy : [(a,10),(b,3),(c,17),....] -> [(c,17),(a,10),(c,3),....]
    counts = lines.map(map_func) \
            .flatMap(lambda x: x) \
            .reduceByKey(reduce_func) \
            .sortBy(lambda x: x[1],ascending=False)
    counts.saveAsHadoopFile("gensim/output","org.apache.hadoop.mapred.TextOutputFormat")
    '''

    '''
    lines = sc.textFile(file_path, 1)
    # user defined map,reduce
    counts = lines.map(map_func) \
            .flatMap(lambda x: x) \
            .groupByKey() \
            .map(map_func2) \
            .sortBy(lambda x: x[1],ascending=False)
    output = counts.collect()
    for key,value in output :
        print key + "\t" + str(value)
    '''

    '''
    lines = sc.textFile(file_path, 1)
    # save to local
    counts = lines.flatMap(lambda x: x.split(' ')) \
                  .map(lambda x: (x, 1)) \
                  .reduceByKey(lambda a, b: a + b)
    output = counts.collect()
    fd = open_file("output.txt",'w')
    for (word, count) in output:
        fd.write("%s\t%s\n" % (word,count))
    close_file(fd)
    '''
    
    '''
    lines = sc.textFile(file_path, 1)
    # test goupByKey
    group = lines.flatMap(lambda x: x.split(' ')).map(lambda x: (x, 1)).groupByKey()
    output = group.collect()
    for (word,count_list) in output :
        print word + "\t" + ','.join(map(lambda x: str(x),count_list))
    '''

    sc.stop()
