from typing import Any, Dict, List
from core.agent_skills import AgentSkill

class BaseAgent:
    def __init__(self, skill: AgentSkill):
        self.skill = skill
        self.decisions: List[Dict[str, Any]] = []

    def validate_and_clarify(self, current_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inspects the context for required fields. 
        Prompts the user via CLI if mandatory data is missing.
        """
        print(f"\n[*] {self.skill.agent_name} validating requirements...")
        updated_context = current_context.copy()

        for requirement in self.skill.required_inputs:
            if requirement not in updated_context or not updated_context[requirement]:
                # Check if we have a default
                if requirement in self.skill.default_values:
                    default_val = self.skill.default_values[requirement]
                    updated_context[requirement] = default_val
                    print(f"  - Using default for '{requirement}': {default_val}")
                else:
                    # Interactive Prompt
                    user_input = input(f"  - Missing mandatory field '{requirement}'. Please enter value: ")
                    while not user_input.strip():
                        user_input = input(f"    [!] {requirement} cannot be empty. Please enter value: ")
                    updated_context[requirement] = user_input.strip()
        
        return updated_context

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        To be implemented by specific agents (e.g., ScaffoldingEngine).
        Should call Gemini to generate content.
        """
        raise NotImplementedError("Agents must implement execute()")

    def log_decision(self, parameter: str, value: Any, source: str):
        """
        Helper to track decisions for the PR Explainer.
        Source should be 'user', 'default', or 'requirement_spec'.
        """
        self.decisions.append({"param": parameter, "val": value, "src": source})