#!/usr/bin/env bash
#DESCRIPTION: Download word embeddings
#CREATES: data/tmp/w2v_320d

mkdir -p data/tmp
wget http://i.amcat.nl/w2v_320d -O data/tmp/w2v_320d
