import populus
from populus.utils.accounts import is_account_locked
from populus.utils.cli import request_account_unlock
from eth_utils import from_wei
from ico.utils import check_succesful_tx

from eth_utils import to_wei
import yaml

# Which network we deployed our contract
chain_name = "mynet"

# read address from crowdsales/example.deployment-report.yml
config = {}
with open("crowdsales/example.deployment-report.yml", 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# Owner account on geth
#owner_address = "0x2b317defb1d07e737ef9dacd88bf1daeb5a54da3"

participant_address = "0x19bb685e8bc2fa3cf2afb09743355be24aac7edb"
#participant_address = "0x2b317defb1d07e737ef9dacd88bf1daeb5a54da3"

# Crowdsale address
# token_address = "0x57b27d7d3b752cb5a3af47c0d0451b97884008b9"
# crowdsale_address = "0xbe1b38d91c01a47e56c685bf4d3517502cacceba"
# price_address = "0x85b79209862ef8ebca75719cb3f9e00e087d4299"
# finalize_address = "0xbe1481d84c16e13103a41eb9b460cfdb8b008587"
token_address = config['contracts']['token'][3][1];
crowdsale_address = config['contracts']['crowdsale'][3][1];
price_address = config['contracts']['pricing_strategy'][3][1];
finalize_address = config['contracts']['finalize_agent'][3][1];

project = populus.Project()

with project.get_chain(chain_name) as chain:

    web3 = chain.web3
    print("Web3 provider is", web3.currentProvider)
    print("Participant address is", participant_address)
    print("Participant balance is", from_wei(web3.eth.getBalance(participant_address), "ether"), "ETH")

    # Goes through geth account unlock process if needed
    if is_account_locked(web3, participant_address):
        request_account_unlock(chain, participant_address, None)

    print("contract addr:", chain.provider.get_all_contract_data())
    transaction = {"from": participant_address}

    Contract = getattr(chain.contract_factories, "MintedTokenCappedCrowdsale")
    crowdsale = Contract(address=crowdsale_address)

    Contract = getattr(chain.contract_factories, "FlatPricing")
    pricingStrategy = Contract(address=price_address)

    Contract = getattr(chain.contract_factories, "BonusFinalizeAgent")
    finalizeAgent = Contract(address=finalize_address)

    Contract = getattr(chain.contract_factories, "CrowdsaleToken")
    token = Contract(address=token_address)

    print("crowdsale owner is", crowdsale.call().owner())
    print("crowdsale tokensSold is ", crowdsale.call().tokensSold())
    print("crowdsale weiRaised is ", crowdsale.call().weiRaised())
    print("crowdsale investorCount is ", crowdsale.call().investorCount())
    print("crowdsale starts at ", crowdsale.call().startsAt())
    print("crowdsale ends at ", crowdsale.call().endsAt())
    print("crowdsale state ", crowdsale.call().getState())
    print("crowdsale pricing ", crowdsale.call().pricingStrategy())
    print("crowdsale pricing ", pricingStrategy.call().isSane(crowdsale.address))
    print("crowdsale finalize ", crowdsale.call().finalizeAgent())
    print("crowdsale finalize ", finalizeAgent.call().isSane())
    print("crowdsale isfinalize ", finalizeAgent.call().isFinalizeAgent())
    print("token mint", token.call().mintAgents(finalizeAgent.address))
    print("token release", token.call().releaseAgent())

    #print("add to early participate..")
    #txid = crowdsale.call().setEarlyParicipantWhitelist(participant_address, True)
    #print("TXID", txid)
    #check_succesful_tx(web3, txid)

    #txid = crowdsale.estimateGas({"from": participant_address, "value": to_wei("10", "ether")}, "gasPrice": "0x095799F9F8BFACE").invest(participant_address)
    txid = crowdsale.transact({"from": participant_address, "value": to_wei("50", "ether"), "gasPrice": "0x3E8"}).invest(participant_address)
    #txid = crowdsale.transact({"from": participant_address, "value": '0x016345785d8a0000', "gas": '0x1388', "gasPrice": '0x4563918244F40000'}).invest(participant_address)
    print("TXID", txid)
    check_succesful_tx(web3, txid)

