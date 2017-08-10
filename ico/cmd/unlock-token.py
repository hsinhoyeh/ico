import populus
from populus.utils.accounts import is_account_locked
from populus.utils.cli import request_account_unlock
from eth_utils import from_wei
from ico.utils import check_succesful_tx

# Which network we deployed our contract
chain_name = "mynet"

# Owner account on geth
owner_address = "0x2b317defb1d07e737ef9dacd88bf1daeb5a54da3"

# Where did we deploy our token
contract_address = "0x0aa721cc960c65b341f5663af620819148034ae1"

project = populus.Project()

with project.get_chain(chain_name) as chain:

    web3 = chain.web3
    print("Web3 provider is", web3.currentProvider)
    print("Owner address is", owner_address)
    print("Owner balance is", from_wei(web3.eth.getBalance(owner_address), "ether"), "ETH")

    # Goes through geth account unlock process if needed
    if is_account_locked(web3, owner_address):
        request_account_unlock(chain, owner_address, None)

    print("contract addr:", chain.provider.get_all_contract_data())
    transaction = {"from": owner_address}
    #Contract = chain.get_contract_factory("CrowdsaleToken")
    Contract = getattr(chain.contract_factories, "CrowdsaleToken")

    contract = Contract(address=contract_address)
    print("Attempting to release the token transfer")
    txid = contract.transact(transaction).releaseTokenTransfer()
    check_succesful_tx(web3, txid)
    print("Token released")

