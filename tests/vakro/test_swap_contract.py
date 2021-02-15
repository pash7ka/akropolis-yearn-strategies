import pytest
import brownie


def hexify(s):
    return s.encode("utf-8").hex()

@pytest.fixture(scope="module")
def prepare_swap(deployer, stakingpool, akro, adel, vakro, vakroSwap):
    akro.approve(vakroSwap.address, 1000, {'from': deployer})
    vakroSwap.addSwapLiquidity(1000, {'from': deployer})

    vakro.addMinter(vakroSwap.address, {'from': deployer})

    adel.addMinter(vakroSwap.address, {'from': deployer})

    stakingpool.setSwapContract(vakroSwap.address, {'from': deployer})



def test_swap_adel(deployer, prepare_swap, vakroSwap, akro, adel, vakro, regular_user):
    pass

def test_swap_staked_adel(deployer, prepare_swap, stakingpool, vakroSwap, akro, adel, vakro, regular_user):
    assert adel.balanceOf(stakingpool.address) == 0

    adel.approve(stakingpool.address, 100, {'from': regular_user})
    stakingpool.stake(100, hexify("Some string"), {'from': regular_user})
    
    assert adel.balanceOf(stakingpool.address) == 100

def test_swap_rewards_adel(deployer, prepare_swap, stakingpool, vakroSwap, akro, adel, vakro, regular_user):
    pass