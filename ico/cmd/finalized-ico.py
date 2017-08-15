import populus
from populus.utils.cli import request_account_unlock
from populus.utils.accounts import is_account_locked
from eth_utils import to_wei, from_wei
from ico.utils import check_succesful_tx
import yaml

config = {}
with open("crowdsales/example.deployment-report.yml", 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

p = populus.Project()
deploy_address = "0x2b317defb1d07e737ef9dacd88bf1daeb5a54da3"  # Our controller account on mainnet
crowdsale_address = config['contracts']['crowdsale'][3][1]
team_multisig = config['contracts']['team_multisig'][3][1]

with p.get_chain("mynet") as chain:
    web3 = chain.web3

    Crowdsale = chain.contract_factories.Crowdsale
    crowdsale = Crowdsale(address=crowdsale_address)

    BonusFinalizeAgent = chain.contract_factories.BonusFinalizeAgent
    finalize_agent = BonusFinalizeAgent(address=crowdsale.call().finalizeAgent())
    assert finalize_agent.call().teamMultisig() == team_multisig
    assert finalize_agent.call().bonusBasePoints() > 1000

    # Safety check that Crodsale is using our pricing strategy
    txid = crowdsale.transact({"from": deploy_address}).finalize()
    print("Finalize txid is", txid)
    check_succesful_tx(web3, txid)
    print(crowdsale.call().getState())
