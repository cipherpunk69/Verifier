// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

abstract contract Verifier {
    bytes32 private _root;
    address private _owner;

    constructor(bytes32 root) {
        _owner = msg.sender;
        _root = root;
    }

    function verify(bytes32[] memory proof, bytes32 leaf) internal view returns (bool) {
        return processProof(proof, leaf) == _root;
    }

    function verifyaddress(bytes32[] memory proof, address addr) internal view returns (bool) {
        return processProof(proof, keccak256(bytes.concat(keccak256(abi.encode(addr))))) == _root;
    }

    function processProof(bytes32[] memory proof, bytes32 leaf) internal pure returns (bytes32) {
        bytes32 computedHash = leaf;
        for (uint256 i = 0; i < proof.length; i++) {
            computedHash = hashPair(computedHash, proof[i]);
        }
        return computedHash;
    }

    function hashPair(bytes32 a, bytes32 b) private pure returns (bytes32) {
        return a < b ? efficientHash(a, b) : efficientHash(b, a);
    }

    function efficientHash(bytes32 a, bytes32 b) private pure returns (bytes32 value) {
        assembly {
            mstore(0x00, a)
            mstore(0x20, b)
            value := keccak256(0x00, 0x40)
        }
    }

    function setRoot(bytes32 root) public virtual {
        require(owner() == msg.sender, "Caller is not the owner");
        _root = root;
    }

    function transferOwnership(address newOwner) public virtual {
        require(owner() == msg.sender, "Caller is not the owner");
        _owner = newOwner;
    }

    function owner() public view virtual returns (address) {
        return _owner;
    }
    
    function getRoot() public view virtual returns (bytes32) {
        return _root;
    }
    
}