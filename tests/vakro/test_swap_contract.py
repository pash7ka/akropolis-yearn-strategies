import pytest
import brownie

ADEL_TO_SWAP = 100
AKRO_ON_SWAP = 10000
ADEL_AKRO_RATE = 15
EPOCH_LENGTH = 100
REWARDS_AMOUNT = 150

@pytest.fixture(scope="module")
def prepare_swap(deployer, adel, akro, vakro, stakingpool, vakroSwap):

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

    assert vakro.balanceOf(regular_user) == 0
    assert adel.balanceOf(vakroSwap.address) == 0

    ###
    # Action performed
    ###
    vakro.setVestingCliff(0, {'from': deployer})
    start = chain.time() + 50
    vakro.setVestingStart(start, {'from': deployer})
    chain.mine(1)

    adel.approve(vakroSwap.address, ADEL_TO_SWAP, {'from': regular_user})
    vakroSwap.swapFromAdel(ADEL_TO_SWAP, {'from': regular_user})

    adel_balance_after = adel.balanceOf(regular_user)
    akro_balance_after = akro.balanceOf(regular_user)

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
    assert vakro.balanceOf(vakroSwap.address) == 0

    akro.approve(vakro.address, ADEL_TO_SWAP * ADEL_AKRO_RATE, {'from': deployer})
    vakro.addAkroLiquidity(ADEL_TO_SWAP * ADEL_AKRO_RATE, {'from': deployer})

    assert akro.balanceOf(vakro.address) == ADEL_TO_SWAP * ADEL_AKRO_RATE

    # get vesting for the user
    chain.mine(1, start + EPOCH_LENGTH)

    vakro.unlockAndRedeemAll({'from' : regular_user})


def test_swap_staked_adel(chain, deployer, akro, adel, vakro, stakingpool, vakroSwap, prepare_swap, regular_user2):
    assert adel.balanceOf(stakingpool.address) == 0

    adel.approve(stakingpool.address, ADEL_TO_SWAP, {'from': regular_user2})
    stakingpool.stake(ADEL_TO_SWAP, hexify("Some string"), {'from': regular_user2})
    
    assert adel.balanceOf(stakingpool.address) == ADEL_TO_SWAP
    assert stakingpool.totalStakedFor(regular_user2) == ADEL_TO_SWAP

    adel_balance_before = adel.balanceOf(regular_user2)
    akro_balance_before = akro.balanceOf(regular_user2)
    staking_adel_balance_before = adel.balanceOf(stakingpool.address)

    assert vakro.balanceOf(regular_user2) == 0
    assert adel.balanceOf(vakroSwap.address) == 0


    start = chain.time()
    chain.mine(1, start + EPOCH_LENGTH)
    ###
    # Action performed
    ###
    vakro.setVestingCliff(0, {'from': deployer})
    start = chain.time() + 50
    vakro.setVestingStart(start, {'from': deployer})
    chain.mine(1)

    vakroSwap.swapFromStakedAdel(hexify("Some string"), {'from': regular_user2})
    
    adel_balance_after = adel.balanceOf(regular_user2)
    akro_balance_after = akro.balanceOf(regular_user2)
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
    assert vakro.balanceOf(vakroSwap.address) == 0

    akro.approve(vakro.address, ADEL_TO_SWAP * ADEL_AKRO_RATE, {'from': deployer})
    vakro.addAkroLiquidity(ADEL_TO_SWAP * ADEL_AKRO_RATE, {'from': deployer})

    assert akro.balanceOf(vakro.address) == ADEL_TO_SWAP * ADEL_AKRO_RATE

    # Stake was burned
    assert staking_adel_balance_before - staking_adel_balance_after == ADEL_TO_SWAP
    assert stakingpool.totalStakedFor(regular_user2) == 0

    # get vesting for the user
    chain.mine(1, start + EPOCH_LENGTH)

    vakro.unlockAndRedeemAll({'from' : regular_user2})



def test_swap_rewards_adel(chain, deployer, akro, adel, vakro, rewardmodule, stakingpool, vakroSwap, setup_rewards, prepare_swap, regular_user3):

    assert adel.balanceOf(stakingpool.address) == 0

    adel.approve(stakingpool.address, ADEL_TO_SWAP, {'from': regular_user3})
    stakingpool.stake(ADEL_TO_SWAP, hexify("Some string"), {'from': regular_user3})
    
    assert adel.balanceOf(stakingpool.address) == ADEL_TO_SWAP
    assert stakingpool.totalStakedFor(regular_user3) == ADEL_TO_SWAP

    adel_balance_before = adel.balanceOf(regular_user3)
    akro_balance_before = akro.balanceOf(regular_user3)
    staking_adel_balance_before = adel.balanceOf(stakingpool.address)

    assert vakro.balanceOf(regular_user3) == 0
    assert adel.balanceOf(vakroSwap.address) == 0


    start = chain.time()
    chain.mine(1, start + 2*EPOCH_LENGTH)
    # Get rewards for vesting

    stakingpool.claimRewardsFromVesting({'from': deployer})

    assert adel.balanceOf(stakingpool.address) == ADEL_TO_SWAP + REWARDS_AMOUNT
    ###
    # Action performed
    ###
    vakro.setVestingCliff(0, {'from': deployer})
    vakro.setVestingStart(chain.time(), {'from': deployer})
    chain.mine(1)

    vakroSwap.swapFromRewardAdel({'from': regular_user3})
    
    adel_balance_after = adel.balanceOf(regular_user3)
    akro_balance_after = akro.balanceOf(regular_user3)
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
    assert vakro.balanceOf(vakroSwap.address) == 0

    akro.approve(vakro.address, REWARDS_AMOUNT * ADEL_AKRO_RATE, {'from': deployer})
    vakro.addAkroLiquidity(REWARDS_AMOUNT * ADEL_AKRO_RATE, {'from': deployer})

    assert akro.balanceOf(vakro.address) == REWARDS_AMOUNT * ADEL_AKRO_RATE

    # Stake was unchanged
    assert staking_adel_balance_before - staking_adel_balance_after == 0
    assert stakingpool.totalStakedFor(regular_user3) == ADEL_TO_SWAP

def test_batch_creation(chain, deployer, akro, adel, vakro, rewardmodule, stakingpool, vakroSwap, setup_rewards, prepare_swap, regular_user4):
    adel.transfer(regular_user4, 3 * ADEL_TO_SWAP, {'from': deployer})
    vakro.setVestingCliff(0, {'from': deployer})
    start = chain.time() + 50
    vakro.setVestingStart(start, {'from': deployer})
    chain.mine(1)

    akro.approve(vakro.address, 3 * ADEL_TO_SWAP * ADEL_AKRO_RATE, {'from': deployer})
    vakro.addAkroLiquidity(3 * ADEL_TO_SWAP * ADEL_AKRO_RATE, {'from': deployer})

    unclaimedBatch, totalBatches = vakro.batchesInfoOf(regular_user4)
    assert unclaimedBatch == 0
    assert totalBatches == 0

    locked, unlocked, unlockable = vakro.balanceInfoOf(regular_user4)
    assert locked == 0
    assert unlocked == 0
    assert unlockable == 0

    ###
    # First swap
    ###
    adel.approve(vakroSwap.address, ADEL_TO_SWAP, {'from': regular_user4})
    vakroSwap.swapFromAdel(ADEL_TO_SWAP, {'from': regular_user4})

    unclaimedBatch, totalBatches = vakro.batchesInfoOf(regular_user4)
    assert unclaimedBatch == 0
    assert totalBatches == 1

    batchAmount, _, _, batchClaimed, _ = vakro.batchInfo(regular_user4, 0)
    assert batchAmount == ADEL_TO_SWAP * ADEL_AKRO_RATE
    assert batchClaimed == 0

    locked, unlocked, unlockable = vakro.balanceInfoOf(regular_user4)
    assert locked == ADEL_TO_SWAP * ADEL_AKRO_RATE
    assert unlocked == 0
    assert unlockable == 0

    ###
    # Second swap
    ###
    adel.approve(vakroSwap.address, ADEL_TO_SWAP, {'from': regular_user4})
    vakroSwap.swapFromAdel(ADEL_TO_SWAP, {'from': regular_user4})

    unclaimedBatch, totalBatches = vakro.batchesInfoOf(regular_user4)
    assert unclaimedBatch == 0
    assert totalBatches == 1

    batchAmount, _, _, batchClaimed, _ = vakro.batchInfo(regular_user4, 0)
    assert batchAmount == 2 * ADEL_TO_SWAP * ADEL_AKRO_RATE
    assert batchClaimed == 0

    locked, unlocked, unlockable = vakro.balanceInfoOf(regular_user4)
    assert locked == 2 * ADEL_TO_SWAP * ADEL_AKRO_RATE
    assert unlocked == 0
    assert unlockable == 0

    # get vesting for the user
    chain.mine(1, start + EPOCH_LENGTH)

    vakro.unlockAndRedeemAll({'from' : regular_user4})

    unclaimedBatch, totalBatches = vakro.batchesInfoOf(regular_user4)
    assert unclaimedBatch == 1 #Has updated
    assert totalBatches == 1

    batchAmount, _, _, batchClaimed, _ = vakro.batchInfo(regular_user4, 0)
    assert batchAmount == 2 * ADEL_TO_SWAP * ADEL_AKRO_RATE
    assert batchClaimed == 2 * ADEL_TO_SWAP * ADEL_AKRO_RATE # has been claimed

    locked, unlocked, unlockable = vakro.balanceInfoOf(regular_user4)
    assert locked == 0
    assert unlocked == 0
    assert unlockable == 0

    ###
    # Thrid swap (to create a new batch)
    ###
    adel.approve(vakroSwap.address, ADEL_TO_SWAP, {'from': regular_user4})
    vakroSwap.swapFromAdel(ADEL_TO_SWAP, {'from': regular_user4})

    unclaimedBatch, totalBatches = vakro.batchesInfoOf(regular_user4)
    assert unclaimedBatch == 1
    assert totalBatches == 2

    batchAmount, _, _, batchClaimed, _ = vakro.batchInfo(regular_user4, 1)
    assert batchAmount == ADEL_TO_SWAP * ADEL_AKRO_RATE
    assert batchClaimed == 0

    locked, unlocked, unlockable = vakro.balanceInfoOf(regular_user4)
    assert locked == ADEL_TO_SWAP * ADEL_AKRO_RATE
