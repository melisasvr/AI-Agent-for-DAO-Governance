// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title SimpleDAOGovernance
 * @dev Basic DAO governance contract for AI agent interaction
 */
contract SimpleDAOGovernance {
    
    // Proposal structure
    struct Proposal {
        uint256 id;
        string title;
        string description;
        address proposer;
        uint256 createdAt;
        uint256 votingDeadline;
        uint256 votesFor;
        uint256 votesAgainst;
        uint256 votesAbstain;
        bool executed;
        mapping(address => bool) hasVoted;
    }
    
    // Voting options
    enum VoteChoice { For, Against, Abstain }
    
    // State variables
    mapping(uint256 => Proposal) public proposals;
    uint256 public proposalCount;
    uint256 public votingPeriod = 7 days;
    uint256 public quorum = 100; // Minimum votes required
    
    address public admin;
    mapping(address => uint256) public votingPower;
    
    // Events
    event ProposalCreated(
        uint256 indexed proposalId,
        string title,
        address indexed proposer,
        uint256 deadline
    );
    
    event VoteCast(
        uint256 indexed proposalId,
        address indexed voter,
        VoteChoice vote,
        uint256 weight
    );
    
    event ProposalExecuted(uint256 indexed proposalId);
    
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin");
        _;
    }
    
    constructor() {
        admin = msg.sender;
    }
    
    /**
     * @dev Set voting power for an address (e.g., based on token holdings)
     */
    function setVotingPower(address voter, uint256 power) external onlyAdmin {
        votingPower[voter] = power;
    }
    
    /**
     * @dev Create a new proposal
     */
    function createProposal(
        string memory title,
        string memory description
    ) external returns (uint256) {
        require(votingPower[msg.sender] > 0, "No voting power");
        
        uint256 proposalId = proposalCount++;
        Proposal storage proposal = proposals[proposalId];
        
        proposal.id = proposalId;
        proposal.title = title;
        proposal.description = description;
        proposal.proposer = msg.sender;
        proposal.createdAt = block.timestamp;
        proposal.votingDeadline = block.timestamp + votingPeriod;
        proposal.executed = false;
        
        emit ProposalCreated(proposalId, title, msg.sender, proposal.votingDeadline);
        
        return proposalId;
    }
    
    /**
     * @dev Cast a vote on a proposal
     */
    function castVote(uint256 proposalId, VoteChoice vote) external {
        require(proposalId < proposalCount, "Invalid proposal");
        require(votingPower[msg.sender] > 0, "No voting power");
        
        Proposal storage proposal = proposals[proposalId];
        
        require(block.timestamp < proposal.votingDeadline, "Voting ended");
        require(!proposal.hasVoted[msg.sender], "Already voted");
        require(!proposal.executed, "Proposal executed");
        
        uint256 weight = votingPower[msg.sender];
        proposal.hasVoted[msg.sender] = true;
        
        if (vote == VoteChoice.For) {
            proposal.votesFor += weight;
        } else if (vote == VoteChoice.Against) {
            proposal.votesAgainst += weight;
        } else {
            proposal.votesAbstain += weight;
        }
        
        emit VoteCast(proposalId, msg.sender, vote, weight);
    }
    
    /**
     * @dev Get proposal details
     */
    function getProposal(uint256 proposalId) external view returns (
        uint256 id,
        string memory title,
        string memory description,
        address proposer,
        uint256 createdAt,
        uint256 deadline,
        uint256 votesFor,
        uint256 votesAgainst,
        uint256 votesAbstain,
        bool executed
    ) {
        require(proposalId < proposalCount, "Invalid proposal");
        Proposal storage p = proposals[proposalId];
        
        return (
            p.id,
            p.title,
            p.description,
            p.proposer,
            p.createdAt,
            p.votingDeadline,
            p.votesFor,
            p.votesAgainst,
            p.votesAbstain,
            p.executed
        );
    }
    
    /**
     * @dev Execute a proposal if it passed
     */
    function executeProposal(uint256 proposalId) external {
        require(proposalId < proposalCount, "Invalid proposal");
        
        Proposal storage proposal = proposals[proposalId];
        
        require(block.timestamp >= proposal.votingDeadline, "Voting ongoing");
        require(!proposal.executed, "Already executed");
        
        uint256 totalVotes = proposal.votesFor + proposal.votesAgainst + proposal.votesAbstain;
        require(totalVotes >= quorum, "Quorum not reached");
        require(proposal.votesFor > proposal.votesAgainst, "Proposal rejected");
        
        proposal.executed = true;
        
        emit ProposalExecuted(proposalId);
        
        // Execute proposal logic here
        // This would typically call other contracts or update state
    }
    
    /**
     * @dev Check if an address has voted on a proposal
     */
    function hasVoted(uint256 proposalId, address voter) external view returns (bool) {
        require(proposalId < proposalCount, "Invalid proposal");
        return proposals[proposalId].hasVoted[voter];
    }
}


/**
 * @title AIAgentWallet
 * @dev Smart contract wallet for AI agent with governance controls
 */
contract AIAgentWallet {
    
    address public aiAgent; // EOA controlled by AI
    address public governance; // DAO governance contract
    address public emergencyAdmin; // For emergency situations
    
    uint256 public dailySpendLimit;
    uint256 public spentToday;
    uint256 public lastResetTime;
    
    bool public paused;
    
    event FundsReceived(address indexed from, uint256 amount);
    event VoteCast(address indexed dao, uint256 proposalId, uint8 vote);
    event SpendLimitUpdated(uint256 newLimit);
    event Paused(address indexed by);
    event Unpaused(address indexed by);
    
    modifier onlyAIAgent() {
        require(msg.sender == aiAgent, "Only AI agent");
        _;
    }
    
    modifier onlyGovernance() {
        require(msg.sender == governance, "Only governance");
        _;
    }
    
    modifier onlyEmergency() {
        require(msg.sender == emergencyAdmin, "Only emergency admin");
        _;
    }
    
    modifier whenNotPaused() {
        require(!paused, "Contract paused");
        _;
    }
    
    constructor(
        address _aiAgent,
        address _governance,
        address _emergencyAdmin,
        uint256 _dailySpendLimit
    ) {
        aiAgent = _aiAgent;
        governance = _governance;
        emergencyAdmin = _emergencyAdmin;
        dailySpendLimit = _dailySpendLimit;
        lastResetTime = block.timestamp;
    }
    
    receive() external payable {
        emit FundsReceived(msg.sender, msg.value);
    }
    
    /**
     * @dev Reset daily spending if 24 hours passed
     */
    function _checkAndResetDaily() internal {
        if (block.timestamp >= lastResetTime + 1 days) {
            spentToday = 0;
            lastResetTime = block.timestamp;
        }
    }
    
    /**
     * @dev AI agent casts vote on DAO proposal
     */
    function castVote(
        address daoContract,
        uint256 proposalId,
        uint8 vote
    ) external onlyAIAgent whenNotPaused {
        // Call DAO contract to cast vote
        (bool success, ) = daoContract.call(
            abi.encodeWithSignature(
                "castVote(uint256,uint8)",
                proposalId,
                vote
            )
        );
        require(success, "Vote failed");
        
        emit VoteCast(daoContract, proposalId, vote);
    }
    
    /**
     * @dev Transfer funds with daily limit
     */
    function transfer(
        address payable to,
        uint256 amount
    ) external onlyAIAgent whenNotPaused {
        _checkAndResetDaily();
        
        require(spentToday + amount <= dailySpendLimit, "Daily limit exceeded");
        require(address(this).balance >= amount, "Insufficient balance");
        
        spentToday += amount;
        
        (bool success, ) = to.call{value: amount}("");
        require(success, "Transfer failed");
    }
    
    /**
     * @dev Update daily spend limit (governance only)
     */
    function updateSpendLimit(uint256 newLimit) external onlyGovernance {
        dailySpendLimit = newLimit;
        emit SpendLimitUpdated(newLimit);
    }
    
    /**
     * @dev Emergency pause
     */
    function pause() external onlyEmergency {
        paused = true;
        emit Paused(msg.sender);
    }
    
    /**
     * @dev Unpause
     */
    function unpause() external onlyEmergency {
        paused = false;
        emit Unpaused(msg.sender);
    }
    
    /**
     * @dev Get contract balance
     */
    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
    
    /**
     * @dev Get remaining daily spend allowance
     */
    function getRemainingDailyAllowance() external view returns (uint256) {
        if (block.timestamp >= lastResetTime + 1 days) {
            return dailySpendLimit;
        }
        
        if (spentToday >= dailySpendLimit) {
            return 0;
        }
        
        return dailySpendLimit - spentToday;
    }
}


/**
 * @title VotingMetricsRegistry
 * @dev On-chain registry of AI agent's voting criteria for transparency
 */
contract VotingMetricsRegistry {
    
    struct Metrics {
        uint256 treasuryImpactWeight;      // Basis points (0-10000)
        uint256 communityAlignmentWeight;  // Basis points
        uint256 technicalFeasibilityWeight; // Basis points
        uint256 riskAssessmentWeight;      // Basis points
        uint256 minScoreToSupport;         // Basis points (e.g., 6000 = 60%)
        uint256 maxTreasurySpendPct;       // Basis points
        uint256 lastUpdated;
        string rationale;
    }
    
    address public aiAgentWallet;
    address public governance;
    Metrics public currentMetrics;
    
    mapping(uint256 => Metrics) public historicalMetrics;
    uint256 public metricsVersion;
    
    event MetricsUpdated(
        uint256 indexed version,
        uint256 timestamp,
        string rationale
    );
    
    modifier onlyGovernance() {
        require(msg.sender == governance, "Only governance");
        _;
    }
    
    constructor(address _aiAgentWallet, address _governance) {
        aiAgentWallet = _aiAgentWallet;
        governance = _governance;
        
        // Set default metrics
        currentMetrics = Metrics({
            treasuryImpactWeight: 3000,        // 30%
            communityAlignmentWeight: 2500,    // 25%
            technicalFeasibilityWeight: 2500,  // 25%
            riskAssessmentWeight: 2000,        // 20%
            minScoreToSupport: 6000,           // 60%
            maxTreasurySpendPct: 1000,         // 10%
            lastUpdated: block.timestamp,
            rationale: "Initial configuration"
        });
        
        historicalMetrics[0] = currentMetrics;
    }
    
    /**
     * @dev Update voting metrics (governance only)
     */
    function updateMetrics(
        uint256 _treasuryImpactWeight,
        uint256 _communityAlignmentWeight,
        uint256 _technicalFeasibilityWeight,
        uint256 _riskAssessmentWeight,
        uint256 _minScoreToSupport,
        uint256 _maxTreasurySpendPct,
        string memory _rationale
    ) external onlyGovernance {
        // Validate weights sum to 10000 (100%)
        require(
            _treasuryImpactWeight + 
            _communityAlignmentWeight + 
            _technicalFeasibilityWeight + 
            _riskAssessmentWeight == 10000,
            "Weights must sum to 10000"
        );
        
        require(_minScoreToSupport <= 10000, "Invalid min score");
        require(_maxTreasurySpendPct <= 10000, "Invalid max spend");
        
        metricsVersion++;
        
        Metrics memory newMetrics = Metrics({
            treasuryImpactWeight: _treasuryImpactWeight,
            communityAlignmentWeight: _communityAlignmentWeight,
            technicalFeasibilityWeight: _technicalFeasibilityWeight,
            riskAssessmentWeight: _riskAssessmentWeight,
            minScoreToSupport: _minScoreToSupport,
            maxTreasurySpendPct: _maxTreasurySpendPct,
            lastUpdated: block.timestamp,
            rationale: _rationale
        });
        
        currentMetrics = newMetrics;
        historicalMetrics[metricsVersion] = newMetrics;
        
        emit MetricsUpdated(metricsVersion, block.timestamp, _rationale);
    }
    
    /**
     * @dev Get current metrics
     */
    function getCurrentMetrics() external view returns (
        uint256 treasuryImpact,
        uint256 communityAlignment,
        uint256 technicalFeasibility,
        uint256 riskAssessment,
        uint256 minScore,
        uint256 maxSpend,
        uint256 lastUpdated,
        string memory rationale
    ) {
        Metrics memory m = currentMetrics;
        return (
            m.treasuryImpactWeight,
            m.communityAlignmentWeight,
            m.technicalFeasibilityWeight,
            m.riskAssessmentWeight,
            m.minScoreToSupport,
            m.maxTreasurySpendPct,
            m.lastUpdated,
            m.rationale
        );
    }
    
    /**
     * @dev Get historical metrics by version
     */
    function getHistoricalMetrics(uint256 version) external view returns (
        uint256 treasuryImpact,
        uint256 communityAlignment,
        uint256 technicalFeasibility,
        uint256 riskAssessment,
        uint256 minScore,
        uint256 maxSpend,
        uint256 lastUpdated,
        string memory rationale
    ) {
        require(version <= metricsVersion, "Invalid version");
        Metrics memory m = historicalMetrics[version];
        return (
            m.treasuryImpactWeight,
            m.communityAlignmentWeight,
            m.technicalFeasibilityWeight,
            m.riskAssessmentWeight,
            m.minScoreToSupport,
            m.maxTreasurySpendPct,
            m.lastUpdated,
            m.rationale
        );
    }
}