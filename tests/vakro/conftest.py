import pytest
from brownie import accounts
import sys

from utils.deploy_helpers import deploy_proxy, deploy_admin

@pytest.fixture(scope="module")
def deployer():
    yield accounts[0]

@pytest.fixture(scope="module")
def regular_user(accounts):
    yield accounts[1]

@pytest.fixture(scope="module")
def regular_user2(accounts):
    yield accounts[2]

@pytest.fixture(scope="module")
def pool(accounts):
    yield accounts[3]

@pytest.fixture(scope="module")
def proxy_admin(deployer):
    proxy_admin = deploy_admin(deployer)
    yield proxy_admin

def prepare_token(deployer, regular_user, regular_user2, TestERC20, name, symbol):
    token = deployer.deploy(TestERC20, name, symbol, 18)
    token.mint(1500000000, {"from": deployer})
    assert token.balanceOf(deployer) == 1500000000
    token.transfer(regular_user, 1500000000 // 4, {"from": deployer})
    token.transfer(regular_user2, 1500000000 // 4, {"from": deployer})

    return token

def prepare_adel(deployer, regular_user, regular_user2, proxy_admin, TestADEL):
    adelImplFromProxy, adelProxy, adelImpl = deploy_proxy(deployer, proxy_admin, TestADEL)

    assert adelProxy.admin.call({"from":proxy_admin.address}) == proxy_admin.address
    assert adelProxy.implementation.call({"from":proxy_admin.address}) == adelImpl.address

    adelImplFromProxy.mint(1500000000, {"from": deployer})
    assert adelImplFromProxy.balanceOf(deployer) == 1500000000
    adelImplFromProxy.transfer(regular_user, 1500000000 // 4, {"from": deployer})
    adelImplFromProxy.transfer(regular_user2, 1500000000 // 4, {"from": deployer})

    return adelImplFromProxy

@pytest.fixture(scope="module")
def akro(deployer, regular_user, regular_user2, TestERC20):
    akro = prepare_token(deployer, regular_user, regular_user2, TestERC20, "AKRO", "AKRO")
    yield akro


@pytest.fixture(scope="module")
def adel(deployer, regular_user, regular_user2, TestADEL, proxy_admin):
    adel = prepare_adel(deployer, regular_user, regular_user2, proxy_admin, TestADEL)
    yield adel

@pytest.fixture(scope="module")
def vakro(deployer, proxy_admin, akro, VestedAkro):
    vakroImplFromProxy, vakroProxy, vakroImpl = deploy_proxy(deployer, proxy_admin, VestedAkro, akro.address, 100)

    assert vakroProxy.admin.call({"from":proxy_admin.address}) == proxy_admin.address
    assert vakroProxy.implementation.call({"from":proxy_admin.address}) == vakroImpl.address

    yield vakroImplFromProxy

@pytest.fixture(scope="module")
def stakingpool(deployer, proxy_admin, pool, adel, TestStakingPool):
    stakingpoolImplFromProxy, stakingpoolProxy, stakingpoolImpl = deploy_proxy(deployer, proxy_admin, TestStakingPool, pool, adel.address, 100)

    assert stakingpoolProxy.admin.call({"from":proxy_admin.address}) == proxy_admin.address
    assert stakingpoolProxy.implementation.call({"from":proxy_admin.address}) == stakingpoolImpl.address

    assert stakingpoolImplFromProxy.owner() == deployer.address

    yield stakingpoolImplFromProxy

@pytest.fixture(scope="module")
def vakroSwap(deployer, proxy_admin, akro, adel, vakro, stakingpool, AdelVAkroSwap):
    vakroSwapImplFromProxy, vakroSwapProxy, vakroSwapImpl = deploy_proxy(deployer, proxy_admin, AdelVAkroSwap,
                                                                         akro.address, adel.address, vakro.address, stakingpool.address)

    assert vakroSwapProxy.admin.call({"from":proxy_admin.address}) == proxy_admin.address
    assert vakroSwapProxy.implementation.call({"from":proxy_admin.address}) == vakroSwapImpl.address

    yield vakroSwapImplFromProxy