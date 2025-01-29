# Verifier Contract

## Overview
The Verifier contract is an abstract smart contract that allows for efficient and secure verification of Merkle proofs and addresses. It provides functionality to verify if a provided proof matches a stored root and to verify the validity of an address using a Merkle proof.

This contract is designed to be extensible and can be inherited and used by other contracts to provide Merkle tree-based proof verification.
## Features
- Merkle Proof Verification: The contract can verify a proof against a known root.
- Address Verification: The contract can verify if a given address is valid according to a provided Merkle proof.
- Ownership Management: The owner of the contract can update the root and transfer ownership of the contract.
- Efficient Hashing: Uses efficient hashing for Merkle proof processing.

## Contract Methods

1. verify(bytes32[] memory proof, bytes32 leaf) internal view returns (bool)

Verifies if the provided proof for a leaf matches the stored root.

- proof: An array of bytes32 values representing the Merkle proof.
- leaf: The leaf node to verify.

Returns true if the proof is valid, otherwise false.

2. verifyaddress(bytes32[] memory proof, address addr) internal view returns (bool)

Verifies if the provided address is valid according to the Merkle proof.

- proof: An array of bytes32 values representing the Merkle proof.
- addr: The address to verify.

Returns true if the address is valid, otherwise false.

3. processProof(bytes32[] memory proof, bytes32 leaf) internal pure returns (bytes32)

Processes the proof to compute the hash from the leaf and proof data.

- proof: An array of bytes32 values representing the Merkle proof.
- leaf: The leaf node to verify.

Returns the computed hash after processing the proof.

4. setRoot(bytes32 root) public virtual

Sets a new root value. Only the contract owner can call this function.

- root: The new root value to set.

5. transferOwnership(address newOwner) public virtual

Transfers ownership of the contract to a new address. Only the current owner can call this function.

- newOwner: The address to transfer ownership to.

6. owner() public view virtual returns (address)

Returns the current owner’s address.

7. getRoot() public view virtual returns (bytes32)

Returns the current root value stored in the contract.

## Usage

### Installation
```sh
npm install verifier-contract
```

### Deploying the Contract

1. Deploy the contract with an initial root value.
```solidity
bytes32 initialRoot = 0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef;
Verifier verifier = new Verifier(initialRoot);
```

### Verifying a Proof

1. You can verify a proof for a leaf node by calling the verify function.
```solidity
bytes32 leaf = 0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890;
bytes32[] memory proof = [0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890];
bool isValid = verifier.verify(proof, leaf);
```
    
2. To verify an address, you can call the verifyaddress function.
```solidity
address addr = 0x1234567890abcdef1234567890abcdef12345678;
bytes32[] memory proof = [0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890];
bool isValidAddress = verifier.verifyaddress(proof, addr);
```

3. Updating the Root

Only the owner can update the root. To set a new root, the owner can call:
```solidity
verifier.setRoot(newRoot);
```

4. Transferring Ownership

To transfer ownership to another address, the current owner can call:
```solidity
verifier.transferOwnership(newOwnerAddress);
```

## Example

Here is a full example of how you might deploy and interact with the contract in a JavaScript file using Hardhat:
```js
const { ethers } = require("hardhat");

async function main() {
    const [owner] = await ethers.getSigners();

    // Set the root
    const initialRoot = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("initialRoot"));

    // Deploy the contract
    const Verifier = await ethers.getContractFactory("Verifier");
    const verifier = await Verifier.deploy(initialRoot);
    console.log("Verifier deployed to:", verifier.address);

    // Verify a proof (replace with actual proof data)
    const proof = [ethers.utils.hexlify(ethers.utils.randomBytes(32))];
    const leaf = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("leaf"));
    const isValidProof = await verifier.verify(proof, leaf);
    console.log("Is the proof valid?", isValidProof);

    // Transfer ownership
    await verifier.transferOwnership(owner.address);
    console.log("Ownership transferred to:", owner.address);
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
```
