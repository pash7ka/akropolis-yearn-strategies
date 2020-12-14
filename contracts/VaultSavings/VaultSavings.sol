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


    address[] internal registeredVaults;
    mapping(address => VaultInfo) vaults;
    mapping(address => address) poolTokenToVault;


    event VaultRegistered(address vault, address baseToken);
    event Deposit(address indexed vault, address indexed user, uint256 nAmount);
    event WithdrawToken(address indexed vault, address indexed token, uint256 dnAmount);
    event Withdraw(address indexed vault, address indexed user, uint256 nAmount, uint256 nFee);

    function deposit(address _vault, _amount) external returns(uint256) {

    }

    function withdraw(address _vaultvault, _amount) external returns(uint256) {

    }

    function registerVault(address _vault, address _baseToken) external {
        require(!isVaultRegistered(address(vault)), "Vault is already registered");
        registeredVaults.push(_vault);
        poolTokenToVault[_baseToken] = address(_vault);

        emit VaultRegistered(_vault, _baseToken);
    }
    
    //view functions
    function isVaultRegistered(address _vault) public view returns(bool) {

    }
    function vaultInfoByvault(address _vault) external view returns(address, address) {

    }
    function supportedVaults() public view returns(address[] memory) {
        return registeredVaults;
    }
    
    //logic functions
    function isBaseTokenForVault(address _vault, _token) public view returns(bool) {

    }
}