import pytest
import brownie

def test_swap_adel(owner, akro, adel, vakro, vakroSwap, prepare_swap):
    assert adel.balanceOf(vakro.address) == 0
    assert adel.balanceOf(vakroSwap.address) == 0