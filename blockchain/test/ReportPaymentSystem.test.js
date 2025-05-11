const { expectRevert, time } = require('@openzeppelin/test-helpers');
const { web3 } = require('@openzeppelin/test-helpers/src/setup');
const ReportPaymentSystemTest = artifacts.require('ReportPaymentSystemTest');
const ERC20Mock = artifacts.require('ERC20Mock');

contract('ReportPaymentSystem', function (accounts) {
  const [owner, user1, user2] = accounts;
  const REPORT_COST = web3.utils.toWei('100', 'ether');
  const REPORT_TIMEOUT = 24 * 60 * 60; // 24 hours in seconds
  const INITIAL_SUPPLY = web3.utils.toWei('1000', 'ether');

  beforeEach(async function () {
    // Deploy token mock
    this.token = await ERC20Mock.new('Platform Token', 'PTK', owner, INITIAL_SUPPLY);
    
    // Deploy ReportPaymentSystem
    this.reportSystem = await ReportPaymentSystemTest.new(this.token.address);

    // Transfer tokens to users and approve spending
    await this.token.transfer(user1, REPORT_COST, { from: owner });
    await this.token.transfer(user2, REPORT_COST, { from: owner });
    await this.token.approve(this.reportSystem.address, REPORT_COST, { from: user1 });
    await this.token.approve(this.reportSystem.address, REPORT_COST, { from: user2 });
  });

  describe('Initialization', function () {
    it('should set the correct owner', async function () {
      const contractOwner = await this.reportSystem.owner();
      assert.equal(contractOwner, owner, 'Owner not set correctly');
    });

    it('should set the correct platform token', async function () {
      const platformToken = await this.reportSystem.platformToken();
      assert.equal(platformToken, this.token.address, 'Platform token not set correctly');
    });

    it('should have the correct report cost', async function () {
      const reportCost = await this.reportSystem.REPORT_COST();
      assert.equal(reportCost.toString(), REPORT_COST, 'Report cost not set correctly');
    });
  });

  describe('Report Request', function () {
    it('should allow users to request reports', async function () {
      const result = await this.reportSystem.requestReport({ from: user1 });
      
      // Check event emission
      const event = result.logs.find(log => log.event === 'ReportRequested');
      assert.exists(event, 'ReportRequested event not emitted');
      
      // Check report creation
      const reportId = event.args.reportId;
      const report = await this.reportSystem.getReportDetails(reportId, { from: user1 });
      
      assert.equal(report.user, user1, 'Report user not set correctly');
      assert.equal(report.paid, true, 'Report not marked as paid');
      assert.equal(report.refunded, false, 'Report incorrectly marked as refunded');
    });

    it('should fail if user has insufficient tokens', async function () {
      await expectRevert(
        this.reportSystem.requestReport({ from: accounts[5] }),
        'Insufficient token balance'
      );
    });

    it('should fail if allowance is too low', async function () {
      await this.token.approve(this.reportSystem.address, 0, { from: user1 });
      await expectRevert(
        this.reportSystem.requestReport({ from: user1 }),
        'Token allowance too low'
      );
    });
  });

  describe('Report Hash Setting', function () {
    let reportId;

    beforeEach(async function () {
      const result = await this.reportSystem.requestReport({ from: user1 });
      reportId = result.logs.find(log => log.event === 'ReportRequested').args.reportId;
    });

    it('should allow owner to set report hash', async function () {
      const ipfsHash = 'QmTest123';
      const result = await this.reportSystem.setReportHash(reportId, ipfsHash, { from: owner });
      
      const event = result.logs.find(log => log.event === 'ReportGenerated');
      assert.exists(event, 'ReportGenerated event not emitted');
      
      const report = await this.reportSystem.getReportDetails(reportId, { from: user1 });
      assert.equal(report.reportHash, ipfsHash, 'Report hash not set correctly');
    });

    it('should fail if non-owner tries to set report hash', async function () {
      await expectRevert(
        this.reportSystem.setReportHash(reportId, 'QmTest123', { from: user1 }),
        'Ownable: caller is not the owner'
      );
    });

    it('should fail if report deadline has expired', async function () {
      await time.increase(REPORT_TIMEOUT + 1);
      await expectRevert(
        this.reportSystem.setReportHash(reportId, 'QmTest123', { from: owner }),
        'Report deadline expired'
      );
    });
  });

  describe('Report Refund', function () {
    let reportId;

    beforeEach(async function () {
      const result = await this.reportSystem.requestReport({ from: user1 });
      reportId = result.logs.find(log => log.event === 'ReportRequested').args.reportId;
    });

    it('should allow refund after deadline if report not generated', async function () {
      await time.increase(REPORT_TIMEOUT + 1);
      
      const initialBalance = await this.token.balanceOf(user1);
      await this.reportSystem.requestRefund(reportId, { from: user1 });
      const finalBalance = await this.token.balanceOf(user1);
      
      assert.equal(
        finalBalance.sub(initialBalance).toString(),
        REPORT_COST,
        'Refund amount incorrect'
      );
      
      const report = await this.reportSystem.getReportDetails(reportId, { from: user1 });
      assert.equal(report.refunded, true, 'Report not marked as refunded');
    });

    it('should fail if report already generated', async function () {
      await this.reportSystem.setReportHash(reportId, 'QmTest123', { from: owner });
      await time.increase(REPORT_TIMEOUT + 1);
      
      await expectRevert(
        this.reportSystem.requestRefund(reportId, { from: user1 }),
        'Report already generated'
      );
    });

    it('should fail if deadline not reached', async function () {
      await expectRevert(
        this.reportSystem.requestRefund(reportId, { from: user1 }),
        'Deadline not reached'
      );
    });
  });

  describe('Deadline Extension', function () {
    let reportId;

    beforeEach(async function () {
      const result = await this.reportSystem.requestReport({ from: user1 });
      reportId = result.logs.find(log => log.event === 'ReportRequested').args.reportId;
    });

    it('should allow owner to extend deadline', async function () {
      const extensionTime = 24 * 60 * 60; // 24 more hours
      const result = await this.reportSystem.extendDeadline(reportId, extensionTime, { from: owner });
      
      const event = result.logs.find(log => log.event === 'ReportDeadlineExtended');
      assert.exists(event, 'ReportDeadlineExtended event not emitted');
      
      const report = await this.reportSystem.getReportDetails(reportId, { from: user1 });
      assert(report.deadline > 0, 'Deadline not extended');
    });

    it('should fail if non-owner tries to extend deadline', async function () {
      await expectRevert(
        this.reportSystem.extendDeadline(reportId, 86400, { from: user1 }),
        'Ownable: caller is not the owner'
      );
    });
  });

  describe('Token Withdrawal', function () {
    beforeEach(async function () {
      await this.reportSystem.requestReport({ from: user1 });
    });

    it('should allow owner to withdraw tokens', async function () {
      const initialBalance = await this.token.balanceOf(owner);
      await this.reportSystem.withdrawTokens({ from: owner });
      const finalBalance = await this.token.balanceOf(owner);
      
      assert.equal(
        finalBalance.sub(initialBalance).toString(),
        REPORT_COST,
        'Withdrawal amount incorrect'
      );
    });

    it('should fail if non-owner tries to withdraw', async function () {
      await expectRevert(
        this.reportSystem.withdrawTokens({ from: user1 }),
        'Ownable: caller is not the owner'
      );
    });
  });

  describe('Report Queries', function () {
    let reportId;

    beforeEach(async function () {
      const result = await this.reportSystem.requestReport({ from: user1 });
      reportId = result.logs.find(log => log.event === 'ReportRequested').args.reportId;
    });

    it('should allow users to query their reports', async function () {
      const reports = await this.reportSystem.getUserReports({ from: user1 });
      assert.equal(reports.length, 1, 'Incorrect number of reports');
      assert.equal(reports[0].toString(), reportId.toString(), 'Incorrect report ID');
    });

    it('should allow users to get report details', async function () {
      const report = await this.reportSystem.getReportDetails(reportId, { from: user1 });
      assert.equal(report.user, user1, 'Incorrect report user');
      assert.equal(report.paid, true, 'Incorrect payment status');
      assert.equal(report.refunded, false, 'Incorrect refund status');
    });

    it('should fail if unauthorized user tries to get report details', async function () {
      await expectRevert(
        this.reportSystem.getReportDetails(reportId, { from: user2 }),
        'Not authorized'
      );
    });
  });
}); 