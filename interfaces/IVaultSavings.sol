pragma solidity ^0.6.12;


//solhint-disable func-order
contract IVaultSavings {
    event VaultRegistered(address protocol, address baseToken);
    event DepositToken(address indexed protocol, address indexed token, uint256 dnAmount);
    event Deposit(address indexed protocol, address indexed user, uint256 nAmount, uint256 nFee);
    event WithdrawToken(address indexed protocol, address indexed token, uint256 dnAmount);
    event Withdraw(address indexed protocol, address indexed user, uint256 nAmount, uint256 nFee);

    function deposit(address[] calldata _protocols, address[] calldata _tokens, uint256[] calldata _dnAmounts) external returns(uint256[] memory);
    function deposit(address _protocol, address[] calldata _tokens, uint256[] calldata _dnAmounts) external returns(uint256);
    function withdraw(address _vaultProtocol, address[] calldata _tokens, uint256[] calldata _amounts, bool isQuick) external returns(uint256);

    function registerVault(address _protocol, address _baseToken) external;
    function registerVault(address _protocol, address _baseToken, address[] _tokens) external;
    function addSupportTokensToVault(address _protocol, address[] _tokens) external;


    //view functions
    function isVaultRegistered(address _protocol) public view returns(bool);
    function vaultInfoByProtocol(address _protocol) external view returns(address, address);
    function supportedVaults() public view returns(address[] memory);
    function supportTokensForVault() public view returns(address[] memory);

    //logic functions
    function isBaseTokenForVault(address _protocol, _token) public view returns(bool);
    function isSupportTokenForVault(address _protocol, _token) public view returns(bool);






}