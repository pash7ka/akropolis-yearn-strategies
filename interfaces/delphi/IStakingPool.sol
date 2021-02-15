// SPDX-License-Identifier: AGPL V3.0
pragma solidity ^0.6.12;

interface IStakingPool { 
    function withdrawStakeForSwap(address _user, uint256 _amount, bytes calldata _data) external;
    function withdrawRewardForSwap(address _user, address _token) external;
}