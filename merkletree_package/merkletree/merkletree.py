from Crypto.Hash import keccak
from eth_abi import encode
from typing import NamedTuple
import math
from functools import cmp_to_key
import json

# Utility functions
def compare_bytes(a, b):
    n = min(len(a), len(b))
    i = 0
    while i < n:
        if a[i] != b[i]:
            return a[i] - b[i]
        i += 1
    return len(a) - len(b)

def hashPair(a, b):
    keccak_hash = keccak.new(digest_bits=256, update_after_digest=True)
    keccak_hash.update(b"".join(sorted([a, b], key=cmp_to_key(compare_bytes))))
    return keccak_hash.digest()

def leftChildIndex(i):
    return 2 * i + 1

def rightChildIndex(i):
    return 2 * i + 2

def siblingIndex(i):
    return i - (-1) ** (i % 2)

def parentIndex(i):
    return math.floor((i - 1) / 2)

def _to_hex(x):
    return "0x" + x.hex()

def _from_hex(x):
    return bytes.fromhex(x[2:])

# Data structures
class Leaf(NamedTuple):
    value: bytes
    hash: bytes

    def __lt__(self, other) -> bool:
        return compare_bytes(self.hash, other.hash) < 0

class MerkleTree:
    def __init__(self):
        self.reset_tree()
        
    def reset_tree(self):
        self.hashed_values = []
        self.tree = []
        self.values = {}
    
    def make_from_values(self, values):
        for v in values:
            leaf = Leaf(v, self.leafHash(v))
            self.hashed_values.append(leaf)
        self.hashed_values.sort()
        self.tree = [bytes()] * (2 * len(self.hashed_values) - 1)
        
        for i, v in enumerate(reversed(self.hashed_values)):
            self.tree[-(i + 1)] = v.hash
        
        for i in range(len(self.tree) - len(self.hashed_values) - 1, -1, -1):
            self.tree[i] = hashPair(self.tree[leftChildIndex(i)], self.tree[rightChildIndex(i)])
        
        self.values = {v.value: len(self.tree) - i - 1 for i, v in enumerate(self.hashed_values)}
    
    def getProof(self, value):
        index = self.values[value]
        proof = []
        while index > 0:
            proof.append(self.tree[siblingIndex(index)])
            index = parentIndex(index)
        return [_to_hex(x) for x in proof]

    def leafHash(self, leaf):
        keccak_hash = keccak.new(digest_bits=256, update_after_digest=True)   
        keccak_hash.update(encode(['address'], [leaf]))
        leaf = keccak_hash.digest()
        keccak_hash = keccak.new(digest_bits=256, update_after_digest=True)
        keccak_hash.update(leaf)
        return keccak_hash.digest()

    def getRoot(self):
        return _to_hex(self.tree[0])
    
    def dumpToFile(self, filename):
        formatted = {
            "tree": [_to_hex(hash) for hash in self.tree],
            "values": [{"value": v, "treeIndex": i} for v, i in self.values.items()]
        }
        with open(filename, "w") as outfile:
            json.dump(formatted, outfile, indent=2)

    @classmethod
    def loadFromFile(cls, filename):
        with open(filename, "r") as infile:
            data = json.load(infile)
        
        tree = cls()
        tree.tree = [_from_hex(hash) for hash in data["tree"]]
        tree.values = {entry["value"]: entry["treeIndex"] for entry in data["values"]}
        return tree