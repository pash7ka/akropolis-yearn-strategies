pragma solidity ^0.6.12;

interface Comptroller {
    function getCompAddress() external view returns (address);
    function oracle()  external view returns (address);

    function markets(address) external returns (bool, uint256);
    function enterMarkets(address[] calldata) external returns (uint256[] memory);
    function getAccountLiquidity(address) external view returns (uint256, uint256, uint256);
}