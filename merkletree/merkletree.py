from Crypto.Hash import keccak
from eth_abi import encode
from typing import NamedTuple
import math
from functools import cmp_to_key
import json

def compare_bytes(a, b):
    n = min(len(a), len(b))
    i = 0
    while(i < n):
        if(a[i] != b[i]):
            return a[i] - b[i]
        else:
            i = i + 1
    return len(a) - len(b)

def hashPair(a, b):
    keccak_hash = keccak.new(digest_bits=256, update_after_digest=True)
    keccak_hash.update(b''.join(sorted([a, b], key=cmp_to_key(compare_bytes))))
    return keccak_hash.digest()

def leftChildIndex(i):
    return 2 * i + 1

def rightChildIndex(i):
    return 2 * i + 2

def siblingIndex(i):
    return i  - (-1) ** (i % 2)

def parentIndex(i):
    return math.floor((i - 1) / 2)

def _to_hex(x):
    return '0x' + x.hex()


class Leaf(NamedTuple):
    value: bytes
    hash: bytes

    def __lt__(self, other) -> bool:
        diff = compare_bytes(self.hash, other.hash)
        if diff > 0:
            return False
        elif diff < 0:
            return True
        elif diff == 0:
            return False

class MerkleTree(object):
    def __init__(self):
        self.reset_tree()
        
    def reset_tree(self):
        self.hashed_values = list()
        self.tree = list()
        self.values = dict()
    
    def make_from_values(self, values):
        for v in values:
            leaf = Leaf(v, self.leafHash(v))
            self.hashed_values.append(leaf)
        self.hashed_values = sorted(self.hashed_values)
        for i in range(2 * len(self.hashed_values) - 1):
            self.tree.append(bytes)
        i = 0
        for v in self.hashed_values:
            self.tree[len(self.tree) - 1 - i] = v.hash
            i = i + 1
        i = len(self.tree) - 1 - len(self.hashed_values)
        while(i >= 0):
            self.tree[i] = hashPair(self.tree[leftChildIndex(i)], self.tree[rightChildIndex(i)])
            i = i - 1
        self.values = { value: 0 for value in values }
        i = 0
        for v in self.hashed_values:
            self.values[v.value] = len(self.tree) - i - 1
            i = i + 1

    def getProof(self, value):
        index = self.values[value]
        proof = []
        while(index > 0):
            proof.append(self.tree[siblingIndex(index)])
            index = parentIndex(index)
        result = [_to_hex(x) for x in proof]
        return result

    def leafHash(self, leaf):
        keccak_hash = keccak.new(digest_bits=256, update_after_digest=True)   
        keccak_hash.update((encode(['address'], [leaf])))
        leaf = keccak_hash.digest()
        keccak_hash = keccak.new(digest_bits=256, update_after_digest=True)
        keccak_hash.update(leaf)
        leaf = keccak_hash.digest()
        return leaf

    def getRoot(self):
        return _to_hex(self.tree[0])
    
    def dumpToFile(self, filename):
        hex_tree = list()
        values = list()
        for hash in self.tree:
            hex_tree.append(_to_hex(hash))
        for value in self.values:
            values.append({"value" : value, "treeIndex" : self.values[value]})
        formatted = {
            "tree" : hex_tree,
            "values" : values
        }
        json_object = json.dumps(formatted, indent=2)
        with open(filename, "w") as outfile:
            outfile.write(json_object)

