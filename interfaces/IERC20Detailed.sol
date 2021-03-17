// SPDX-License-Identifier: AGPL V3.0
pragma solidity ^0.6.12;

interface IERC20Detailed { 
	function name() external view returns (string memory);
	function symbol() external view returns (string memory);
	function decimals() external view returns (uint8);
}