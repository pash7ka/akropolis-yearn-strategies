import pytest
import brownie
from web3 import Web3

ADEL_TO_SWAP = 100
AKRO_ON_SWAP = 10000
ADEL_AKRO_RATE = 15
EPOCH_LENGTH = 100
REWARDS_AMOUNT = 150
ADEL_MAX_ALLOWED = 1000
NULL_ADDRESS = '0x0000000000000000000000000000000000000000'
AVAILABLE_USER1 = 2000
AVAILABLE_USER2 = 4000

@pytest.fixture(scope="module")
def prepare_swap(deployer, adel, akro, vakro, stakingpool, vakroSwap):
    vakro.addMinter(vakroSwap.address, {'from': deployer})
    vakro.addSender(vakroSwap.address, {'from': deployer})

    adel.addMinter(vakroSwap.address, {'from': deployer})

    stakingpool.setSwapContract(vakroSwap.address, {'from': deployer})

    vakroSwap.setSwapRate(ADEL_AKRO_RATE, 1, {'from': deployer})
    vakroSwap.setStakingPool(stakingpool, {'from': deployer})
    vakroSwap.setRewardStakingPool(NULL_ADDRESS, stakingpool, {'from': deployer})

def encode(s):
    return s.encode("utf-8")

def hexify(s):
    return encode(s).hex()

def to_keccak(types, str):
    return Web3.solidityKeccak(types, str)

def prepare_root(regular_user, regular_user2):
    h1 = to_keccak( ['address', 'uint256'], [regular_user, AVAILABLE_USER1] )
    h2 = to_keccak( ['address', 'uint256'], [regular_user, AVAILABLE_USER2] )
    if int(h1.hex(), 16) <= int(h2.hex(), 16):
        root = to_keccak(['bytes32', 'bytes32'], [h1, h2] )
    else:
        root = to_keccak(['bytes32', 'bytes32'], [h2, h1] )
    return (root, h1, h2)



def test_swap_adel(chain, deployer, akro, adel, vakro, vakroSwap, prepare_swap, regular_user, regular_user2):
    root, h1, h2 = prepare_root(regular_user.address, regular_user2.address)


    # Set root
    vakroSwap.setMerkleRoots([root], {'from': deployer})
    
    
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

    assert vakroSwap.adelSwapped(regular_user) == 0
    adel.approve(vakroSwap.address, ADEL_TO_SWAP, {'from': regular_user})
    vakroSwap.swapFromAdel(ADEL_TO_SWAP, 0, AVAILABLE_USER1, [h1, h2], {'from': regular_user})
    assert vakroSwap.adelSwapped(regular_user) == ADEL_TO_SWAP

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

    # Swap has collected ADEL, minted vAkro for the user and sent AKRO to vAkro
    assert adel.balanceOf(vakroSwap.address) == ADEL_TO_SWAP
    assert vakro.balanceOf(vakroSwap.address) == 0
