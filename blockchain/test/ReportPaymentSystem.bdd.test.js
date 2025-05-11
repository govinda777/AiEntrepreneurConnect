const TestReportPaymentSystem = artifacts.require("TestReportPaymentSystem");
const MockToken = artifacts.require("MockToken");
const { expect } = require("chai");
const truffleAssert = require("truffle-assertions");
const { time } = require("@openzeppelin/test-helpers");

contract("ReportPaymentSystem (BDD)", accounts => {
  const [owner, user1, user2] = accounts;
  let paymentSystem;
  let mockToken;
  const REPORT_COST = web3.utils.toWei("100", "ether");
  const ONE_DAY = 86400; // 24 hours in seconds

  beforeEach(async () => {
    // Deploy mock token
    mockToken = await MockToken.new({ from: owner });
    // Deploy payment system
    paymentSystem = await TestReportPaymentSystem.new(mockToken.address, { from: owner });
    
    // Mint tokens for testing
    await mockToken.mint(user1, web3.utils.toWei("1000", "ether"));
    await mockToken.mint(user2, web3.utils.toWei("1000", "ether"));
  });

  describe("System Setup", () => {
    it("should be properly initialized with the correct owner and token", async () => {
      const actualOwner = await paymentSystem.owner();
      const actualToken = await paymentSystem.platformToken();
      
      expect(actualOwner).to.equal(owner);
      expect(actualToken).to.equal(mockToken.address);
    });

    it("should have the correct report cost", async () => {
      const cost = await paymentSystem.getReportCost();
      expect(cost.toString()).to.equal(REPORT_COST);
    });
  });

  describe("Report Request Flow", () => {
    context("When a user requests a report", () => {
      beforeEach(async () => {
        await mockToken.approve(paymentSystem.address, REPORT_COST, { from: user1 });
      });

      it("should allow users to request reports with sufficient tokens", async () => {
        const result = await paymentSystem.requestReport({ from: user1 });
        
        truffleAssert.eventEmitted(result, 'ReportRequested', (ev) => {
          return ev.user === user1;
        });

        const reportId = result.logs[0].args.reportId;
        const report = await paymentSystem.getReportDetails(reportId, { from: user1 });
        
        expect(report.user).to.equal(user1);
        expect(report.paid).to.be.true;
        expect(report.refunded).to.be.false;
        expect(report.reportHash).to.equal("");
      });

      it("should update contract token balance after report request", async () => {
        await paymentSystem.requestReport({ from: user1 });
        
        const contractBalance = await paymentSystem.getContractTokenBalance();
        expect(contractBalance.toString()).to.equal(REPORT_COST);
      });

      it("should fail when user has insufficient tokens", async () => {
        const poorUser = accounts[5];
        await mockToken.approve(paymentSystem.address, REPORT_COST, { from: poorUser });
        
        await truffleAssert.reverts(
          paymentSystem.requestReport({ from: poorUser }),
          "Insufficient token balance"
        );
      });
    });
  });

  describe("Report Generation", () => {
    let reportId;
    const ipfsHash = "QmTest123";

    beforeEach(async () => {
      await mockToken.approve(paymentSystem.address, REPORT_COST, { from: user1 });
      const result = await paymentSystem.requestReport({ from: user1 });
      reportId = result.logs[0].args.reportId;
    });

    context("When owner generates a report", () => {
      it("should allow owner to set report hash", async () => {
        const result = await paymentSystem.setReportHash(reportId, ipfsHash, { from: owner });
        
        truffleAssert.eventEmitted(result, 'ReportGenerated', (ev) => {
          return ev.reportId.toString() === reportId.toString() && ev.reportHash === ipfsHash;
        });

        const report = await paymentSystem.getReportDetails(reportId, { from: user1 });
        expect(report.reportHash).to.equal(ipfsHash);
      });

      it("should not allow non-owners to set report hash", async () => {
        await truffleAssert.reverts(
          paymentSystem.setReportHash(reportId, ipfsHash, { from: user2 }),
          "Ownable: caller is not the owner"
        );
      });

      it("should not allow setting hash after deadline", async () => {
        await time.increase(ONE_DAY + 1);
        
        await truffleAssert.reverts(
          paymentSystem.setReportHash(reportId, ipfsHash, { from: owner }),
          "Report deadline expired"
        );
      });
    });
  });

  describe("Refund Process", () => {
    let reportId;

    beforeEach(async () => {
      await mockToken.approve(paymentSystem.address, REPORT_COST, { from: user1 });
      const result = await paymentSystem.requestReport({ from: user1 });
      reportId = result.logs[0].args.reportId;
    });

    context("When report deadline passes without generation", () => {
      it("should allow user to request refund", async () => {
        await time.increase(ONE_DAY + 1);
        
        const initialBalance = await mockToken.balanceOf(user1);
        const result = await paymentSystem.requestRefund(reportId, { from: user1 });
        
        truffleAssert.eventEmitted(result, 'ReportRefunded', (ev) => {
          return ev.reportId.toString() === reportId.toString() && 
                 ev.user === user1 &&
                 ev.amount.toString() === REPORT_COST;
        });

        const finalBalance = await mockToken.balanceOf(user1);
        expect(finalBalance.sub(initialBalance).toString()).to.equal(REPORT_COST);
      });

      it("should not allow refund before deadline", async () => {
        await truffleAssert.reverts(
          paymentSystem.requestRefund(reportId, { from: user1 }),
          "Deadline not reached"
        );
      });

      it("should not allow refund of generated reports", async () => {
        await paymentSystem.setReportHash(reportId, "QmTest123", { from: owner });
        await time.increase(ONE_DAY + 1);
        
        await truffleAssert.reverts(
          paymentSystem.requestRefund(reportId, { from: user1 }),
          "Report already generated"
        );
      });
    });
  });

  describe("Deadline Extension", () => {
    let reportId;

    beforeEach(async () => {
      await mockToken.approve(paymentSystem.address, REPORT_COST, { from: user1 });
      const result = await paymentSystem.requestReport({ from: user1 });
      reportId = result.logs[0].args.reportId;
    });

    context("When owner extends report deadline", () => {
      it("should allow owner to extend deadline", async () => {
        const extensionTime = ONE_DAY;
        const result = await paymentSystem.extendDeadline(reportId, extensionTime, { from: owner });
        
        truffleAssert.eventEmitted(result, 'ReportDeadlineExtended');
        
        const report = await paymentSystem.getReportDetails(reportId, { from: user1 });
        const expectedDeadline = (await time.latest()).toNumber() + extensionTime;
        expect(report.deadline.toNumber()).to.be.closeTo(expectedDeadline, 2);
      });

      it("should not allow non-owners to extend deadline", async () => {
        await truffleAssert.reverts(
          paymentSystem.extendDeadline(reportId, ONE_DAY, { from: user2 }),
          "Ownable: caller is not the owner"
        );
      });
    });
  });

  describe("Token Management", () => {
    beforeEach(async () => {
      await mockToken.approve(paymentSystem.address, REPORT_COST, { from: user1 });
      await paymentSystem.requestReport({ from: user1 });
    });

    context("When owner withdraws tokens", () => {
      it("should allow owner to withdraw accumulated tokens", async () => {
        const initialBalance = await mockToken.balanceOf(owner);
        const result = await paymentSystem.withdrawTokens({ from: owner });
        
        truffleAssert.eventEmitted(result, 'PaymentWithdrawn', (ev) => {
          return ev.to === owner && ev.amount.toString() === REPORT_COST;
        });

        const finalBalance = await mockToken.balanceOf(owner);
        expect(finalBalance.sub(initialBalance).toString()).to.equal(REPORT_COST);
      });

      it("should not allow non-owners to withdraw tokens", async () => {
        await truffleAssert.reverts(
          paymentSystem.withdrawTokens({ from: user2 }),
          "Ownable: caller is not the owner"
        );
      });
    });
  });

  describe("Report Queries", () => {
    let reportId;

    beforeEach(async () => {
      await mockToken.approve(paymentSystem.address, REPORT_COST, { from: user1 });
      const result = await paymentSystem.requestReport({ from: user1 });
      reportId = result.logs[0].args.reportId;
    });

    it("should allow users to query their own reports", async () => {
      const reports = await paymentSystem.getUserReports({ from: user1 });
      expect(reports.length).to.equal(1);
      expect(reports[0].toString()).to.equal(reportId.toString());
    });

    it("should allow users to get details of their reports", async () => {
      const report = await paymentSystem.getReportDetails(reportId, { from: user1 });
      expect(report.user).to.equal(user1);
      expect(report.paid).to.be.true;
      expect(report.refunded).to.be.false;
    });

    it("should not allow users to get details of others' reports", async () => {
      await truffleAssert.reverts(
        paymentSystem.getReportDetails(reportId, { from: user2 }),
        "Not authorized"
      );
    });
  });
}); 