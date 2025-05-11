// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "../ReportPaymentSystem.sol";

contract TestReportPaymentSystem is ReportPaymentSystem {
    constructor(address _tokenAddress) ReportPaymentSystem(_tokenAddress) {}
} 