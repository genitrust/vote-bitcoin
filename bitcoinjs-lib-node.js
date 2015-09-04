var bitcoinjs = {
  base58: require('bs58'),
  bitcoin: require('bitcoinjs-lib'),
  ecurve: require('ecurve'),
  BigInteger: require('bigi'),
  Buffer: require('buffer')
}

module.exports = foobar

// compile with: browserify bitcoinjs-lib-node.js -s bitcoinjs > bitcoinjs-lib.min.js
