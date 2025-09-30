# AI Agent for DAO Governance
- This project implements an AI-powered agent for analyzing and voting on DAO governance proposals. 
- It evaluates proposals based on treasury impact, community alignment, technical feasibility, and risk assessment, then casts votes (FOR, AGAINST, or ABSTAIN) in a mock environment. 
- The agent generates visualizations of the analysis results using Matplotlib, displaying three charts: Proposal Analysis Scores, Overall Scores with Threshold, and Voting Summary.

## Features
- Proposal Analysis: Evaluates proposals using weighted metrics (35% treasury, 30% community, 20% technical, 15% risk).
- Automated Voting: Casts votes based on a minimum score threshold (0.65).
- Visualization: Generates three charts using Matplotlib:
- Bar chart of individual scores per proposal.
- Bar chart of overall scores with a threshold line.
- Pie chart of voting distribution (e.g., 1 FOR, 0 AGAINST, 4 ABSTAIN).
- Mock Data Mode: Uses test_proposals.json for testing without blockchain interaction.
- Configurable: Metrics and settings defined in main.py and deploy_info.json.

## Prerequisites
- Python 3.6+: Ensure Python is installed (python --version).
- Dependencies:
- web3.py: For blockchain interaction (mock mode doesn’t require a live blockchain).
- eth-account: For account management.
- matplotlib: For chart visualization.
- numpy: For numerical operations in charts.
- Operating System: Tested on Windows or Mac.
- Ganache (Optional): For future blockchain integration.

## Installation
1. Clone or Set Up the Project:
- Place all project files in a directory (e.g., C:\Users\name\files\Program\title of the project).

2. Install Dependencies:
- `pip install web3 eth-account matplotlib numpy`
3. Verify Files: Ensure the following files are present:
- main.py: Main script for the AI agent.
- deployment_testing.py: Script to generate mock proposal data.
- deploy_info.json: Configuration file with mock deployment details (e.g., AI agent address, private key).

## Usage
1. Generate Mock Proposals:
- Run the deployment testing script to create `test_proposals.json`:
- `python deployment_testing.py`
- This generates 5 mock proposals for testing.

2. Run the AI Agent:
- Execute the main script:
- `python main.py`
- The script will:
- Load 5 proposals from `test_proposals.json`.
- Analyze each proposal and print scores (e.g., Proposal #0: Treasury=0.30, Community=0.50, Technical=0.70, Risk=0.60, Overall=0.48).
- Cast votes (e.g., 1 FOR, 0 AGAINST, 4 ABSTAIN).
- Display three Matplotlib chart windows:
- Proposal Analysis Scores: Bar chart of scores per category.
- Overall Scores with Threshold: Bar chart with a 0.65 threshold line.
- Voting Summary: Pie chart of vote distribution.

3. Expected Output:
- Console output showing analysis and voting results.
- Three pop-up chart windows visualizing the results.
- Example console output:
```
✓: • Loaded 5 proposals from test_proposals.json
...
📊 VOTING SUMMARY
Total Votes: 5
FOR: 1
AGAINST: 0
ABSTAIN: 4
```

## Configuration
- Metrics: Defined in `main.py` under `custom_metrics`:
  ```
    custom_metrics = VotingMetrics(
    treasury_impact_weight=0.35,
    community_alignment_weight=0.30,
    technical_feasibility_weight=0.20,
    risk_assessment_weight=0.15,
    min_score_to_support=0.65
  )

- Deployment Info: Stored in deploy_info.json (no .env file needed):
```
  {
  "network": "ganache-local",
  "governance_address": "0x5FbDB2315678afecb367f032d93F642f64180aa3",
  "ai_wallet_address": "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512",
  "metrics_registry_address": "0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0",
  "ai_agent_address": "0xc0A606038c2E7c86a6acaDf9D9Dd0F55480E3149",
  "deployer_address": "0xf3dD9E569D8Ba6726FE3b7f54A1CFB19998bDc88",
  "ai_agent_private_key": "0x55d655def66eeca0ab86237c4407f3a92033b6cc32d9aa4f8af9f9f9c30fb87a",
  "note": "MOCK DEPLOYMENT - Contracts not actually deployed"
}
``` 

## Troubleshooting
- Charts Not Displaying:
- Ensure matplotlib and numpy are installed (pip show matplotlib numpy).
- Verify you’re running on a system with a graphical interface (Windows should work fine).
- If charts don’t pop up, check for errors in the console and ensure test_proposals.json exists.
- Missing `test_proposals.json`:
- Run python deployment_testing.py to generate it.
- Python Errors:
- Ensure Python 3.6+ is used.
- Check console output for specific errors and address missing dependencies.
- Chart Data Mismatch:
- Verify `test_proposals.json` contains 5 proposals with expected descriptions.
- Ensure `main.py` is the Matplotlib version.


## Notes
- The project currently runs in mock mode (use_mock_data=True), using `test_proposals.json` for testing.
- No .env file is required; configuration is handled via `deploy_info.json`.
- Charts are displayed as pop-up windows using Matplotlib, requiring no browser or internet connection.

## Contributing
- Contributions welcome! Fork the repo, make changes, and submit a pull request. Open an issue for major updates. 

## License
- This project is for educational and testing purposes. No license is specified.
