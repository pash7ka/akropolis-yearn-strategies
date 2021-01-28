import pytest
import brownie
from brownie.test import given, strategy
from hypothesis import settings



#PAUSE/UNPAUSE

DEPOSIT_VALUE = 2000000

@given(
    user=strategy('address', length=10)
)

@settings(max_examples=500)

def test_pause_vault_reverts(vaultSavings, deployer, user):

    if (user == deployer):
        vaultSavings.pause({'from': user});
    else:
        with brownie.reverts():
            print(user)
            vaultSavings.pause({'from': user});



@given(
    user=strategy('address', length=10)
)

@settings(max_examples=500)
def test_deposit_unpause_vault_reverts(token, vault, vaultSavings, deployer, user):
    vaultSavings.pause({'from': deployer});
    assert vaultSavings.paused() == True

    token.transfer(user, DEPOSIT_VALUE,  {"from": deployer})

    with brownie.reverts():
        user_balance_before = token.balanceOf(user)
        token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})
        vaultSavings.deposit['address,uint'](vault.address, DEPOSIT_VALUE, {'from': user})
        user_balance_after = token.balanceOf(regular_user)



