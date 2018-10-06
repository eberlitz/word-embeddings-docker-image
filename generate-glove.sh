
VOCAB_FILE=./data/glove/vocab.txt
COOCCURRENCE_SHUF_FILE=./data/glove/cooccurrence.shuf.bin
BUILDDIR=docker run -it -v /home/berlitz/data:/usr/src/app/data eberlitz/ptwiki2vec ./GloVe/build
VERBOSE=2
MAX_ITER=15
BINARY=0
NUM_THREADS=32
X_MAX=10

# VECTOR_SIZE=50
# SAVE_FILE=./data/models/GloVe/vectors-$VECTOR_SIZE
# $BUILDDIR/glove -save-file $SAVE_FILE -threads $NUM_THREADS -input-file $COOCCURRENCE_SHUF_FILE -x-max $X_MAX -iter $MAX_ITER -vector-size $VECTOR_SIZE -binary $BINARY -vocab-file $VOCAB_FILE -verbose $VERBOSE

VECTOR_SIZE=100
SAVE_FILE=./data/models/GloVe/vectors-$VECTOR_SIZE
$BUILDDIR/glove -save-file $SAVE_FILE -threads $NUM_THREADS -input-file $COOCCURRENCE_SHUF_FILE -x-max $X_MAX -iter $MAX_ITER -vector-size $VECTOR_SIZE -binary $BINARY -vocab-file $VOCAB_FILE -verbose $VERBOSE

VECTOR_SIZE=300
SAVE_FILE=./data/models/GloVe/vectors-$VECTOR_SIZE
$BUILDDIR/glove -save-file $SAVE_FILE -threads $NUM_THREADS -input-file $COOCCURRENCE_SHUF_FILE -x-max $X_MAX -iter $MAX_ITER -vector-size $VECTOR_SIZE -binary $BINARY -vocab-file $VOCAB_FILE -verbose $VERBOSE

VECTOR_SIZE=600
SAVE_FILE=./data/models/GloVe/vectors-$VECTOR_SIZE
$BUILDDIR/glove -save-file $SAVE_FILE -threads $NUM_THREADS -input-file $COOCCURRENCE_SHUF_FILE -x-max $X_MAX -iter $MAX_ITER -vector-size $VECTOR_SIZE -binary $BINARY -vocab-file $VOCAB_FILE -verbose $VERBOSE

VECTOR_SIZE=1000
SAVE_FILE=./data/models/GloVe/vectors-$VECTOR_SIZE
$BUILDDIR/glove -save-file $SAVE_FILE -threads $NUM_THREADS -input-file $COOCCURRENCE_SHUF_FILE -x-max $X_MAX -iter $MAX_ITER -vector-size $VECTOR_SIZE -binary $BINARY -vocab-file $VOCAB_FILE -verbose $VERBOSE