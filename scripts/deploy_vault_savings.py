import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

from brownie import VaultSavings, yTestVault, TestERC20, YTestRegistry, YTestController, YTestStrategy, accounts, network, web3

def main():
    #load_dotenv(dotenv_path=Path('..')/".env", override=True)
    load_dotenv(find_dotenv())

    print(f"You are using the '{network.show_active()}' network")
    if (network.show_active() == 'development'):
        deployer = accounts[0]
    else:
        deployer = accounts.add(os.getenv("DEPLOYER_PRIVATE_KEY"))
    print(f"You are using: 'deployer' [{deployer.address}]")

    vaultSavings = deployer.deploy(VaultSavings)
    print(f"VaultSavings deployed at {vaultSavings.address}")

    registry = deployer.deploy(YTestRegistry, deployer.address)
    print(f"Registry deployed at {registry.address}")

    token = deployer.deploy(TestERC20, "Y Test Token", "yTST", 18)
    token.mint(2*10**6 * 10**18, {"from": deployer})
    print(f"Token deployed at {token.address}")
    print(f"Tokens balance at {deployer.address} == {token.balanceOf(deployer.address)}")

    controller = deployer.deploy(YTestController)
    print(f"Controller deployed at {controller.address}")

    yVault = deployer.deploy(yTestVault, token.address, controller.address)
    print(f"Vault deployed at {yVault.address}")

    strategy = deployer.deploy(YTestStrategy, token.address)
    print(f"Strategy deployed at {strategy.address}")
    
    controller.setVault(token.address, yVault.address, {'from': deployer})
    controller.setStrategy(token.address, strategy.address, {'from': deployer})

    registry.addVault.transact(yVault.address, {'from': deployer})
    vaultSavings.registerVault.transact(yVault.address, {'from': deployer})
    vaultSavings.activateVault.transact(yVault.address, {'from': deployer})
    print("Vault registered")


