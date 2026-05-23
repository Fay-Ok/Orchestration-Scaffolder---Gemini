from pathlib import Path
from typing import Dict, Any
from core.agents.base_agent import BaseAgent
# Import specific agents here as we build them
from core.agents.requirements_parser_agent import RequirementsParserAgent
from core.agents.pr_explainer_agent import PRExplainerAgent
from core.agents.git_manager_agent import GitManagerAgent
from core.agent_skills import REQUIREMENTS_PARSER_SKILLS, PR_EXPLAINER_SKILLS, VCS_SKILLS
from core.llm_client import GeminiClient

class Orchestrator:
    def __init__(self, target_dir: Path):
        self.target_dir = target_dir
        self.llm_client = GeminiClient()
        self.global_context: Dict[str, Any] = {
            "target_directory": str(target_dir)
        }
        
        # Initialize the agent chain
        self.agents = [
            RequirementsParserAgent(REQUIREMENTS_PARSER_SKILLS, self.llm_client),
            GitManagerAgent(VCS_SKILLS),
            PRExplainerAgent(PR_EXPLAINER_SKILLS, self.llm_client)
        ]

    def run(self, requirements_path: Path):
        print(f"--- Starting Orchestration for: {requirements_path.name} ---")
        
        # 1. Load the requirements content
        with open(requirements_path, "r") as f:
            self.global_context["raw_requirements"] = f.read()

        # 2. Sequential Agent Execution
        # (In the next step, we'll initialize RequirementsParserAgent, etc.)
        for agent in self.agents:
            # Step A: Interactive Clarification
            self.global_context = agent.validate_and_clarify(self.global_context)
            
            # Step B: LLM Generation
            result = agent.execute(self.global_context)
            self.global_context.update(result)

        print("\n--- Orchestration Complete ---")