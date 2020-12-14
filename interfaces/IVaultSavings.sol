pragma solidity ^0.6.12;


//solhint-disable func-order
contract IVaultSavings {
    event VaultRegistered(address vault, address baseToken);
    event Deposit(address indexed vault, address indexed user, uint256 nAmount);
    event WithdrawToken(address indexed vault, address indexed token, uint256 dnAmount);
    event Withdraw(address indexed vault, address indexed user, uint256 nAmount, uint256 nFee);

    function deposit(address _vault, _amount) external returns(uint256);

    function withdraw(address _vaultvault, _amount) external returns(uint256);

    function registerVault(address _vault, address _baseToken) external;
    
    //view functions
    function isVaultRegistered(address _vault) public view returns(bool);
    function vaultInfoByvault(address _vault) external view returns(address, address);
    function supportedVaults() public view returns(address[] memory);
    
    //logic functions
    function isBaseTokenForVault(address _vault, _token) public view returns(bool);

}