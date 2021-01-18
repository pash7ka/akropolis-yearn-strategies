FLAT_DIR="./flattened"
ECHIDNA_DIR="$FLAT_DIR/echidna"

if  [ ! -d $FLAT_DIR ]; then mkdir $FLAT_DIR; fi
if  [ ! -d $ECHIDNA_DIR ]; then mkdir $ECHIDNA_DIR; fi

brownie run flatten_contracts.py