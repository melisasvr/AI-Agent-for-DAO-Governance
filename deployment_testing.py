"""
Deployment Script for DAO Governance AI Agent
Works with Ganache local node
"""

import json
import os
from web3 import Web3
from eth_account import Account

class SimpleDAODeployer:
    """Simplified deployer that works with Ganache"""
    
    def __init__(self):
        # Connect to Ganache
        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
        
        # Use Ganache's account #0
        self.deployer_key = "0xcdc181bca0ad823df429e136f307adbe95334a5cdc626e2898611264468e9866"
        self.deployer = Account.from_key(self.deployer_key)
        
        # AI Agent will be account #1
        self.ai_agent_key = "0x55d655def66eeca0ab86237c4407f3a92033b6cc32d9aa4f8af9f9f9c30fb87a"
        self.ai_agent = Account.from_key(self.ai_agent_key)
        
        print("=" * 60)
        print("DAO GOVERNANCE AI AGENT - DEPLOYMENT")
        print("=" * 60)
        print(f"\nDeployer: {self.deployer.address}")
        print(f"AI Agent: {self.ai_agent.address}")
        
        # Check connection
        try:
            balance = self.w3.eth.get_balance(self.deployer.address)
            print(f"Deployer Balance: {self.w3.from_wei(balance, 'ether')} ETH")
            print(f"Connected to: {self.w3.provider.endpoint_uri}")
            print(f"Chain ID: {self.w3.eth.chain_id}")
        except Exception as e:
            print(f"\nERROR: Cannot connect to blockchain!")
            print(f"Make sure Ganache is running: ganache")
            raise e
    
    def create_mock_deployment(self):
        """
        Create mock deployment for testing without actual contract deployment
        This allows you to test the agent logic without compiling/deploying
        """
        print("\n" + "=" * 60)
        print("CREATING MOCK DEPLOYMENT INFO")
        print("=" * 60)
        
        # Mock contract addresses (won't actually work for real transactions)
        deployment_info = {
            "network": "ganache-local",
            "governance_address": "0x5FbDB2315678afecb367f032d93F642f64180aa3",
            "ai_wallet_address": "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512",
            "metrics_registry_address": "0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0",
            "ai_agent_address": self.ai_agent.address,
            "deployer_address": self.deployer.address,
            "ai_agent_private_key": self.ai_agent_key,
            "note": "MOCK DEPLOYMENT - Contracts not actually deployed"
        }
        
        # Save to file
        with open('deployment_info.json', 'w') as f:
            json.dump(deployment_info, f, indent=2)
        
        print("\nMock deployment info saved to: deployment_info.json")
        print("\nWARNING: This is a mock deployment!")
        print("Contracts are not actually deployed.")
        print("Use this to test the agent's analysis logic only.")
        
        return deployment_info
    
    def create_test_proposals_file(self):
        """Create a JSON file with test proposals for local testing"""
        proposals = [
            {
                "id": 0,
                "title": "Treasury Diversification Strategy",
                "description": """
## Proposal: Diversify DAO Treasury into Stablecoins

### Summary
Allocate 30% of treasury (approximately 50 ETH) into USDC and DAI stablecoins to reduce volatility exposure.

### Rationale
- Current 100% ETH exposure creates high volatility risk
- Stablecoins provide liquidity for operational expenses
- Industry best practice for DAO treasury management

### Budget
Total cost: 50 ETH + gas fees

### Timeline
6 weeks from approval
                """,
                "proposer": self.deployer.address,
                "votesFor": 0,
                "votesAgainst": 0,
                "votesAbstain": 0,
                "executed": False
            },
            {
                "id": 1,
                "title": "Fund Community Education Program",
                "description": """
## Proposal: Launch Web3 Education Initiative

### Summary
Establish a community education program with 10 ETH funding for workshops, tutorials, and documentation.

### Goals
- Create comprehensive developer documentation
- Host monthly community workshops
- Produce video tutorial series
- Build example projects and templates

### Budget
- Documentation: 3 ETH
- Video production: 4 ETH
- Workshops: 2 ETH
- Contingency: 1 ETH

### Timeline
3 months with monthly progress reports
                """,
                "proposer": self.deployer.address,
                "votesFor": 0,
                "votesAgainst": 0,
                "votesAbstain": 0,
                "executed": False
            },
            {
                "id": 2,
                "title": "Implement Quadratic Voting",
                "description": """
## Proposal: Upgrade to Quadratic Voting Mechanism

### Summary
Implement quadratic voting to improve democratic decision-making and reduce whale influence.

### Technical Details
- Use proven OpenZeppelin contracts
- Security audit by ConsenSys Diligence
- 2-week testing period on testnet
- Gradual rollout with fallback mechanism

### Budget
- Development: 15 ETH
- Security audit: 20 ETH
- Testing: 5 ETH
Total: 40 ETH

### Timeline
- Development: 6 weeks
- Audit: 4 weeks
- Testing: 2 weeks
Total: 13 weeks
                """,
                "proposer": self.deployer.address,
                "votesFor": 0,
                "votesAgainst": 0,
                "votesAbstain": 0,
                "executed": False
            },
            {
                "id": 3,
                "title": "RISKY: Remove All Governance Delays",
                "description": """
## Proposal: Eliminate All Security Delays

Remove all security delays for instant execution.
No audit, no testing, deploy immediately.

This will allow the DAO to react instantly to any situation.
Vote YES to move fast and break things.
                """,
                "proposer": self.deployer.address,
                "votesFor": 0,
                "votesAgainst": 0,
                "votesAbstain": 0,
                "executed": False
            },
            {
                "id": 4,
                "title": "Monthly Contributor Grants Program",
                "description": """
## Proposal: Establish Recurring Grant Program

### Summary
Create a sustainable grants program allocating 5 ETH monthly to community contributors.

### Structure
- Open applications every month
- Review committee of 5 members
- Grant sizes: 0.5-2 ETH per project
- Focus areas: development, design, community growth

### Budget
60 ETH annual (5 ETH x 12 months)

### Timeline
Start next month, ongoing program
                """,
                "proposer": self.deployer.address,
                "votesFor": 0,
                "votesAgainst": 0,
                "votesAbstain": 0,
                "executed": False
            }
        ]
        
        with open('test_proposals.json', 'w') as f:
            json.dump(proposals, f, indent=2)
        
        print("\nTest proposals saved to: test_proposals.json")
        print(f"Created {len(proposals)} test proposals for analysis")
        return proposals


def main():
    try:
        deployer = SimpleDAODeployer()
        
        # Create mock deployment
        deployment = deployer.create_mock_deployment()
        
        # Create test proposals
        proposals = deployer.create_test_proposals_file()
        
        print("\n" + "=" * 60)
        print("SETUP COMPLETE!")
        print("=" * 60)
        print("\nFiles created:")
        print("  - deployment_info.json (contract addresses)")
        print("  - test_proposals.json (5 test proposals)")
        print("\nNext steps:")
        print("  1. Review the test proposals in test_proposals.json")
        print("  2. Run the AI agent: python main.py")
        print("\nNote: This uses MOCK data for testing the agent logic.")
        print("For real deployment, compile and deploy the actual Solidity contracts.")
        
    except Exception as e:
        print(f"\nDeployment failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Ganache is running:")
        print("   ganache")
        print("2. Check that port 8545 is not blocked")
        print("3. Try restarting Ganache")

if __name__ == "__main__":
    main()