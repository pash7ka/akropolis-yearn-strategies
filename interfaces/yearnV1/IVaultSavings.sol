// SPDX-License-Identifier: AGPL V3.0

pragma solidity ^0.6.12;


//solhint-disable func-order
interface IVaultSavings {

    event VaultRegistered(address indexed vault, address baseToken);
    event VaultDisabled(address indexed vault);

    event Deposit(address indexed vault, address indexed user, uint256 nAmount);
    event WithdrawToken(address indexed vault, address indexed token, uint256 dnAmount);
    event Withdraw(address indexed vault, address indexed user, uint256 nAmount);

    function deposit(address[] calldata _vaults, uint256[] calldata _amounts) external;

    function withdraw(address[] calldata _vaults, uint256[] calldata _amounts) external;

    function registerVault(address _vault) external;

    function disableVault(address _vault) external;
    
    //view functions
    function isVaultRegistered(address _vault) external view returns(bool);

    function supportedVaults() external view returns(address[] memory);
    
    //logic functions
    function isBaseTokenForVault(address _vault, address _token) external view returns(bool);
}