import subprocess
from typing import Dict, Any
from core.agents.base_agent import BaseAgent
from core.agent_skills import AgentSkill

class ValidationAgent(BaseAgent):
    def __init__(self, skill: AgentSkill):
        super().__init__(skill)

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        print(f"[*] {self.skill.agent_name} running smoke tests (dotnet build)...")
        target_dir = context.get("target_directory", ".")
        
        try:
            # Attempt to build the generated .NET project
            build_output = subprocess.check_output(
                ["dotnet", "build"], cwd=target_dir, stderr=subprocess.STDOUT, text=True
            )
            print("  - Build Successful.")
            self.log_decision("smoke_test", "Passed", "agent_action")
            return {"build_status": "Success", "validation_logs": build_output}
        except subprocess.CalledProcessError as e:
            print("  - Build Failed!")
            self.log_decision("smoke_test", "Failed", "agent_action")
            return {
                "build_status": "Failure",
                "validation_logs": e.output,
                "security_alerts": [{"type": "BuildError", "details": "Generated code failed to compile."}]
            }