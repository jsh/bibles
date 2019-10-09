#!/bin/bash -euo pipefail
# write a corpus to stdout

# Example:
# make a New-Testament latin corpus
#    make-corpus nt latin

corpus=$1
lang=$2

source location.sh  # where is everything?

cat $( ls $lang_data/$lang/*.txt | grep -f ${corpus/.d/}-list.txt )
