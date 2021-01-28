import pytest
import brownie
from brownie.test import given, strategy
from hypothesis import settings



#PAUSE/UNPAUSE

DEPOSIT_VALUE = 2000000

@given(
    user=strategy('address', length=10)
)

@settings(max_examples=50)
def test_pause_vault_reverts(vaultSavings, deployer, user):

    if (user == deployer):
        vaultSavings.pause({'from': user});
    else:
        with brownie.reverts():
            vaultSavings.pause({'from': user});



@given(
    user=strategy('address', length=10)
)

@settings(max_examples=50)
def test_deposit_unpause_vault_reverts(token, vault, vaultSavings, deployer, user):
    vaultSavings.pause({'from': deployer});
    assert vaultSavings.paused() == True

    token.transfer(user, DEPOSIT_VALUE,  {"from": deployer})

    user_balance_before = token.balanceOf(user)
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})

    with brownie.reverts():
        vaultSavings.deposit['address,uint'](vault.address, DEPOSIT_VALUE, {'from': user})

    vaultSavings.unpause({'from': deployer});

@given(
    user=strategy('address', length=10)
)

@settings(max_examples=50)
def test_deposit_array_unpause_vault_reverts(token, vault, vaultSavings, deployer, user):
    vaultSavings.pause({'from': deployer});
    assert vaultSavings.paused() == True

    token.transfer(user, DEPOSIT_VALUE,  {"from": deployer})

    user_balance_before = token.balanceOf(user)
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})

    with brownie.reverts():
        vaultSavings.deposit['address[],uint[]']([vault.address], [DEPOSIT_VALUE], {'from': user})

    vaultSavings.unpause({'from': deployer});



@given(
    user=strategy('address', length=10)
)

@settings(max_examples=50)
def test_deposit_array(register_vault, token, vault, vaultSavings, user, deployer):
    
    assert vaultSavings.paused() == False

    token.transfer(user, DEPOSIT_VALUE,  {"from": deployer})
    # Initial deposit
    user_balance_before = token.balanceOf(user)
    vault_token_balance_before = token.balanceOf(vault.address)
    vault_user_balance_before = vault.balanceOf(user)
    
    vault_totalSupply = vault.totalSupply()

    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})
    vaultSavings.deposit['address[],uint[]']([vault.address], [DEPOSIT_VALUE], {'from': user})

    user_balance_after = token.balanceOf(user)
    vault_token_balance_after = token.balanceOf(vault.address)
    vault_user_balance_after = vault.balanceOf(user)

    # User sends tokens and receives LP-tokens
    assert user_balance_before - user_balance_after == DEPOSIT_VALUE
    assert vault_token_balance_after - vault_token_balance_before == DEPOSIT_VALUE

    # First deposit - exect amount
    assert vault_user_balance_after - vault_user_balance_before == DEPOSIT_VALUE
    assert vault.totalSupply() - vault_totalSupply == DEPOSIT_VALUE

    # Nothing left on vaultSavings
    assert vault.balanceOf(vaultSavings.address) == 0
    assert token.balanceOf(vaultSavings.address) == 0

    # For test vault - custom logic
    assert vault.available() == (vault_totalSupply+DEPOSIT_VALUE) * vault.min() // vault.max()
    assert vault.balance() == (vault_totalSupply+DEPOSIT_VALUE)



@given(
    user=strategy('address', length=10)
)
@settings(max_examples=50)
def test_deposit_array(register_vault, token, vault, vaultSavings, user, deployer):
    
    assert vaultSavings.paused() == False

    token.transfer(user, DEPOSIT_VALUE,  {"from": deployer})
    # Initial deposit
    user_balance_before = token.balanceOf(user)
    vault_token_balance_before = token.balanceOf(vault.address)
    vault_user_balance_before = vault.balanceOf(user)
    
    vault_totalSupply = vault.totalSupply()
    
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})
    vaultSavings.deposit['address,uint'](vault.address, DEPOSIT_VALUE, {'from': user})

    user_balance_after = token.balanceOf(user)
    vault_token_balance_after = token.balanceOf(vault.address)
    vault_user_balance_after = vault.balanceOf(user)

    # User sends tokens and receives LP-tokens
    assert user_balance_before - user_balance_after == DEPOSIT_VALUE
    assert vault_token_balance_after - vault_token_balance_before == DEPOSIT_VALUE

    # First deposit - exect amount
    assert vault_user_balance_after - vault_user_balance_before == DEPOSIT_VALUE
    assert vault.totalSupply() - vault_totalSupply == DEPOSIT_VALUE

    # Nothing left on vaultSavings
    assert vault.balanceOf(vaultSavings.address) == 0
    assert token.balanceOf(vaultSavings.address) == 0

    # For test vault - custom logic
    assert vault.available() == (vault_totalSupply+DEPOSIT_VALUE) * vault.min() // vault.max()
    assert vault.balance() == (vault_totalSupply+DEPOSIT_VALUE)


@given(
    user=strategy('address', length=10),
    test_vault = strategy('address', length=10),
)

@settings(max_examples=50)

def test_deposit_with_failed_vault(register_vault, token, test_vault, vaultSavings, user, deployer):
    assert vaultSavings.paused() == False

    token.transfer(user, DEPOSIT_VALUE,  {"from": deployer})
    
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})

    with brownie.reverts():
        vaultSavings.deposit['address,uint'](test_vault, DEPOSIT_VALUE, {'from': user})

@given(
    user=strategy('address', length=10),
    test_vault = strategy('address', length=10),
)

@settings(max_examples=50)
def test_deposit_array_with_failed_vault(register_vault, token, test_vault, vaultSavings, user, deployer):
    assert vaultSavings.paused() == False

    token.transfer(user, DEPOSIT_VALUE,  {"from": deployer})
    
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})

    with brownie.reverts():
        vaultSavings.deposit['address[],uint[]']([test_vault], [DEPOSIT_VALUE], {'from': user})
        