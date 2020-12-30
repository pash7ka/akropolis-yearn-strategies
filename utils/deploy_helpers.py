import brownie
from brownie import Contract
from brownie.project import DelphiYearnTestsProject

def deploy_proxy(deployer, contract_admin, ImplContract, *args):
    #Deploy implementation first
    contract_impl = deployer.deploy(ImplContract)
    
    #Deploy proxy next
    initializer_data = contract_impl.initialize.encode_input(*args)
    proxy_contract = deployer.deploy(DelphiYearnTestsProject.TransparentUpgradeableProxy, contract_impl.address, contract_admin.address, initializer_data)

    #Route all calls to go through the proxy contract
    contract_impl_from_proxy = Contract.from_abi(ImplContract._name, proxy_contract.address, ImplContract.abi)

    return contract_impl_from_proxy, proxy_contract, contract_impl

def deploy_admin(deployer):
    return deployer.deploy(DelphiYearnTestsProject.ProxyAdmin)