// SPDX-License-Identifier: MIT

pragma solidity ^0.6.12;

import "../../../interfaces/yearnV1/IController.sol";
import "../../../interfaces/yearnV1/IStrategy.sol";
import "../../../interfaces/yearnV1/IVault.sol";
import "../../../interfaces/yearnV1/IWrappedVault.sol";

contract YTestController {

    mapping(address => address) public _vaults;
    mapping(address => address) public _strategies;
    function withdraw(address, uint256) public {

    }

    function balanceOf(address) public view returns (uint256) {
        return 0;
    }

    function earn(address, uint256) public {

    }

    function want(address) public view returns (address) {
        return address(this);
    }

    function rewards() public view returns (address) {
        return address(this);
    }

    function vaults(address _token) public view returns (address) {
        return _vaults[_token];
    }

    function strategies(address _token) public view returns (address) {
        return _strategies[_token];
    }

    function approvedStrategies(address, address) public view returns (bool) {
        return true;
    }

    function setVault(address _token, address _vault) public {
        require(_vaults[_token] == address(0), "vault");
        _vaults[_token] = _vault;
    }

    function setStrategy(address _token, address _strategy) public {
        _strategies[_token] = _strategy;
    }
}