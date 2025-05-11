// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "../ReportPaymentSystem.sol";

contract ReportPaymentSystemTest is ReportPaymentSystem {
    constructor(address _tokenAddress) ReportPaymentSystem(_tokenAddress) {}
} 