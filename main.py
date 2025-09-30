"""
AI Agent for DAO Governance - Works with local testing
"""

import json
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import re
import matplotlib.pyplot as plt
import numpy as np
from web3 import Web3
from eth_account import Account

class VoteChoice(Enum):
    """Vote options"""
    FOR = 1
    AGAINST = 2
    ABSTAIN = 3

@dataclass
class Proposal:
    """Represents a DAO proposal"""
    id: int
    title: str
    description: str
    proposer: str
    votes_for: int = 0
    votes_against: int = 0
    votes_abstain: int = 0
    executed: bool = False

@dataclass
class VotingMetrics:
    """Transparent metrics for automated voting decisions"""
    treasury_impact_weight: float = 0.3
    community_alignment_weight: float = 0.25
    technical_feasibility_weight: float = 0.25
    risk_assessment_weight: float = 0.2
    min_score_to_support: float = 0.6
    max_treasury_spend_pct: float = 0.1

class DAOGovernanceAgent:
    """AI Agent for automated DAO governance participation"""
    
    def __init__(
        self,
        metrics: Optional[VotingMetrics] = None,
        use_mock_data: bool = True,
        web3_provider: str = 'http://127.0.0.1:8545',
        ai_agent_key: str = None
    ):
        self.metrics = metrics or VotingMetrics()
        self.use_mock_data = use_mock_data
        self.voting_history: List[Dict] = []
        self.analyses: List[Dict] = []
        
        if not use_mock_data:
            try:
                self.w3 = Web3(Web3.HTTPProvider(web3_provider))
                self.ai_agent = Account.from_key(ai_agent_key)
                print(f"Connected to Web3: {web3_provider}")
                print(f"AI Agent Address: {self.ai_agent.address}")
                balance = self.w3.eth.get_balance(self.ai_agent.address)
                print(f"AI Agent Balance: {self.w3.from_wei(balance, 'ether')} ETH")
            except Exception as e:
                print(f"ERROR: Failed to connect to Web3 provider: {e}")
                raise e
        
        print("✓ DAO Agent initialized")
        print(f"  Mode: {'MOCK DATA (Testing)' if use_mock_data else 'BLOCKCHAIN'}")
        print(f"  Metrics: {self._format_metrics()}")

    def _format_metrics(self) -> str:
        return f"Treasury={self.metrics.treasury_impact_weight:.0%}, " \
               f"Community={self.metrics.community_alignment_weight:.0%}, " \
               f"Technical={self.metrics.technical_feasibility_weight:.0%}, " \
               f"Risk={self.metrics.risk_assessment_weight:.0%}"

    def load_proposals_from_file(self, filename: str = 'test_proposals.json') -> List[Proposal]:
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            proposals = []
            for p in data:
                proposals.append(Proposal(
                    id=p['id'],
                    title=p['title'],
                    description=p['description'],
                    proposer=p['proposer'],
                    votes_for=p.get('votesFor', 0),
                    votes_against=p.get('votesAgainst', 0),
                    votes_abstain=p.get('votesAbstain', 0),
                    executed=p.get('executed', False)
                ))
            print(f"\n✓ Loaded {len(proposals)} proposals from {filename}")
            return proposals
        except FileNotFoundError:
            print(f"\nERROR: {filename} not found!")
            print("Run deployment_testing.py first to create test data.")
            return []
        except Exception as e:
            print(f"\nERROR loading proposals: {e}")
            return []

    def monitor_proposals(self) -> List[Proposal]:
        if self.use_mock_data:
            return self.load_proposals_from_file()
        else:
            print("Fetching proposals from blockchain...")
            return []

    def analyze_proposal(self, proposal: Proposal) -> Dict:
        print(f"\n{'='*60}")
        print(f"📋 Analyzing Proposal #{proposal.id}")
        print(f"{'='*60}")
        print(f"Title: {proposal.title}")
        print(f"Proposer: {proposal.proposer}")
        
        analysis = {
            "proposal_id": proposal.id,
            "title": proposal.title,
            "scores": {},
            "overall_score": 0.0,
            "recommendation": VoteChoice.ABSTAIN,
            "reasoning": [],
            "summary": ""
        }
        
        treasury_score = self._analyze_treasury_impact(proposal)
        analysis["scores"]["treasury_impact"] = treasury_score
        print(f"  💰 Treasury Impact: {treasury_score:.2f}")
        
        alignment_score = self._analyze_community_alignment(proposal)
        analysis["scores"]["community_alignment"] = alignment_score
        print(f"  👥 Community Alignment: {alignment_score:.2f}")
        
        technical_score = self._analyze_technical_feasibility(proposal)
        analysis["scores"]["technical_feasibility"] = technical_score
        print(f"  🔧 Technical Feasibility: {technical_score:.2f}")
        
        risk_score = self._analyze_risk(proposal)
        analysis["scores"]["risk_assessment"] = risk_score
        print(f"  ⚠️  Risk Assessment: {risk_score:.2f}")
        
        overall = (
            treasury_score * self.metrics.treasury_impact_weight +
            alignment_score * self.metrics.community_alignment_weight +
            technical_score * self.metrics.technical_feasibility_weight +
            risk_score * self.metrics.risk_assessment_weight
        )
        analysis["overall_score"] = overall
        
        if overall >= self.metrics.min_score_to_support:
            analysis["recommendation"] = VoteChoice.FOR
            analysis["reasoning"].append(
                f"Score {overall:.2f} exceeds threshold {self.metrics.min_score_to_support}"
            )
        elif overall < 0.4:
            analysis["recommendation"] = VoteChoice.AGAINST
            analysis["reasoning"].append(
                f"Score {overall:.2f} is below 0.4 threshold"
            )
        else:
            analysis["reasoning"].append(
                f"Score {overall:.2f} is neutral (0.4 to {self.metrics.min_score_to_support})"
            )
        
        print(f"\n  📊 OVERALL SCORE: {overall:.2f}")
        print(f"  🗳️  RECOMMENDATION: {analysis['recommendation'].name}")
        print(f"  💭 Reasoning: {analysis['reasoning'][0]}")
        
        self.analyses.append(analysis)
        return analysis

    def _analyze_treasury_impact(self, proposal: Proposal) -> float:
        desc = proposal.description.lower()
        has_cost = any(word in desc for word in ['spend', 'cost', 'budget', 'fund', 'eth', 'token'])
        if not has_cost:
            return 0.8
        numbers = re.findall(r'\b\d+(?:,\d{3})*(?:\.\d+)?\b', desc)
        if numbers:
            max_num = max(float(n.replace(',', '')) for n in numbers)
            if max_num > 50:
                return 0.3
            elif max_num > 20:
                return 0.6
            else:
                return 0.8
        return 0.5

    def _analyze_community_alignment(self, proposal: Proposal) -> float:
        desc = proposal.description.lower()
        positive = ['community', 'decentralized', 'transparent', 'education', 
                   'growth', 'sustainable', 'public', 'open source']
        negative = ['centralized', 'exclusive', 'private', 'restricted']
        pos_count = sum(1 for kw in positive if kw in desc)
        neg_count = sum(1 for kw in negative if kw in desc)
        score = 0.5 + (pos_count * 0.08) - (neg_count * 0.15)
        return max(0.0, min(1.0, score))

    def _analyze_technical_feasibility(self, proposal: Proposal) -> float:
        desc = proposal.description
        word_count = len(desc.split())
        has_structure = any(m in desc for m in ['##', '###', '1.', '2.', '-'])
        has_timeline = any(w in desc.lower() for w in ['week', 'month', 'timeline', 'phase'])
        has_budget = 'budget' in desc.lower()
        has_technical = any(w in desc.lower() for w in ['contract', 'audit', 'test', 'develop'])
        score = 0.2
        if word_count > 150:
            score += 0.2
        if has_structure:
            score += 0.2
        if has_timeline:
            score += 0.15
        if has_budget:
            score += 0.15
        if has_technical:
            score += 0.1
        return min(1.0, score)

    def _analyze_risk(self, proposal: Proposal) -> float:
        desc = proposal.description.lower()
        title = proposal.title.lower()
        high_risk = ['risky', 'experimental', 'untested', 'no audit', 'instant', 'immediately']
        medium_risk = ['new', 'change', 'modify', 'remove']
        low_risk = ['audit', 'tested', 'proven', 'standard', 'established']
        score = 0.6
        for kw in high_risk:
            if kw in desc or kw in title:
                score -= 0.2
        for kw in medium_risk:
            if kw in desc or kw in title:
                score -= 0.05
        for kw in low_risk:
            if kw in desc:
                score += 0.1
        return max(0.0, min(1.0, score))

    def cast_vote(self, proposal_id: int, vote: VoteChoice, dry_run: bool = True) -> Dict:
        vote_record = {
            "timestamp": int(time.time()),
            "proposal_id": proposal_id,
            "vote": vote.name,
            "dry_run": dry_run
        }
        self.voting_history.append(vote_record)
        if dry_run or self.use_mock_data:
            print(f"\n  [DRY RUN] Vote recorded: {vote.name}")
        else:
            print(f"\n  ✓ Vote submitted to blockchain: {vote.name}")
        return vote_record

    def generate_charts(self):
        if not self.analyses or not self.voting_history:
            print("\n⚠️ No analysis data available for charts. Run governance cycle first.")
            return
        
        labels = [f"Proposal #{a['proposal_id']}" for a in self.analyses]
        
        # 1. Proposal Analysis Scores (Bar Chart)
        plt.figure(figsize=(10, 6))
        x = np.arange(len(labels))
        width = 0.2
        plt.bar(x - 0.3, [a["scores"]["treasury_impact"] for a in self.analyses], width, label='Treasury Impact', color='#4BC0C0')
        plt.bar(x - 0.1, [a["scores"]["community_alignment"] for a in self.analyses], width, label='Community Alignment', color='#36A2EB')
        plt.bar(x + 0.1, [a["scores"]["technical_feasibility"] for a in self.analyses], width, label='Technical Feasibility', color='#FFCE56')
        plt.bar(x + 0.3, [a["scores"]["risk_assessment"] for a in self.analyses], width, label='Risk Assessment', color='#FF6384')
        plt.xlabel('Proposals')
        plt.ylabel('Score (0-1)')
        plt.title('Proposal Analysis Scores by Category')
        plt.xticks(x, labels)
        plt.legend()
        plt.ylim(0, 1)
        plt.tight_layout()
        plt.show()

        # 2. Overall Scores with Threshold (Bar Chart)
        plt.figure(figsize=(10, 6))
        plt.bar(labels, [a["overall_score"] for a in self.analyses], color='#9966FF')
        plt.axhline(y=self.metrics.min_score_to_support, color='r', linestyle='--', label=f'Min Score to Support ({self.metrics.min_score_to_support})')
        plt.xlabel('Proposals')
        plt.ylabel('Overall Score (0-1)')
        plt.title('Overall Proposal Scores with Voting Threshold')
        plt.legend()
        plt.ylim(0, 1)
        plt.tight_layout()
        plt.show()

        # 3. Voting Summary (Pie Chart)
        for_count = sum(1 for v in self.voting_history if v['vote'] == 'FOR')
        against_count = sum(1 for v in self.voting_history if v['vote'] == 'AGAINST')
        abstain_count = sum(1 for v in self.voting_history if v['vote'] == 'ABSTAIN')
        plt.figure(figsize=(8, 8))
        plt.pie([for_count, against_count, abstain_count], labels=['FOR', 'AGAINST', 'ABSTAIN'], 
                colors=['#4BC0C0', '#FF6384', '#FFCE56'], autopct='%1.1f%%')
        plt.title('Voting Summary Distribution')
        plt.tight_layout()
        plt.show()

    def run_governance_cycle(self, dry_run: bool = True):
        print("\n" + "="*60)
        print("🤖 DAO GOVERNANCE AGENT - Starting Analysis Cycle")
        print("="*60)
        print(f"Mode: {'DRY RUN (No blockchain transactions)' if dry_run else 'LIVE'}")
        
        self.analyses = []
        proposals = self.monitor_proposals()
        
        if not proposals:
            print("\n⚠️  No proposals found to analyze.")
            print("Run 'python deployment_testing.py' first!")
            return
        
        for proposal in proposals:
            analysis = self.analyze_proposal(proposal)
            self.cast_vote(proposal.id, analysis['recommendation'], dry_run)
            time.sleep(1)
        
        print("\n" + "="*60)
        print("✓ Governance Cycle Complete")
        print("="*60)
        self.print_summary()
        self.generate_charts()

    def print_summary(self):
        if not self.voting_history:
            print("\nNo votes cast yet.")
            return
        
        print(f"\n📊 VOTING SUMMARY")
        print(f"{'='*60}")
        print(f"Total Votes: {len(self.voting_history)}")
        
        for_count = sum(1 for v in self.voting_history if v['vote'] == 'FOR')
        against_count = sum(1 for v in self.voting_history if v['vote'] == 'AGAINST')
        abstain_count = sum(1 for v in self.voting_history if v['vote'] == 'ABSTAIN')
        
        print(f"  FOR: {for_count}")
        print(f"  AGAINST: {against_count}")
        print(f"  ABSTAIN: {abstain_count}")
        
        print(f"\n📝 Vote History:")
        for vote in self.voting_history:
            print(f"  Proposal #{vote['proposal_id']}: {vote['vote']}")

    def export_metrics(self) -> Dict:
        return {
            "treasury_impact_weight": self.metrics.treasury_impact_weight,
            "community_alignment_weight": self.metrics.community_alignment_weight,
            "technical_feasibility_weight": self.metrics.technical_feasibility_weight,
            "risk_assessment_weight": self.metrics.risk_assessment_weight,
            "min_score_to_support": self.metrics.min_score_to_support,
            "max_treasury_spend_pct": self.metrics.max_treasury_spend_pct
        }

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║        DAO GOVERNANCE AI AGENT - ANALYSIS MODE           ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    custom_metrics = VotingMetrics(
        treasury_impact_weight=0.35,
        community_alignment_weight=0.30,
        technical_feasibility_weight=0.20,
        risk_assessment_weight=0.15,
        min_score_to_support=0.65
    )
    
    agent = DAOGovernanceAgent(
        metrics=custom_metrics,
        use_mock_data=True,
        web3_provider='http://127.0.0.1:8545',
        ai_agent_key='0x5eee54068ea1532a9b39b420e30a090731bbd655d272eeade42d9e9ecf466c90'
    )
    
    print("\n📊 Agent Configuration:")
    print(json.dumps(agent.export_metrics(), indent=2))
    
    agent.run_governance_cycle(dry_run=True)
    
    print("\n✓ Analysis complete!")
    print("\nTo run with real blockchain:")
    print("  1. Deploy actual contracts")
    print("  2. Update use_mock_data=False")
    print("  3. Implement Web3 contract interactions in monitor_proposals and cast_vote")