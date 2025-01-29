# Merkle Tree Package

## Overview
This Python package provides an implementation of a Merkle tree, allowing for efficient verification of data integrity using cryptographic hashes. The package includes functionality to construct a Merkle tree, generate proof of inclusion, and save/load the tree from a file.

## Features
- Construct a Merkle tree from a list of Ethereum addresses.
- Generate a proof of inclusion for any address.
- Compute the Merkle root hash.
- Save and load Merkle trees from a JSON file.

## Installation
Ensure you have Python 3 installed, then install dependencies:
```sh
pip install merkeletree_ethadd
```

## Usage
```python
from merkletree_ethadd import MerkleTree

# Define Ethereum addresses
addresses = [
    "0x5B38Da6a701c568545dCfcB03FcB875f56beddC4",
    "0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2",
    "0x4B20993Bc481177ec7E8f571ceCaE8A9e22C02db",
    "0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB"
]

# Create a Merkle tree
tree = MerkleTree()
tree.make_from_values(addresses)

# Get the Merkle root
print("Merkle Root:", tree.getRoot())

# Get proof for an address
proof = tree.getProof(addresses[0])
print("Proof for first address:", proof)

# Save and load the tree
tree.dumpToFile("merkle_tree.json")
loaded_tree = MerkleTree.loadFromFile("merkle_tree.json")
```
