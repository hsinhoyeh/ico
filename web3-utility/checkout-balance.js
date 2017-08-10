const fs = require('fs');
const solc = require('solc');
const Web3 = require('web3');
const web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));


const readFile = function(filePath) {
  return fs.readFileSync(filePath, "utf8")
}

const inputs = {
  'CrowdsaleToken.sol': readFile('./contracts/CrowdsaleToken.sol'),
  'StandardToken.sol': readFile('./contracts/StandardToken.sol'),
  'UpgradeableToken.sol': readFile('./contracts/UpgradeableToken.sol'),
  'ReleasableToken.sol': readFile('./contracts/ReleasableToken.sol'),
  'MintableToken.sol': readFile('./contracts/MintableToken.sol'),
  'UpgradeAgent.sol': readFile('./contracts/UpgradeAgent.sol'),
  'SafeMathLib.sol': readFile('./contracts/SafeMathLib.sol'),
  'zeppelin/contracts/token/ERC20.sol': readFile('./zeppelin/contracts/token/ERC20.sol'),
  'zeppelin/contracts/ownership/Ownable.sol': readFile('./zeppelin/contracts/ownership/Ownable.sol'),
  'zeppelin/contracts/SafeMath.sol': readFile('./zeppelin/contracts/SafeMath.sol')
}

console.log("output1")
const output = solc.compile({sources: inputs}, 1);
//for (var contractName in output.contracts)
//  console.log(contractName)

console.log("output:", output.contracts['CrowdsaleToken.sol:CrowdsaleToken']);
const abi = JSON.parse(output.contracts['CrowdsaleToken.sol:CrowdsaleToken'].interface);
//console.log("abi:", abi)
//for (var contractName in output.contracts)
//    console.log(contractName + ': ' + output.contracts[contractName].bytecode)
//const bytecode = output.contracts['CrowdsaleToken'].bytecode;
//const abi = JSON.parse(output.contracts['CrowdsaleToken'].interface);
//console.log(bytecode)
//console.log(abi)

function padTokens(s, n, m) {
  //var o = s.toFixed(n);
  var o = s;
  while (o.length < m) {
    o = " " + o;
  }
  return o;
}

function padEthers(s, n) {
  var o = s.toFixed(18);
  while (o.length < 27) {
    o = " " + o;
  }
  return o;
}

function checkAllBalances() {
  var erc20ABI = abi
  var golemAddress = "0x0aa721cc960c65b341f5663af620819148034ae1";
  //var golemContractT = web3.eth.contract(erc20ABI);
  var golemTotal = 0;
  var ethersTotal = 0;

  console.log("Data:   #     Account                                                             AXN                        ETH");
  console.log("Data: ------- ------------------------------------------ ---------------------------- --------------------------");
  var i =0;
  // Standard accounts
  web3.eth.getAccounts(function(error, accounts) {
    console.log("accounts:", accounts)
    for (var i=0; i < accounts.length; i++) {
      var golemContract = web3.eth.contract(erc20ABI).at(golemAddress)
    //accounts.forEach( function(e){
      var e = accounts[i]
      //var golemContract = golemContractT.at(golemAddress)
      var golemTokens = golemContract.balanceOf(e).div(1e18);
      golemTotal = golemTotal + golemTokens;
      var ethers = web3.fromWei(web3.eth.getBalance(e), "ether");
      ethersTotal = ethersTotal + ethers;
      console.log("Data:   " + i + "\t" + e + " " + padTokens(golemTokens, 18, 28) + " " + padTokens(ethers, 18, 26));
      i++;
    }
    console.log("Data: ------- ------------------------------------------ ---------------------------- --------------------------");
    console.log("Data:   " + i + "     Total                                      " + padTokens(golemTotal, 18, 28) + " " + padTokens(ethersTotal, 18, 26));
  });
};

checkAllBalances();
