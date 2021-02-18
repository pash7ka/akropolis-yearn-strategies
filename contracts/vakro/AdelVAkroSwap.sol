 
// SPDX-License-Identifier: AGPL V3.0
pragma solidity ^0.6.12;

import "@ozUpgradesV3/contracts/access/OwnableUpgradeable.sol";
import "@ozUpgradesV3/contracts/token/ERC20/IERC20Upgradeable.sol";
import "@ozUpgradesV3/contracts/token/ERC20/SafeERC20Upgradeable.sol";
import "@ozUpgradesV3/contracts/math/SafeMathUpgradeable.sol";
import "@ozUpgradesV3/contracts/utils/ReentrancyGuardUpgradeable.sol";

import "../../interfaces/IERC20Burnable.sol";
import "../../interfaces/IERC20Mintable.sol";
import "../../interfaces/delphi/IStakingPool.sol";

contract AdelVAkroSwap is OwnableUpgradeable, ReentrancyGuardUpgradeable {
    using SafeERC20Upgradeable for IERC20Upgradeable;
    using SafeMathUpgradeable for uint256;
 
    event AdelSwapped(address indexed receiver, uint256 adelAmount, uint256 akroAmount);

    //Addresses of affected contracts
    address public akro;
    address public adel;
    address public vakro;
    address public stakingPool;
    address public rewardStakingPool;

    //Swap settings
    uint256 public minAmountToSwap = 0;
    uint256 public swapRateNumerator = 0;   //Amount of vAkro for 1 ADEL - 0 by default
    uint256 public swapRateDenominator = 1; //Akro amount = Adel amount * swapRateNumerator / swapRateDenominator
                                            //1 Adel = swapRateNumerator/swapRateDenominator Akro

    modifier swapEnabled() {
        require(swapRateNumerator != 0, "Swap is disabled");
        _;
    }

    modifier enoughAdel(uint256 _adelAmount) {
        require(_adelAmount > 0 && _adelAmount >= minAmountToSwap, "Insufficient ADEL amount");
        _;
    }

    function initialize(address _akro, address _adel, address _vakro) public initializer {
        require(_akro != address(0), "Zero address");
        require(_adel != address(0), "Zero address");
        require(_vakro != address(0), "Zero address");

        __Ownable_init();

        akro = _akro;
        adel = _adel;
        vakro = _vakro;
    }    

    //Setters for the swap tuning

    /**
     * @notice Sets the ADEL staking pool address
     * @param _stakingPool Adel staking pool address)
     */
    function setStakingPool(address _stakingPool) public onlyOwner {
        require(_stakingPool != address(0), "Zero address");
        stakingPool = _stakingPool;
    }

    /**
     * @notice Sets the staking pool address with ADEL rewards
     * @param _rewardStakingPool Adel staking pool address)
     */
    function setRewardStakingPool(address _rewardStakingPool) public onlyOwner {
        require(_rewardStakingPool != address(0), "Zero address");
        rewardStakingPool = _rewardStakingPool;
    }

    /**
     * @notice Sets the minimum amount of ADEL which can be swapped. 0 by default
     * @param _minAmount Minimum amount in wei (the least decimals)
     */
    function setMinSwapAmount(uint256 _minAmount) public onlyOwner {
        minAmountToSwap = _minAmount;
    }

    /**
     * @notice Sets the rate of ADEL to vAKRO swap: 1 ADEL = _swapRateNumerator/_swapRateDenominator vAKRO
     * @notice By default is set to 0, that means that swap is disabled
     * @param _swapRateNumerator Numerator for Adel converting. Can be set to 0 - that stops the swap.
     * @param _swapRateDenominator Denominator for Adel converting. Can't be set to 0
     */
    function setSwapRate(uint256 _swapRateNumerator, uint256 _swapRateDenominator) public onlyOwner {
        require(_swapRateDenominator > 0, "Incorrect value");
        swapRateNumerator = _swapRateNumerator;
        swapRateDenominator = _swapRateDenominator;
    }

    /**
     * @notice Withdraws all ADEL collected on a Swap contract
     * @param _recepient Recepient of ADEL.
     */
    function withdrawAdel(address _recepient) public onlyOwner {
        require(_recepient != address(0), "Zero address");
        uint256 _adelAmount = IERC20Upgradeable(adel).balanceOf(address(this));
        require(_adelAmount > 0, "Nothing to withdraw");
        IERC20Upgradeable(adel).safeTransfer(_recepient, _adelAmount);
    }

    /**
     * @notice Allows to swap ADEL token from the wallet for vAKRO
     * @param _adelAmount Amout of ADEL the user approves for the swap.
     */
    function swapFromAdel(uint256 _adelAmount) public nonReentrant swapEnabled enoughAdel(_adelAmount)
    {
        IERC20Upgradeable(adel).safeTransferFrom(_msgSender(), address(this), _adelAmount);

        swap(_adelAmount);
    }
    

    /**
     * @notice Allows to swap ADEL token which is currently staked in StakingPool
     * @param _data Data for unstaking.
     */
    function swapFromStakedAdel(bytes memory _data) public nonReentrant swapEnabled
    {
        require(stakingPool != address(0), "Swap from stake is disabled");
        
        uint256 adelBefore = IERC20Upgradeable(adel).balanceOf(address(this));
        uint256 _adelAmount = IStakingPool(stakingPool).withdrawStakeForSwap(_msgSender(), _data);
        uint256 adelAfter = IERC20Upgradeable(adel).balanceOf(address(this));
        
        require( adelAfter - adelBefore == _adelAmount, "ADEL was not transferred");
                
        swap(_adelAmount);
    }

    /**
     * @notice Allows to swap ADEL token which belongs to vested unclaimed rewards
     */
    function swapFromRewardAdel() public nonReentrant swapEnabled
    {
        require(rewardStakingPool != address(0), "Swap from reards is disabled");

        uint256 adelBefore = IERC20Upgradeable(adel).balanceOf(address(this));
        uint256 _adelAmount = IStakingPool(rewardStakingPool).withdrawRewardForSwap(_msgSender(), adel);
        uint256 adelAfter = IERC20Upgradeable(adel).balanceOf(address(this));

        require( adelAfter - adelBefore == _adelAmount, "ADEL was not transferred");
        
        swap(_adelAmount);
    }


    /**
     * @notice Internal function to collect ADEL and mint vAkro for the sender
     * @param _adelAmount Amout of ADEL the contract needs to swap.
     */
    function swap(uint256 _adelAmount) internal
    {
        require(_adelAmount != 0 && _adelAmount >= minAmountToSwap, "Not enough ADEL");

        uint256 vAkroAmount = _adelAmount.mul(swapRateNumerator).div(swapRateDenominator);

        IERC20Mintable(vakro).mint(address(this), vAkroAmount);
        IERC20Upgradeable(vakro).transfer(_msgSender(), vAkroAmount);

        emit AdelSwapped(_msgSender(), _adelAmount, vAkroAmount);
    }
}