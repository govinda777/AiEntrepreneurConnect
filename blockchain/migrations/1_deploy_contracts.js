const ERC20Mock = artifacts.require("ERC20Mock");
const ReportPaymentSystemTest = artifacts.require("ReportPaymentSystemTest");

module.exports = async function (deployer, network, accounts) {
  const owner = accounts[0];
  const initialSupply = web3.utils.toWei('1000000', 'ether'); // 1 million tokens

  // Deploy token mock only in test networks
  if (network === 'development' || network === 'test') {
    await deployer.deploy(ERC20Mock, 'Platform Token', 'PTK', owner, initialSupply);
    const token = await ERC20Mock.deployed();
    
    // Deploy ReportPaymentSystem with the mock token
    await deployer.deploy(ReportPaymentSystemTest, token.address);
  }
}; 