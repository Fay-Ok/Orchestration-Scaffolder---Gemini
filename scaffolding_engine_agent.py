import os
from typing import Dict, Any
from core.agents.base_agent import BaseAgent
from core.agent_skills import AgentSkill
from core.llm_client import GeminiClient

class ScaffoldingEngineAgent(BaseAgent):
    def __init__(self, skill: AgentSkill, llm_client: GeminiClient):
        super().__init__(skill)
        self.llm_client = llm_client

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        print(f"[*] {self.skill.agent_name} generating .NET 8.0 scaffold with Swagger...")
        
        system_instruction = f"""
        You are a Senior .NET Architect. Generate a production-ready C# Web API.
        Required: Enable Swagger UI (AddSwaggerGen, UseSwaggerUI) so it is visible on localhost.
        
        Standards: {self.skill.coding_standards}
        Output Schema: {self.skill.output_schema}
        """
        
        user_prompt = f"Service Name: {context.get('service_name')}. Endpoints: {context.get('endpoints')}."
        
        result = self.llm_client.generate_structured(system_instruction, user_prompt)
        
        # Write files to disk
        target_dir = context.get("target_directory", ".")
        files_created = []
        for file_info in result.get("files", []):
            path = os.path.join(target_dir, file_info['path'])
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(file_info['content'])
            files_created.append(file_info['path'])
            self.log_decision("file_created", file_info['path'], "ai_generated")

        return {
            "files_generated": files_created,
            "decisions": self.decisions
        }