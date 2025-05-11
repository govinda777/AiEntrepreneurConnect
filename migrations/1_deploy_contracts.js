const ReportPaymentSystem = artifacts.require("ReportPaymentSystem");

module.exports = function(deployer, network, accounts) {
  // For development, you can deploy with a dummy token address
  // Replace this with your actual token address when deploying to other networks
  const dummyTokenAddress = "0x0000000000000000000000000000000000000000";
  deployer.deploy(ReportPaymentSystem, dummyTokenAddress);
}; 