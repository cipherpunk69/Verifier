// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol";

contract MyToken is ERC20, Ownable, ERC20Permit, AccessControl {
    
    bytes32 public constant MINTER_ROLE = keccak256("MINTER");
    
    constructor()
        ERC20("MyToken", "MTK")
        Ownable(msg.sender)
        ERC20Permit("MyToken")
    {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }

    function addMinters(address[] memory minters) public onlyOwner {
        for (uint256 i = 0; i < minters.length; ++i) {
            grantRole(MINTER_ROLE, minters[i]);
        }
    }

    function mint(uint256 amount) public {
        // Check that the calling account has the minter role
        require(hasRole(MINTER_ROLE, msg.sender), "Caller is not a minter");
        _mint(msg.sender, amount);
    }

}