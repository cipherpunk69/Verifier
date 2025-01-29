import unittest
import os
from merkletree import MerkleTree

class TestMerkleTree(unittest.TestCase):
    def setUp(self):
        self.addresses = ['0x5B38Da6a701c568545dCfcB03FcB875f56beddC4',
                  '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2',
                    '0x4B20993Bc481177ec7E8f571ceCaE8A9e22C02db',
                    '0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB']
        self.tree = MerkleTree()
        self.tree.make_from_values(self.addresses)
        self.test_file = "merkle_tree.json"
    
    def test_root_hash(self):
        root = self.tree.getRoot()
        self.assertIsInstance(root, str)
        self.assertTrue(root.startswith("0x"))
    
    def test_proof_generation(self):
        for value in self.addresses:
            proof = self.tree.getProof(value)
            self.assertIsInstance(proof, list)
            self.assertTrue(all(isinstance(p, str) and p.startswith("0x") for p in proof))
    
    def test_dump_and_load(self):
        self.tree.dumpToFile(self.test_file)
        loaded_tree = MerkleTree.loadFromFile(self.test_file)
        self.assertEqual(self.tree.tree, loaded_tree.tree)
        self.assertEqual(self.tree.values, loaded_tree.values)
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == "__main__":
    unittest.main()