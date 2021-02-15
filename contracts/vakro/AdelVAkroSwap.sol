 
// SPDX-License-Identifier: AGPL V3.0
pragma solidity ^0.6.12;

import "@openzeppelin/contracts/proxy/Initializable.sol";
import "@openzeppelin/contracts/GSN/Context.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/SafeERC20.sol";
import "@openzeppelin/contracts/math/SafeMath.sol";

import "../../interfaces/IERC20Burnable.sol";
import "../../interfaces/IERC20Mintable.sol";
import "../../interfaces/delphi/IStakingPool.sol";

contract AdelVAkroSwap is Initializable, Context, Ownable {
    using SafeERC20 for IERC20;
    using SafeMath for uint256;
 
    event AkroAdded(uint256 amount);
    event AdelSwapped(address indexed receiver, uint256 adelAmount, uint256 akroAmount);

    //Addresses of affected contracts
    address public akro;
    address public adel;
    address public vakro;
    address public stakingPool;

    //Swap settings
    uint256 minAmountToSwap = 0;
    uint256 swapRate = 0; //Amount of vAkro for 1 ADEL

    uint256 swapLiquidity = 0;

    modifier swapEnabled() {
        require(swapRate != 0, "Swap is disabled");
        _;
    }

    modifier enoughAdel(uint256 _adelAmount) {
        require(_adelAmount > 0 && _adelAmount >= minAmountToSwap, "Insufficient ADEL amount");
        _;
    }

    function initialize(address _akro, address _adel, address _vakro, address _stakingPool) public initializer {
        require(_akro != address(0), "Zero address");
        require(_adel != address(0), "Zero address");
        require(_vakro != address(0), "Zero address");
        require(_stakingPool != address(0), "Zero address");

        akro = _akro;
        adel = _adel;
        vakro = _vakro;
        stakingPool = _stakingPool;
    }    

    //Setters for the swap tuning

    /**
     * @notice Sets the minimum amount of ADEL which can be swapped. 0 by default
     * @param _minAmount Minimum amount in wei (the least decimals)
     */
    function setMinSwapAmount(uint256 _minAmount) public onlyOwner {
        minAmountToSwap = _minAmount;
    }

    /**
     * @notice Sets the rate of ADEL to vAKRO swap - how many vAKRO for 1 ADEL
     * @notice By default is set to 0, that means that swap is disabled
     * @param _swapRate Amout of vAKRO for 1 ADEL. Can be set to 0 - that stops the swap.
     */
    function setSwapRate(uint256 _swapRate) public onlyOwner {
        swapRate = _swapRate;
    }

    /**
     * @notice Adds AKRO liquidity to the swap contract
     * @param _amount Amout of AKRO added to the contract.
     */
    function addSwapLiquidity(uint256 _amount) public {
        require(_amount > 0, "Incorrect amount");
        
        IERC20(akro).safeTransferFrom(_msgSender(), address(this), _amount);
        swapLiquidity = swapLiquidity.add(_amount);
        
        emit AkroAdded(_amount);
    }

    /**
     * @notice Allows to swap ADEL token from the wallet for vAKRO
     * @param _adelAmount Amout of ADEL the user approves for the swap.
     */
    function swapFromAdel(uint256 _adelAmount) public swapEnabled enoughAdel(_adelAmount)
    {
        uint256 vAkroAmount = _adelAmount.mul(swapRate);
        require(swapLiquidity >= vAkroAmount, "Not enough AKRO");

        IERC20(adel).safeTransferFrom(_msgSender(), address(this), _adelAmount);

        burnAndSwap(_adelAmount, vAkroAmount);
    }
    

    /**
     * @notice Allows to swap ADEL token which is currently staked in StakingPool
     * @param _adelAmount Amout of ADEL the user has available to unstake in staking pool.
     * @param _data Data for unstaking.
     */
    function swapFromStakedAdel(uint256 _adelAmount, bytes memory _data) public swapEnabled enoughAdel(_adelAmount)
    {
        uint256 vAkroAmount = _adelAmount.mul(swapRate);
        require(swapLiquidity >= vAkroAmount, "Not enough AKRO");

        IStakingPool(stakingPool).withdrawStakeForSwap(_msgSender(), _adelAmount, _data);
        require(IERC20(adel).balanceOf(address(this)) == _adelAmount, "ADEL was not transferred");
        
        burnAndSwap(_adelAmount, vAkroAmount);
    }

    /**
     * @notice Allows to swap ADEL token which belongs to vested unclaimed rewards
     * @param _adelAmount Amout of ADEL the user has available to unstake in staking pool.
     */
    function swapFromRewardAdel() public swapEnabled
    {
        uint256 vAkroAmount = _adelAmount.mul(swapRate);
        require(swapLiquidity >= vAkroAmount, "Not enough AKRO");

        IStakingPool(stakingPool).withdrawRewardForSwap(_msgSender(), adel);

        uint256 _adelAmount = IERC20(adel).balanceOf(address(this));

        require(_adelAmount != 0 && _adelAmount >= minAmountToSwap, "Not enough ADEL rewards");
        
        burnAndSwap(_adelAmount, vAkroAmount);
    }


    /**
     * @notice Internal function to burn ADEL and mint vAkro for the sender
     * @param _adelAmount Amout of ADEL the contract needs to burn.
     * @param vAkroAmount Amout of vAkro the contract needs to mint.
     */
    function burnAndSwap(uint256 _adelAmount, uint256 vAkroAmount) internal
    {
        IERC20Burnable(adel).burn(_adelAmount);

        swapLiquidity = swapLiquidity.sub(vAkroAmount);
        
        IERC20(akro).approve(vakro, vAkroAmount);
        IERC20Mintable(vakro).mint(address(this), vAkroAmount);
        IERC20(vakro).transfer(_msgSender(), vAkroAmount);

        emit AdelSwapped(_msgSender(), _adelAmount, vAkroAmount);
    }
}