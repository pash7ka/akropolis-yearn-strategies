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


    event VaultRegistered(address protocol, address baseToken);
    event Deposit(address indexed protocol, address indexed user, uint256 nAmount);
    event WithdrawToken(address indexed protocol, address indexed token, uint256 dnAmount);
    event Withdraw(address indexed protocol, address indexed user, uint256 nAmount, uint256 nFee);

    function deposit(address _protocol, _amount) external returns(uint256) {

    }

    function withdraw(address _vaultProtocol, _amount) external returns(uint256) {

    }

    function registerVault(address _protocol, address _baseToken) external {

    }
    
    //view functions
    function isVaultRegistered(address _protocol) public view returns(bool) {

    }
    function vaultInfoByProtocol(address _protocol) external view returns(address, address) {

    }
    function supportedVaults() public view returns(address[] memory) {

    }
    
    //logic functions
    function isBaseTokenForVault(address _protocol, _token) public view returns(bool) {
        
    }
}