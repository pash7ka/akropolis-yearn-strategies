// SPDX-License-Identifier: AGPL V3.0

pragma solidity ^0.6.12;
pragma experimental ABIEncoderV2;

import "@openzeppelinV3/contracts/token/ERC20/IERC20.sol";
import "@openzeppelinV3/contracts/token/ERC20/SafeERC20.sol";
import "@openzeppelinV3/contracts/utils/Address.sol";
import "@openzeppelinV3/contracts/math/SafeMath.sol";
import "@openzeppelinV3/contracts/Access/Ownable.sol";
import "@openzeppelinV3/contracts/utils/ReentrancyGuard.sol";

import "../../interfaces/IVault.sol";
import "../../interfaces/IVaultSavings.sol";
import "../../interfaces/IYRegistry.sol";

contract VaultSavings is IVaultSavings, Ownable, ReentrancyGuard {

    uint256 constant MAX_UINT256 = uint256(-1);

    using SafeERC20 for IERC20;
    using Address for address;
    using SafeMath for uint256;

    struct VaultInfo {
        bool isActive;
        uint256 blockNumber;
    }

    address[] internal registeredVaults;
    mapping(address => VaultInfo) vaults;

    address registry;

    function initialize(address _registry) public onlyOwner {
        registry = _registry;
    }
    
   
    function deposit(address _vault, uint256 _amount) external override nonReentrant  {
        //check vault
        require(isVaultRegistered(_vault), "Vault is not Registered");

        ( , address baseToken,  ,  ,) = IYRegistry(registry).getVaultInfo(_vault);
     
        //transfer token if it is allowed to contract
        IERC20(baseToken).safeTransferFrom(msg.sender, address(this), _amount);

        //set allowence to vault
        IERC20(baseToken).safeIncreaseAllowance(_vault, _amount);

        //deposit token to vault
        IVault(_vault).deposit(_amount);

        //send new tokens to user
        IERC20(_vault).safeTransfer(msg.sender, IERC20(_vault).balanceOf(address(this)));

        emit  Deposit(_vault, msg.sender, _amount);
    }

    function withdraw(address _vault, uint256 _amount) external override nonReentrant {
        require(isVaultRegistered(_vault), "Vault is not Registered");
        //transfer LP Token if it is allowed to contract
        IERC20(_vault).safeTransferFrom(msg.sender, address(this), _amount);

        //burn tokens from vault
        IVault(_vault).withdraw(_amount);

        ( , address baseToken,  ,  ,) = IYRegistry(registry).getVaultInfo(_vault);

        //Transfer token to user
        IERC20(baseToken).safeTransfer(msg.sender, IERC20(baseToken).balanceOf(address(this)));

        emit Withdraw(_vault, msg.sender, _amount);
    }

    function registerVault(address _vault) external override {
        require(!isVaultRegistered(_vault), "Vault is already registered");

        registeredVaults.push(_vault);

        vaults[_vault] = VaultInfo({
            isActive: true,
            blockNumber: block.number
        });

        (, address baseToken,  ,  ,) = IYRegistry(registry).getVaultInfo(_vault);

        emit VaultRegistered(_vault, baseToken);
    }

    function disableVault(address _vault) external override {
        require(isVaultRegistered(_vault), "Vault is not registered");
        (, address baseToken,  ,  ,) = IYRegistry(_vault).getVaultInfo(_vault);
        vaults[_vault] = VaultInfo({
            isActive: false,
            blockNumber: block.number
        });

       emit VaultDisabled(_vault);
    }
    

    //view functions
    function isVaultRegistered(address _vault) public override view returns(bool) {
        for (uint256 i = 0; i < registeredVaults.length; i++){
            if (registeredVaults[i] == _vault) return true;
        }
        return false;
    }

    function supportedVaults() external override view returns(address[] memory) {
        return registeredVaults;
    }
    
    function isBaseTokenForVault(address _vault, address _token) public override view returns(bool) {
        (, address baseToken,  ,  ,) = IYRegistry(registry).getVaultInfo(_vault);
        if (baseToken == _token) return true;
        return false;
    }
}