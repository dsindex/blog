#!/usr/bin/env python
#-*- coding: utf8 -*-

'''
read http://radimrehurek.com/gensim/dist_lda.html
here is test code
'''

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
from   optparse import OptionParser
from   gensim import corpora, models, similarities, matutils
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def construct_dictionary(documents_path, filter=None) :
    # collect statistics about all tokens
    dictionary = corpora.Dictionary(line.lower().split() for line in open(documents_path))

    if filter :
        # remove stop words and words that appear only once
        stoplist = set('for a of the and to in'.split())
        stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
        once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
        dictionary.filter_tokens(stop_ids + once_ids) # remove stop words and words that appear only once
        dictionary.compactify() # remove gaps in id sequence after words that were removed

    return dictionary

def save_dictionary(dictionary, dictionary_path) :
    dictionary.save(dictionary_path)

def load_dictionary(dictionary_path) :
    dictionary = corpora.Dictionary().load(dictionary_path,mmap='r')
    return dictionary
    
def save_corpus(corpus, corpus_path, format=None) :
    if format == 'svmlight' : # Joachim’s SVMlight format
        corpora.SvmLightCorpus.serialize(corpus_path, corpus)
    if format == 'lda-c' : # Blei’s LDA-C format
        corpora.BleiCorpus.serialize(corpus_path, corpus)
    if format == 'low' : # GibbsLDA++ format
        corpora.LowCorpus.serialize(corpus_path, corpus)
    if not format : # Matrix Market format
        corpora.MmCorpus.serialize(corpus_path, corpus)

def load_corpus(corpus_path) :
    corpus = corpora.MmCorpus(corpus_path)
    return corpus

def corpus_to_tfidf(corpus) :
    tfidf = models.TfidfModel(corpus, normalize=True) # step 1 -- initialize a model
    '''
    corpus_tfidf = tfidf[corpus]
    for doc in corpus_tfidf:
        print doc
    '''
    return tfidf

def save_tfidf(tfidf, tfidf_path) :
    tfidf.save(tfidf_path)

def load_tfidf(tfidf_path) :
    tfidf = models.TfidfModel.load(tfidf_path)
    return tfidf

def corpus_to_lsi(corpus, tfidf, dictionary, topic_number) :
    corpus_tfidf = tfidf[corpus]
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=topic_number) # initialize an LSI transformation
    '''
    corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
    lsi.print_topics(3)
    for doc in corpus_lsi: # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
        print doc
    '''
    return lsi

def save_lsi(lsi, lsi_path) :
    lsi.save(lsi_path)

def load_lsi(lsi_path) :
    lsi = models.LsiModel.load(lsi_path)
    return lsi
    
def corpus_to_lda(corpus, dictionary, topic_number) :
    lda = models.LdaModel(corpus, id2word=dictionary, num_topics=topic_number)
    return lda

def save_lda(lda, lda_path) :
    lda.save(lda_path)

def load_lda(lda_path) :
    lda = models.LdaModel.load(lda_path)
    return lda

def corpus_to_lsi_dist(corpus, dictionary, topic_number) :
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=topic_number, chunksize=10000, distributed=True)
    return lsi

def corpus_to_lda_dist(corpus, dictionary, topic_number) :
    lda = models.LdaModel(corpus, id2word=dictionary, num_topics=topic_number, update_every=1, chunksize=10000, passes=1, distributed=True)
    return lda

'''
python2.7 dist_lda.py --dictionary=document.txt.dict --corpus=document.txt.mm --lda=document.txt.lda
'''
if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("--verbose", action="store_const", const=1, dest="verbose", help="verbose mode")
    parser.add_option("-d", "--dictionary", dest="dictionary",help="dictionary", metavar="DICT")
    parser.add_option("-c", "--corpus", dest="corpus",help="corpus", metavar="CORPUS")
    parser.add_option("-a", "--lda", dest="lda",help="lda, output file", metavar="LDA")
    (options, args) = parser.parse_args()

    if options.verbose == 1 : VERBOSE = 1

    dictionary_path = options.dictionary
    if dictionary_path == None :
        parser.print_help()
        sys.exit(1)

    corpus_path = options.corpus
    if corpus_path == None :
        parser.print_help()
        sys.exit(1)
        
    lda_path = options.lda
    if lda_path == None :
        parser.print_help()
        sys.exit(1)

    dictionary = load_dictionary(dictionary_path)
    corpus = load_corpus(corpus_path)

    lda = corpus_to_lda_dist(corpus, dictionary, 200)
    save_lda(lda, lda_path)
