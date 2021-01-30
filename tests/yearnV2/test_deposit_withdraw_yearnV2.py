import pytest
import brownie

from constantsV2 import *

def test_successful_deposit(register_vault, token, vault, vaultSavings, regular_user, deployer):
    # Initial deposit
    user_balance_before = token.balanceOf(regular_user)
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': regular_user})
    vaultSavings.deposit['address,uint'](vault.address, DEPOSIT_VALUE, {'from': regular_user})

    user_balance_after = token.balanceOf(regular_user)

    # User sends tokens and receives LP-tokens
    assert user_balance_before - user_balance_after == DEPOSIT_VALUE
    assert token.balanceOf(vault.address) == DEPOSIT_VALUE

    # First deposit - exect amount
    assert vault.balanceOf(regular_user) == DEPOSIT_VALUE
    assert vault.totalSupply() == DEPOSIT_VALUE

    # Nothing left on vaultSavings
    assert vault.balanceOf(vaultSavings.address) == 0
    assert token.balanceOf(vaultSavings.address) == 0

    # For test vault - custom logic
    assert token.balanceOf(vault.address) == DEPOSIT_VALUE
    assert vault.totalAssets() == DEPOSIT_VALUE


def test_successful_withdraw(register_vault, token, vault, vaultSavings, regular_user, deployer):
    user_balance_before = token.balanceOf(regular_user)

    # Initial deposits
    # Regular user already has deposit from the dirst test
    assert vault.balanceOf(regular_user) == DEPOSIT_VALUE

    # Withdraw
    vault.approve(vaultSavings.address, vault.balanceOf(regular_user), {'from': regular_user})

    # Withdraw the part
    vaultSavings.withdraw['address,uint'].transact(vault.address, WITHDRAW_VALUE, {'from': regular_user})
    
    assert vault.balanceOf(regular_user) == DEPOSIT_VALUE - WITHDRAW_VALUE
    assert vault.totalAssets() == DEPOSIT_VALUE - WITHDRAW_VALUE

    # Withdraw all
    vaultSavings.withdraw['address,uint'].transact(vault.address, vault.balanceOf(regular_user), {'from': regular_user})

    user_balance_after = token.balanceOf(regular_user)

    assert vault.balanceOf(regular_user) == 0
    assert vault.totalAssets() == 0
    # Regular user returns his deposit from the first test
    assert user_balance_after - user_balance_before  == DEPOSIT_VALUE


def test_deposit_zero(register_vault, token, vault, vaultSavings, regular_user):
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': regular_user})
    with brownie.reverts(revert_pattern = "Depositing zero amount"):
        vaultSavings.deposit['address,uint'](vault.address, 0, {'from': regular_user})

def test_withdraw_zero(register_vault, vault, vaultSavings, regular_user):
    vault.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': regular_user})
    with brownie.reverts(revert_pattern = "Withdrawing zero amount"):
        vaultSavings.withdraw['address,uint'](vault.address, 0, {'from': regular_user})

def test_deposit_yield_withdraw():
    pass

def test_withdraw_all_with_yield():
    pass

def test_several_deposits():
    pass

def test_several_withdraws():
    pass

def test_deposit_yield_withdraw_two_strategies():
    pass

def test_deposit_withdraw_several_vaults():
    pass

def test_deposit_withdraw_several_vaults_different_tokens():
    pass