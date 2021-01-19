FLAT_DIR="./flattened"

if  [ ! -d $FLAT_DIR ]; then mkdir $FLAT_DIR; fi

brownie run flatten_contracts.py