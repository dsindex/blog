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

def load_model(model_path) :
    model = word2vec.Word2Vec.load(model_path)
    return model

'''
python2.7 search_word2vec.py -m corpus.txt.model
'''
if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("--verbose", action="store_const", const=1, dest="verbose", help="verbose mode")
    parser.add_option("-m", "--model", dest="model",help="model path, output file", metavar="MODEL")
    (options, args) = parser.parse_args()

    if options.verbose == 1 : VERBOSE = 1

    model_path = options.model
    if model_path == None :
        parser.print_help()
        sys.exit(1)

    model = load_model(model_path)
    
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

        # convert to unicode
        line_unicode = line.decode('utf-8')
        tokens = []
        for token in line_unicode.split() :
            if token in model : tokens.append(token)
        if len(tokens) >= 1 :
            ret = model.most_similar(positive=tokens)
            for word,sim in ret :
                print word + "\t" + str(sim)
        else :
            print "not in vocab"
        print "=================================="
