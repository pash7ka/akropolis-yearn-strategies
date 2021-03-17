pragma solidity ^0.6.12;

interface CErc20 {
    //CTokenInterfaces.CTokenStorage 
    function comptroller() external returns(address);


    //CTokenInterfaces.CErc20Storage
    function underlying() external returns(address);

    //CTokenInterfaces.CErc20Interface
    function mint(uint256) external returns (uint256);
    function redeem(uint redeemTokens) external returns (uint256);
    function redeemUnderlying(uint redeemAmount) external returns (uint256);
    function borrow(uint256) external returns (uint256);
    function repayBorrow(uint256) external returns (uint256);

    //CTokenInterfaces.CTokenInterface
    function getAccountSnapshot(address account) external view returns (uint, uint, uint, uint); //@return (possible error, token balance, borrow balance, exchange rate mantissa)
    function borrowRatePerBlock() external view returns (uint256);
    function borrowBalanceCurrent(address) external returns (uint256);
}