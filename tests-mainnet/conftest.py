import pytest
from brownie import accounts
import sys
import os

from utils.deploy_helpers import deploy_proxy, deploy_admin

from dotenv import load_dotenv, find_dotenv

ADEL_TO_SWAP = 100
AKRO_ON_SWAP = 10000
ADEL_AKRO_RATE = 15
EPOCH_LENGTH = 100
REWARDS_AMOUNT = 150

@pytest.fixture(scope="module")
def env_settings():
    yield load_dotenv(find_dotenv())

@pytest.fixture(scope="module")
def owner(env_settings, accounts):
    yield accounts.at(os.getenv("MAINNET_OWNER"), force=True)

@pytest.fixture(scope="module")
def regular_user(accounts):
    yield accounts[1]

@pytest.fixture(scope="module")
def regular_user2(accounts):
    yield accounts[2]

@pytest.fixture(scope="module")
def regular_user3(accounts):
    yield accounts[3]

@pytest.fixture(scope="module")
def regular_user4(accounts):
    yield accounts[4]


@pytest.fixture(scope="module")
def akro(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("MAINNET_AKRO"))


@pytest.fixture(scope="module")
def adel(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("MAINNET_ADEL"))

@pytest.fixture(scope="module")
def vakro(env_settings, owner, akro, VestedAkro):
    proxy_admin = os.getenv("MAINNET_PROXY_ADMIN")

    vakroImplFromProxy, vakroProxy, vakroImpl = deploy_proxy(owner, proxy_admin, VestedAkro, akro.address, EPOCH_LENGTH)

    assert vakroProxy.admin.call({"from":proxy_admin.address}) == proxy_admin.address
    assert vakroProxy.implementation.call({"from":proxy_admin.address}) == vakroImpl.address

    yield vakroImplFromProxy

@pytest.fixture(scope="module")
def adelstakingpool(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("MAINNET_ADEL_STAKING"), as_proxy_for=os.getenv("MAINNET_ADEL_STAKING"))

@pytest.fixture(scope="module")
def akrostakingpool(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("MAINNET_AKRO_STAKING"), as_proxy_for=os.getenv("MAINNET_AKRO_STAKING"))


@pytest.fixture(scope="module")
def vakroSwap(env_settings, owner, adel, akro, vakro, AdelVAkroSwap):
    proxy_admin = os.getenv("MAINNET_PROXY_ADMIN")
    vakroSwapImplFromProxy, vakroSwapProxy, vakroSwapImpl = deploy_proxy(owner, proxy_admin, AdelVAkroSwap,
                                                                         akro.address, adel.address, vakro.address)

    assert vakroSwapProxy.admin.call({"from":proxy_admin.address}) == proxy_admin.address
    assert vakroSwapProxy.implementation.call({"from":proxy_admin.address}) == vakroSwapImpl.address

    yield vakroSwapImplFromProxy


@pytest.fixture(scope="module")
def prepare_swap(owner, adel, akro, vakro, stakingpooladel, stakingpoolakro, vakroSwap):
    vakro.addMinter(vakroSwap.address, {'from': owner})
    vakro.addSender(vakroSwap.address, {'from': owner})

    vakroSwap.setSwapRate(ADEL_AKRO_RATE, 1, {'from': owner})
    vakroSwap.setStakingPool(stakingpooladel.address, {'from': owner})
    vakroSwap.setRewardStakingPool(stakingpoolakro.address, stakingpooladel.address, {'from': owner})


@pytest.fixture(scope="module")
def prepare_stakings(owner, stakingpooladel, stakingpoolakro, vakroSwap):
    # Update stakings

    # Set swap address
    stakingpoolakro.setSwapContract(vakroSwap.address, {'from': owner})
    stakingpooladel.setSwapContract(vakroSwap.address, {'from': owner})