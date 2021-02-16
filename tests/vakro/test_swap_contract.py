import pytest
import brownie

ADEL_TO_SWAP = 100
AKRO_ON_SWAP = 10000
ADEL_AKRO_RATE = 15
EPOCH_LENGTH = 100
REWARDS_AMOUNT = 150

@pytest.fixture(scope="module")
def prepare_swap(deployer, adel, akro, vakro, stakingpool, vakroSwap):
    akro.approve(vakroSwap.address, AKRO_ON_SWAP, {'from': deployer})
    vakroSwap.addSwapLiquidity(AKRO_ON_SWAP, {'from': deployer})

    vakro.addMinter(vakroSwap.address, {'from': deployer})
    vakro.addSender(vakroSwap.address, {'from': deployer})

    adel.addMinter(vakroSwap.address, {'from': deployer})

    stakingpool.setSwapContract(vakroSwap.address, {'from': deployer})

    vakroSwap.setSwapRate(ADEL_AKRO_RATE, {'from': deployer})

def hexify(s):
    return s.encode("utf-8").hex()

def test_swap_adel(chain, deployer, akro, adel, vakro, vakroSwap, prepare_swap, regular_user):
    adel_balance_before = adel.balanceOf(regular_user)
    akro_balance_before = akro.balanceOf(regular_user)
    swap_akro_balance_before = akro.balanceOf(vakroSwap.address)

    assert vakro.balanceOf(regular_user) == 0
    assert adel.balanceOf(vakroSwap.address) == 0

    ###
    # Action performed
    ###
    adel.approve(vakroSwap.address, ADEL_TO_SWAP, {'from': regular_user})
    vakroSwap.swapFromAdel(ADEL_TO_SWAP, {'from': regular_user})

    adel_balance_after = adel.balanceOf(regular_user)
    akro_balance_after = akro.balanceOf(regular_user)
    swap_akro_balance_after = akro.balanceOf(vakroSwap.address)

    # User has swapped ADEL and get vAkro. No new AKRO
    assert adel_balance_before - adel_balance_after == ADEL_TO_SWAP
    assert akro_balance_before == akro_balance_after
    assert vakro.balanceOf(regular_user) == ADEL_TO_SWAP * ADEL_AKRO_RATE

    locked, unlocked, unlockable = vakro.balanceInfoOf(regular_user)
    assert locked == ADEL_TO_SWAP * ADEL_AKRO_RATE
    assert unlocked == 0
    assert unlockable == 0

    # Swap has burned ADEL, minted vAkro for the user and sent AKRO to vAkro
    assert adel.balanceOf(vakroSwap.address) == 0
    assert swap_akro_balance_before - swap_akro_balance_after == ADEL_TO_SWAP * ADEL_AKRO_RATE
    assert vakroSwap.swapLiquidity() == AKRO_ON_SWAP - ADEL_TO_SWAP * ADEL_AKRO_RATE
    assert vakro.balanceOf(vakroSwap.address) == 0

    assert akro.balanceOf(vakro.address) == ADEL_TO_SWAP * ADEL_AKRO_RATE

    # get vesting for the user
    start = chain.time()
    chain.mine(1, start + EPOCH_LENGTH)

    vakro.unlockAndRedeemAll({'from' : regular_user})


def test_swap_staked_adel(chain, deployer, akro, adel, vakro, stakingpool, vakroSwap, prepare_swap, regular_user2):
    #Return liquidity from the previous step
    akro.approve(vakroSwap.address, ADEL_TO_SWAP * ADEL_AKRO_RATE, {'from': deployer})
    vakroSwap.addSwapLiquidity(ADEL_TO_SWAP * ADEL_AKRO_RATE, {'from': deployer})

    assert adel.balanceOf(stakingpool.address) == 0

    adel.approve(stakingpool.address, ADEL_TO_SWAP, {'from': regular_user2})
    stakingpool.stake(ADEL_TO_SWAP, hexify("Some string"), {'from': regular_user2})
    
    assert adel.balanceOf(stakingpool.address) == ADEL_TO_SWAP
    assert stakingpool.totalStakedFor(regular_user2) == ADEL_TO_SWAP

    adel_balance_before = adel.balanceOf(regular_user2)
    akro_balance_before = akro.balanceOf(regular_user2)
    swap_akro_balance_before = akro.balanceOf(vakroSwap.address)
    staking_adel_balance_before = adel.balanceOf(stakingpool.address)

    assert vakro.balanceOf(regular_user2) == 0
    assert adel.balanceOf(vakroSwap.address) == 0


    start = chain.time()
    chain.mine(1, start + EPOCH_LENGTH)
    ###
    # Action performed
    ###
    vakroSwap.swapFromStakedAdel(ADEL_TO_SWAP, hexify("Some string"), {'from': regular_user2})
    
    adel_balance_after = adel.balanceOf(regular_user2)
    akro_balance_after = akro.balanceOf(regular_user2)
    swap_akro_balance_after = akro.balanceOf(vakroSwap.address)
    staking_adel_balance_after = adel.balanceOf(stakingpool.address)

     # User has swapped ADEL and get vAkro. No new AKRO or ADEL for user
    assert adel_balance_before == adel_balance_after
    assert akro_balance_before == akro_balance_after
    assert vakro.balanceOf(regular_user2) == ADEL_TO_SWAP * ADEL_AKRO_RATE

    locked, unlocked, unlockable = vakro.balanceInfoOf(regular_user2)
    assert locked == ADEL_TO_SWAP * ADEL_AKRO_RATE
    assert unlocked == 0
    assert unlockable == 0

    # Swap has burned ADEL, minted vAkro for the user and sent AKRO to vAkro
    assert adel.balanceOf(vakroSwap.address) == 0
    assert swap_akro_balance_before - swap_akro_balance_after == ADEL_TO_SWAP * ADEL_AKRO_RATE
    assert vakroSwap.swapLiquidity() == AKRO_ON_SWAP - ADEL_TO_SWAP * ADEL_AKRO_RATE
    assert vakro.balanceOf(vakroSwap.address) == 0

    assert akro.balanceOf(vakro.address) == ADEL_TO_SWAP * ADEL_AKRO_RATE

    # Stake was burned
    assert staking_adel_balance_before - staking_adel_balance_after == ADEL_TO_SWAP
    assert stakingpool.totalStakedFor(regular_user2) == 0

    # get vesting for the user
    start = chain.time()
    chain.mine(1, start + EPOCH_LENGTH)

    vakro.unlockAndRedeemAll({'from' : regular_user2})



def test_swap_rewards_adel(chain, deployer, akro, adel, vakro, rewardmodule, stakingpool, vakroSwap, setup_rewards, prepare_swap, regular_user3):
    #Return liquidity from the previous step
    akro.approve(vakroSwap.address, ADEL_TO_SWAP * ADEL_AKRO_RATE, {'from': deployer})
    vakroSwap.addSwapLiquidity(ADEL_TO_SWAP * ADEL_AKRO_RATE, {'from': deployer})

    assert adel.balanceOf(stakingpool.address) == 0

    adel.approve(stakingpool.address, ADEL_TO_SWAP, {'from': regular_user3})
    stakingpool.stake(ADEL_TO_SWAP, hexify("Some string"), {'from': regular_user3})
    
    assert adel.balanceOf(stakingpool.address) == ADEL_TO_SWAP
    assert stakingpool.totalStakedFor(regular_user3) == ADEL_TO_SWAP

    adel_balance_before = adel.balanceOf(regular_user3)
    akro_balance_before = akro.balanceOf(regular_user3)
    swap_akro_balance_before = akro.balanceOf(vakroSwap.address)
    staking_adel_balance_before = adel.balanceOf(stakingpool.address)

    assert vakro.balanceOf(regular_user3) == 0
    assert adel.balanceOf(vakroSwap.address) == 0


    start = chain.time()
    chain.mine(1, start + EPOCH_LENGTH)
    # Get rewards for vesting
    stakingpool.claimRewardsFromVesting({'from': deployer})
    assert adel.balanceOf(stakingpool.address) == ADEL_TO_SWAP + REWARDS_AMOUNT
    ###
    # Action performed
    ###
    vakroSwap.swapFromRewardAdel({'from': regular_user3})
    
    adel_balance_after = adel.balanceOf(regular_user3)
    akro_balance_after = akro.balanceOf(regular_user3)
    swap_akro_balance_after = akro.balanceOf(vakroSwap.address)
    staking_adel_balance_after = adel.balanceOf(stakingpool.address)

     # User has swapped ADEL rewards and get vAkro. No new AKRO or ADEL for user
    assert adel_balance_before == adel_balance_after
    assert akro_balance_before == akro_balance_after
    assert vakro.balanceOf(regular_user3) == REWARDS_AMOUNT * ADEL_AKRO_RATE

    locked, unlocked, unlockable = vakro.balanceInfoOf(regular_user3)
    assert locked == REWARDS_AMOUNT * ADEL_AKRO_RATE
    assert unlocked == 0
    assert unlockable == 0

    # Swap has burned rewards ADEL, minted vAkro for the user and sent AKRO to vAkro
    assert adel.balanceOf(vakroSwap.address) == 0
    assert swap_akro_balance_before - swap_akro_balance_after == REWARDS_AMOUNT * ADEL_AKRO_RATE
    assert vakroSwap.swapLiquidity() == AKRO_ON_SWAP - REWARDS_AMOUNT * ADEL_AKRO_RATE
    assert vakro.balanceOf(vakroSwap.address) == 0

    assert akro.balanceOf(vakro.address) == REWARDS_AMOUNT * ADEL_AKRO_RATE

    # Stake was unchanged
    assert staking_adel_balance_before - staking_adel_balance_after == 0
    assert stakingpool.totalStakedFor(regular_user3) == ADEL_TO_SWAP
