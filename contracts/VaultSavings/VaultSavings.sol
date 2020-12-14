pragma solidity ^0.6.12;
pragma experimental ABIEncoderV2;

import "@openzeppelinV3/contracts/token/ERC20/IERC20.sol";
import "@openzeppelinV3/contracts/token/ERC20/SafeERC20.sol";
import "@openzeppelinV3/contracts/utils/Address.sol";
import "@openzeppelinV3/contracts/math/SafeMath.sol";
import "../interfaces/IVault.sol";
import "../interfaces/IVaultSavings.sol";

contract VaultSavings is IVaultSavings {

    uint256 constant MAX_UINT256 = uint256(-1);
    
    using SafeERC20 for IERC20;
    using Address for address;
    using SafeMath for uint256;


}