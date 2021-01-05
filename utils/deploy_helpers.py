import brownie
from brownie import Contract, project

def deploy_proxy(deployer, contract_admin, ImplContract, *args):
    """
    @dev
        Deploys upgradable contract with proxy from oz-contracts package
    @param deployer Brownie account used to deploy a contract.
    @param contract_admin Admin contract deployed with deploy_admin().
    @param ImplContract Brownie Contract container for the implementation.
    @param args Initializer arguments.
    @return Contract container for the proxy wrapped into the implementation interface
            Contract container for the proxy
            Contract container for the implementation
    """
    cur_project = project.get_loaded_projects()[0]

    #Deploy implementation first
    contract_impl = deployer.deploy(ImplContract)

    #Deploy proxy next
    initializer_data = contract_impl.initialize.encode_input(*args)
    proxy_contract = deployer.deploy(cur_project.TransparentUpgradeableProxy, contract_impl.address, contract_admin.address, initializer_data)

    #Route all calls to go through the proxy contract
    contract_impl_from_proxy = Contract.from_abi(ImplContract._name, proxy_contract.address, ImplContract.abi)

    return contract_impl_from_proxy, proxy_contract, contract_impl

def deploy_admin(deployer):
    """
    @dev
        Deploys admin contract from oz-contracts package.
        Should be used once
    @param deployer Brownie account used to deploy a contract.
    @return Contract container for the admin contract
    """
    cur_project = project.get_loaded_projects()[0]
    return deployer.deploy(cur_project.ProxyAdmin)