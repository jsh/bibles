#!/bin/bash -eu
# make the bases and snippets

source location.sh  # where is everything?

mkdir -p ot nt

for lang in $lang_list; do
	make-corpus.sh ot $lang | canonicalize.py 2000000 > ot/$lang
	make-corpus.sh nt $lang | canonicalize.py  200000 > nt/$lang
done
