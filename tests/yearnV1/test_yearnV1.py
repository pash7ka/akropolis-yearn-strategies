import pytest

@pytest.fixture(scope="module")
def register_vault(deployer, token, vault, strategy, controller, registry, vaultSavings):
    controller.setVault(token.address, vault.address, {'from': deployer})
    controller.setStrategy(token.address, strategy.address, {'from': deployer})

    assert registry.getVaultsLength() == 0
    registry.addVault.transact(vault.address, {'from': deployer})
    assert registry.getVaultsLength() == 1
    assert registry.getVault(0) == vault.address
    vaults_arr = registry.getVaults()
    assert len(vaults_arr) == 1
    assert vaults_arr[0] == vault.address

    vaultSavings.registerVault.transact(vault.address, {'from': deployer})
    assert vaultSavings.isVaultRegistered(vault.address) == True
    assert vaultSavings.isVaultActive(vault.address) == True
    assert vaultSavings.isBaseTokenForVault(vault.address, token.address) == True
    supported_vaults = vaultSavings.supportedVaults()
    assert len(supported_vaults) == 1
    assert supported_vaults[0] == vault.address
    active_vaults = vaultSavings.activeVaults()
    assert len(active_vaults) == 1
    assert active_vaults[0] == vault.address

def test_deactivate_vault(register_vault, vaultSavings, vault, deployer):
    vaultSavings.deactivateVault.transact(vault.address, {'from': deployer})

    assert vaultSavings.isVaultActive(vault.address) == False
    active_vaults = vaultSavings.activeVaults()
    assert len(active_vaults) == 0

    vaultSavings.activateVault.transact(vault.address, {'from': deployer})

    assert vaultSavings.isVaultActive(vault.address) == True
    active_vaults = vaultSavings.activeVaults()
    assert len(active_vaults) == 1
    assert active_vaults[0] == vault.address

def test_deposit(register_vault):
    pass

def test_withdraw(register_vault):
    pass

def test_registry(register_vault):
    pass


