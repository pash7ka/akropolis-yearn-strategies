pragma solidity ^0.6.12;

interface PriceFeed {
    function getUnderlyingPrice(address cToken) external view returns (uint256);
}