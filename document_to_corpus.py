#!/usr/bin/env python
#-*- coding: utf8 -*-

'''
read http://radimrehurek.com/gensim/tut1.html
here is test code
'''

import os
import sys
import re
from   optparse import OptionParser
from   gensim import corpora, models, similarities, matutils
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import numpy
import scipy

def simple_doc2bow() :
    documents = ["Human machine interface for lab abc computer applications",\
            "A survey of user opinion of computer system response time",\
            "The EPS user interface management system",\
            "System and human system engineering testing of EPS",
            "Relation of user perceived response time to error measurement",
            "The generation of random binary unordered trees",
            "The intersection graph of paths in trees",
            "Graph minors IV Widths of trees and well quasi ordering",
            "Graph minors A survey"]

    # remove common words and tokenize
    stoplist = set('for a of the and to in'.split())
    texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]

    # remove words that appear only once
    all_tokens = sum(texts,[])
    tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    texts = [[word for word in text if word not in tokens_once] for text in texts]
    print texts

    dictionary = corpora.Dictionary(texts)
    dictionary.save('deerwester.dict') # store to disk, for later use
    print dictionary.token2id

    new_doc = "Human computer interaction"
    new_vec = dictionary.doc2bow(new_doc.lower().split())
    print new_vec # the word "interaction" does not appear in the dictionary and is ignored

    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('deerwester.mm', corpus) # store to disk, for later use
    print corpus
    
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

def corpus_to_dense(corpus, dictionary) :
    num_terms = len(dictionary.token2id)
    numpy_matrix = matutils.corpus2dense(corpus, num_terms)
    return numpy_matrix

def dense_to_corpus(numpy_matrix) :
    corpus = matutils.Dense2Corpus(numpy_matrix)
    return corpus

def corpus_to_sparse(corpus) :
    scipy_csc_matrix = matutils.corpus2csc(corpus)
    return scipy_csc_matrix
    
def sparse_to_corpus(scipy_csc_matrix) :
    corpus = matutils.Sparse2Corpus(scipy_csc_matrix)
    return corpus

'''
python2.7 documents_to_corpus.py -d mydocuments.txt < mydocuments.txt
'''
if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("--verbose", action="store_const", const=1, dest="verbose", help="verbose mode")
    parser.add_option("-d", "--documents", dest="documents",help="documents", metavar="DOCS")
    (options, args) = parser.parse_args()

    if options.verbose == 1 : VERBOSE = 1

    documents_path = options.documents
    if documents_path == None :
        parser.print_help()
        sys.exit(1)

    dictionary = construct_dictionary(documents_path)
    dictionary_path = documents_path + '.dict'
    save_dictionary(dictionary, dictionary_path)
    dictionary = load_dictionary(dictionary_path)

    print dictionary.token2id

    corpus = []
    corpus_path = documents_path + '.mm'
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
            
        print line
        vector = dictionary.doc2bow(line.lower().split())
        print vector
        '''
        for id,tf in vector :
            print dictionary.get(id) + "\t" + str(tf)
        '''
        corpus.append(vector)

    save_corpus(corpus, corpus_path)
    corpus = load_corpus(corpus_path)
    for vector in corpus :
        print vector

    # corpus <-> numpy matrix
    numpy_matrix = corpus_to_dense(corpus, dictionary)
    print numpy_matrix
    corpus = dense_to_corpus(numpy_matrix)
    for vector in corpus :
        print vector

    # corpus <-> scipy sparse matrix
    scipy_csc_matrix = corpus_to_sparse(corpus)
    print scipy_csc_matrix
    corpus = sparse_to_corpus(scipy_csc_matrix)
    for vector in corpus :
        print vector
