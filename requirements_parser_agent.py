from typing import Dict, Any
from core.agents.base_agent import BaseAgent
from core.agent_skills import AgentSkill
from llm_client import GeminiClient

class RequirementsParserAgent(BaseAgent):
    def __init__(self, skill: AgentSkill, llm_client: GeminiClient):
        super().__init__(skill)
        self.llm_client = llm_client

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses the raw requirements using Gemini and the defined output schema.
        """
        print(f"[*] {self.skill.agent_name} is analyzing the specification...")
        
        system_instruction = f"""
        You are a Principal Technical Analyst. Your task is to parse a requirements document 
        and extract structured technical data.
        
        Strictly follow this JSON schema for your output:
        {self.skill.output_schema}
        """
        
        raw_reqs = context.get("raw_requirements", "")
        structured_data = self.llm_client.generate_structured(
            system_instruction=system_instruction,
            user_prompt=raw_reqs
        )
        
        return structured_data