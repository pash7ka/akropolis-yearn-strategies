import pytest
import brownie

from constantsV2 import *

def hexify(s):
    return s.encode("utf-8").hex()

def test_swap_vakro(deployer, stakingpool, adel, regular_user):
    assert adel.balanceOf(stakingpool.address) == 0

    adel.approve(stakingpool.address, 100, {'from': regular_user})
    stakingpool.stake(100, hexify("Some string"), {'from': regular_user})
    
    assert adel.balanceOf(stakingpool.address) == 100
