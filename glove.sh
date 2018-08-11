#!/bin/bash

CORPUS=$1
FILE_OUT_DIR=$2
VOCAB_FILE=$FILE_OUT_DIR/vocab.txt
COOCCURRENCE_FILE=$FILE_OUT_DIR/cooccurrence.bin
COOCCURRENCE_SHUF_FILE=$FILE_OUT_DIR/cooccurrence.shuf.bin
BUILDDIR="./GloVe/build"
VERBOSE=2
MEMORY=14.0
VOCAB_MIN_COUNT=2
WINDOW_SIZE=15

echo
echo "$ $BUILDDIR/vocab_count -min-count $VOCAB_MIN_COUNT -verbose $VERBOSE < $CORPUS > $VOCAB_FILE"
$BUILDDIR/vocab_count -min-count $VOCAB_MIN_COUNT -verbose $VERBOSE < $CORPUS > $VOCAB_FILE
echo "$ $BUILDDIR/cooccur -memory $MEMORY -vocab-file $VOCAB_FILE -verbose $VERBOSE -window-size $WINDOW_SIZE < $CORPUS > $COOCCURRENCE_FILE"
$BUILDDIR/cooccur -memory $MEMORY -vocab-file $VOCAB_FILE -verbose $VERBOSE -window-size $WINDOW_SIZE < $CORPUS > $COOCCURRENCE_FILE
echo "$ $BUILDDIR/shuffle -memory $MEMORY -verbose $VERBOSE < $COOCCURRENCE_FILE > $COOCCURRENCE_SHUF_FILE"
$BUILDDIR/shuffle -memory $MEMORY -verbose $VERBOSE < $COOCCURRENCE_FILE > $COOCCURRENCE_SHUF_FILE