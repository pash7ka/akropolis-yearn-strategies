rm -rf build/*
npx truffle compile
slither . --config-file ./security/slither/slither-config.json  || true