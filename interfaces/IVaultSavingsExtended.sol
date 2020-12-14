pragma solidity ^0.6.12;


//solhint-disable func-order
contract IVaultSavingsExtended { 

    event DepositToken(address indexed vault, address indexed token, uint256 dnAmount);
    
    function deposit(address[] calldata _vaults, address[] calldata _tokens, uint256[] calldata _dnAmounts) external returns(uint256[] memory);
    function deposit(address[] memory _protocols, address[] memory _tokens, uint256[] memory _dnAmounts) 

    function registerVault(address _vault, address _baseToken, address[] _tokens) external;

    function addSupportTokensToVault(address _vault, address[] _tokens) external;

    function isSupportTokenForVault(address _vault, _token) public view returns(bool);

    function supportTokensForVault() public view returns(address[] memory);

    function withdraw(address _vault, address[] calldata _tokens, uint256[] calldata _amounts) external returns(uint256);
}
