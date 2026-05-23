from typing import Dict, Any
from core.agents.base_agent import BaseAgent
from core.agent_skills import AgentSkill
from core.llm_client import GeminiClient

class PRExplainerAgent(BaseAgent):
    def __init__(self, skill: AgentSkill, llm_client: GeminiClient):
        super().__init__(skill)
        self.llm_client = llm_client

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        print(f"[*] {self.skill.agent_name} is synthesizing the PR summary...")
        
        # Collect all decision logs and security alerts from previous steps
        decisions = context.get("decisions", [])
        security_alerts = context.get("security_alerts", [])
        files = context.get("files_generated", [])
        
        system_instruction = f"""
        You are a Staff Engineer. Your job is to write a Pull Request description for the generated code.
        
        Use the following inputs:
        - Decisions Log: {decisions}
        - Security Alerts: {security_alerts}
        - Files Created: {files}
        
        Structure your Markdown description with these sections:
        1. ## Executive Summary
        2. ## Technical Decisions (User vs Default Table)
        3. ## Security Audit & Compliance
        4. ## Files Changed
        
        Output MUST follow this JSON schema: {self.skill.output_schema}
        """
        
        result = self.llm_client.generate_structured(
            system_instruction=system_instruction,
            user_prompt="Summarize the service generation and infrastructure changes."
        )
        
        return result
