#!/bin/bash

set -o errexit

export LC_ALL=ko_KR.UTF-8
export LANG=ko_KR.UTF-8

# directory
## current dir of this script
CDIR=$(readlink -f $(dirname $(readlink -f ${BASH_SOURCE[0]})))
PDIR=$(readlink -f $(dirname $(readlink -f ${BASH_SOURCE[0]}))/..)

IRSTLM=/usr/local/irstlm/bin
DOC=../doc.txt
DICT=${CDIR}/dict
NGRAM=${CDIR}/ngram
LM=${CDIR}/lm
iARPA=${CDIR}/iarpa_lm.gz
qARPA=${CDIR}/qarpa_lm
ARPA=${CDIR}/arpa_lm
SPLIT=8
NGRAM_SIZE=2
KENLM=../package/kenlm/bin

# command setting
python='/usr/local/bin/python2.7'
pig='pig'
hls='hadoop fs -ls'
hget='hadoop fs -get'
hmkdir='hadoop fs -mkdir'
hrm='hadoop fs -rm -skipTrash'
hrmr='hadoop fs -rm -r -skipTrash'
hmv='hadoop fs -mv'
hcp='hadoop fs -cp'
hcat='hadoop fs -cat'
hput='hadoop fs -copyFromLocal'
htest='hadoop fs -test -e'
htestd='hadoop fs -test -d'
hmerge='hadoop fs -getmerge'
hdu='hadoop fs -du'

# functions

function make_calmness()
{
    exec 3>&2 # save 2 to 3
    exec 2> /dev/null
}

function revert_calmness()
{
    exec 2>&3 # restore 2 from previous saved 3(originally 2)
}

function close_fd()
{
    exec 3>&-
}

function jumpto
{
    label=$1
    cmd=$(sed -n "/$label:/{:a;n;p;ba};" $0 | grep -v ':$')
    eval "$cmd"
    exit
}
