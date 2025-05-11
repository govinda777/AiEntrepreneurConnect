// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

abstract contract ReportPaymentSystem is ReentrancyGuard, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _reportIds;

    // Token da plataforma
    IERC20 public platformToken;
    
    // Custo fixo por relatório (100 tokens)
    uint256 public constant REPORT_COST = 100 * 10**18;
    
    // Tempo máximo para gerar um relatório (24 horas)
    uint256 public constant REPORT_TIMEOUT = 24 hours;

    struct Report {
        uint256 id;
        address user;
        uint256 timestamp;
        string reportHash; // IPFS hash do relatório
        bool paid;
        bool refunded;
        uint256 deadline;
    }

    // Mapeamento de relatórios
    mapping(uint256 => Report) public reports;
    // Mapeamento de relatórios por usuário
    mapping(address => uint256[]) public userReports;
    // Saldo total do contrato em tokens
    uint256 public totalTokenBalance;

    // Eventos
    event ReportRequested(uint256 indexed reportId, address indexed user, uint256 deadline);
    event ReportGenerated(uint256 indexed reportId, string reportHash);
    event PaymentReceived(address indexed from, uint256 amount);
    event PaymentWithdrawn(address indexed to, uint256 amount);
    event ReportRefunded(uint256 indexed reportId, address indexed user, uint256 amount);
    event ReportDeadlineExtended(uint256 indexed reportId, uint256 newDeadline);

    constructor(address _tokenAddress) {
        _transferOwnership(msg.sender);
        platformToken = IERC20(_tokenAddress);
    }

    // Função para solicitar um relatório usando tokens
    function requestReport() external nonReentrant returns (uint256) {
        require(platformToken.balanceOf(msg.sender) >= REPORT_COST, "Insufficient token balance");
        require(platformToken.allowance(msg.sender, address(this)) >= REPORT_COST, "Token allowance too low");

        // Transferir tokens do usuário para o contrato
        require(platformToken.transferFrom(msg.sender, address(this), REPORT_COST), "Token transfer failed");

        _reportIds.increment();
        uint256 reportId = _reportIds.current();
        uint256 deadline = block.timestamp + REPORT_TIMEOUT;

        reports[reportId] = Report({
            id: reportId,
            user: msg.sender,
            timestamp: block.timestamp,
            reportHash: "",
            paid: true,
            refunded: false,
            deadline: deadline
        });

        userReports[msg.sender].push(reportId);
        totalTokenBalance += REPORT_COST;

        emit ReportRequested(reportId, msg.sender, deadline);
        return reportId;
    }

    // Função para definir o hash IPFS do relatório (apenas owner)
    function setReportHash(uint256 reportId, string memory ipfsHash) external onlyOwner {
        require(reports[reportId].paid, "Report not paid");
        require(!reports[reportId].refunded, "Report was refunded");
        require(bytes(reports[reportId].reportHash).length == 0, "Report already generated");
        require(block.timestamp <= reports[reportId].deadline, "Report deadline expired");

        reports[reportId].reportHash = ipfsHash;
        emit ReportGenerated(reportId, ipfsHash);
    }

    // Função para solicitar reembolso de um relatório não gerado
    function requestRefund(uint256 reportId) external nonReentrant {
        Report storage report = reports[reportId];
        require(report.user == msg.sender, "Not report owner");
        require(report.paid, "Report not paid");
        require(!report.refunded, "Already refunded");
        require(bytes(report.reportHash).length == 0, "Report already generated");
        require(block.timestamp > report.deadline, "Deadline not reached");

        report.refunded = true;
        totalTokenBalance -= REPORT_COST;
        require(platformToken.transfer(msg.sender, REPORT_COST), "Refund transfer failed");

        emit ReportRefunded(reportId, msg.sender, REPORT_COST);
    }

    // Função para estender o prazo de um relatório (apenas owner)
    function extendDeadline(uint256 reportId, uint256 extensionTime) external onlyOwner {
        Report storage report = reports[reportId];
        require(report.paid, "Report not paid");
        require(!report.refunded, "Report was refunded");
        require(bytes(report.reportHash).length == 0, "Report already generated");

        report.deadline = block.timestamp + extensionTime;
        emit ReportDeadlineExtended(reportId, report.deadline);
    }

    // Função para retirar os tokens (apenas owner)
    function withdrawTokens() external onlyOwner nonReentrant {
        uint256 amount = totalTokenBalance;
        require(amount > 0, "No tokens to withdraw");

        totalTokenBalance = 0;
        require(platformToken.transfer(owner(), amount), "Token transfer failed");

        emit PaymentWithdrawn(owner(), amount);
    }

    // Função para consultar relatórios do usuário
    function getUserReports() external view returns (uint256[] memory) {
        return userReports[msg.sender];
    }

    // Função para consultar detalhes de um relatório
    function getReportDetails(uint256 reportId) external view returns (Report memory) {
        require(reports[reportId].user == msg.sender || owner() == msg.sender, "Not authorized");
        return reports[reportId];
    }

    // Função para consultar o custo do relatório em tokens
    function getReportCost() external pure returns (uint256) {
        return REPORT_COST;
    }

    // Função para verificar o saldo em tokens do contrato
    function getContractTokenBalance() external view returns (uint256) {
        return platformToken.balanceOf(address(this));
    }
} 