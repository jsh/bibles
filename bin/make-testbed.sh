#!/bin/bash -eu
# make the bases and snippets

source location.sh  # where is everything?

mkdir -p ot.d nt.d

for lang in $lang_list; do
	make-corpus.sh ot.d $lang | canonicalize.py 2000000 > ot.d/$lang
	make-corpus.sh nt.d $lang | canonicalize.py  200000 > nt.d/$lang
done
