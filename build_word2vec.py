#!/usr/bin/env python
#-*- coding: utf8 -*-

'''
read http://radimrehurek.com/gensim/models/word2vec.html
here is test code
'''

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
from   optparse import OptionParser
import time
from   gensim.models import word2vec,phrases
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def build_model(corpus_path, detect_phrase=False) :
    startTime = time.time()

    sentences = word2vec.LineSentence(corpus_path)
    if detect_phrase :
        bigram_transformer = phrases.Phrases(sentences)
        model = word2vec.Word2Vec(bigram_transformer[sentences], size=100, alpha=0.025, window=5, min_count=5, sample=1e-5, workers=4, sg=1)
    else :
        model = word2vec.Word2Vec(sentences, size=100, alpha=0.025, window=5, min_count=5, sample=1e-5, workers=4, sg=1)
    # no more training
    model.init_sims(replace=True)
    durationTime = time.time() - startTime
    sys.stderr.write("duration time = %f\n" % durationTime)
    return model

def save_model(model, model_path) :
    model.save(model_path)
    
'''
python2.7 build_word2vec.py -c corpus.txt -m corpus.txt.model
'''
if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("--verbose", action="store_const", const=1, dest="verbose", help="verbose mode")
    parser.add_option("-c", "--corpus", dest="corpus",help="corpus path", metavar="CORPUS")
    parser.add_option("-m", "--model", dest="model",help="model path, output file", metavar="MODEL")
    (options, args) = parser.parse_args()

    if options.verbose == 1 : VERBOSE = 1

    corpus_path = options.corpus
    if corpus_path == None :
        parser.print_help()
        sys.exit(1)

    model_path = options.model
    if model_path == None :
        parser.print_help()
        sys.exit(1)

    model = build_model(corpus_path)
    save_model(model, model_path)
