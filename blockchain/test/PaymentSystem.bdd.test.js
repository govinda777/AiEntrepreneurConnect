const ReportPaymentSystem = artifacts.require("ReportPaymentSystem");
const { expect } = require("chai");
const truffleAssert = require("truffle-assertions");

contract("ReportPaymentSystem (BDD)", accounts => {
  const [owner, investor, entrepreneur, validator] = accounts;
  let paymentSystem;

  beforeEach(async () => {
    paymentSystem = await ReportPaymentSystem.new({ from: owner });
  });

  describe("Payment System Setup", () => {
    it("should be properly initialized with the correct owner", async () => {
      const actualOwner = await paymentSystem.owner();
      expect(actualOwner).to.equal(owner);
    });
  });

  describe("Transaction Flow", () => {
    context("When an investor initiates a payment", () => {
      const paymentAmount = web3.utils.toWei("1", "ether");
      
      it("should allow investor to deposit funds", async () => {
        await paymentSystem.depositFunds({ 
          from: investor,
          value: paymentAmount
        });
        
        const balance = await paymentSystem.getBalance(investor);
        expect(balance.toString()).to.equal(paymentAmount);
      });

      it("should emit a DepositMade event", async () => {
        const result = await paymentSystem.depositFunds({ 
          from: investor,
          value: paymentAmount
        });

        truffleAssert.eventEmitted(result, 'DepositMade', (ev) => {
          return ev.investor === investor && ev.amount.toString() === paymentAmount;
        });
      });
    });

    context("When processing a payment to an entrepreneur", () => {
      const paymentAmount = web3.utils.toWei("1", "ether");
      
      beforeEach(async () => {
        await paymentSystem.depositFunds({ 
          from: investor,
          value: paymentAmount
        });
      });

      it("should transfer funds to the entrepreneur after validation", async () => {
        const initialBalance = await web3.eth.getBalance(entrepreneur);
        
        await paymentSystem.initiatePayment(
          entrepreneur,
          paymentAmount,
          "Project milestone payment",
          { from: investor }
        );

        await paymentSystem.validatePayment(
          investor,
          entrepreneur,
          paymentAmount,
          { from: validator }
        );

        const finalBalance = await web3.eth.getBalance(entrepreneur);
        expect(BigInt(finalBalance) - BigInt(initialBalance)).to.equal(BigInt(paymentAmount));
      });

      it("should maintain payment history", async () => {
        await paymentSystem.initiatePayment(
          entrepreneur,
          paymentAmount,
          "Project milestone payment",
          { from: investor }
        );

        const payment = await paymentSystem.getPaymentDetails(investor, entrepreneur);
        expect(payment.amount.toString()).to.equal(paymentAmount);
        expect(payment.description).to.equal("Project milestone payment");
      });
    });
  });

  describe("Security Features", () => {
    context("When attempting unauthorized operations", () => {
      it("should prevent non-validators from validating payments", async () => {
        const paymentAmount = web3.utils.toWei("1", "ether");
        
        await paymentSystem.depositFunds({ 
          from: investor,
          value: paymentAmount
        });

        await paymentSystem.initiatePayment(
          entrepreneur,
          paymentAmount,
          "Project payment",
          { from: investor }
        );

        await truffleAssert.reverts(
          paymentSystem.validatePayment(
            investor,
            entrepreneur,
            paymentAmount,
            { from: entrepreneur }
          ),
          "Not authorized to validate"
        );
      });

      it("should prevent withdrawals exceeding available balance", async () => {
        const excessAmount = web3.utils.toWei("10", "ether");
        
        await truffleAssert.reverts(
          paymentSystem.initiatePayment(
            entrepreneur,
            excessAmount,
            "Excessive payment",
            { from: investor }
          ),
          "Insufficient balance"
        );
      });
    });
  });

  describe("Transaction Limits", () => {
    context("When processing transactions with limits", () => {
      it("should enforce maximum transaction limits", async () => {
        const maxLimit = await paymentSystem.getMaxTransactionLimit();
        const excessiveAmount = maxLimit.add(web3.utils.toBN(web3.utils.toWei("1", "ether")));

        await truffleAssert.reverts(
          paymentSystem.depositFunds({ 
            from: investor,
            value: excessiveAmount
          }),
          "Amount exceeds transaction limit"
        );
      });
    });
  });
}); 