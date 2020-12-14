pragma solidity ^0.6.12;


//solhint-disable func-order
contract IVaultSavingsExtended { 

    event DepositToken(address indexed protocol, address indexed token, uint256 dnAmount);
    function deposit(address[] calldata _protocols, address[] calldata _tokens, uint256[] calldata _dnAmounts) external returns(uint256[] memory);
    function registerVault(address _protocol, address _baseToken, address[] _tokens) external;

    function addSupportTokensToVault(address _protocol, address[] _tokens) external;

    function isSupportTokenForVault(address _protocol, _token) public view returns(bool);

    function supportTokensForVault() public view returns(address[] memory);

    function withdraw(address _vaultProtocol, address[] calldata _tokens, uint256[] calldata _amounts, bool isQuick) external returns(uint256);
}
