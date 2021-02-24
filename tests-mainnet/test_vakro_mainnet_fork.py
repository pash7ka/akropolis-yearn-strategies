import pytest
import brownie

def test_swap_adel(owner, akro, adel, vakro, vakroSwap, adelstakingpool, akrostakingpool, prepare_swap, prepare_stakings):

    assert adel.balanceOf(vakro.address) == 0
    assert adel.balanceOf(vakroSwap.address) == 0
    assert adel.balanceOf(adelstakingpool.address) != 0