import subprocess
from typing import Dict, Any
from core.agents.base_agent import BaseAgent
from core.agent_skills import AgentSkill

class GitManagerAgent(BaseAgent):
    def __init__(self, skill: AgentSkill):
        super().__init__(skill)

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        print(f"[*] {self.skill.agent_name} checking version control status...")
        target_dir = context.get("target_directory", ".")
        
        # 1. Check/Init Repo
        try:
            subprocess.check_output(["git", "rev-parse", "--is-inside-work-tree"], cwd=target_dir)
            print("  - Existing repository detected.")
        except subprocess.CalledProcessError:
            print("  - No repository found. Initializing...")
            subprocess.run(["git", "init"], cwd=target_dir)
            self.log_decision("git_init", True, "agent_action")

        # 2. Check/Set Remote
        remote_url = context.get("remote_url")
        try:
            subprocess.check_output(["git", "remote", "get-url", "origin"], cwd=target_dir)
        except subprocess.CalledProcessError:
            if remote_url:
                print(f"  - Setting remote origin: {remote_url}")
                subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=target_dir)
                self.log_decision("remote_origin", remote_url, "user_explicit")

        # 3. Branch Setup
        branch = context.get("branch_name", "main")
        subprocess.run(["git", "checkout", "-b", branch], cwd=target_dir)
        
        return {
            "repo_initialized": True,
            "remote_set": True if remote_url else False,
            "current_branch": branch
        }

    def _run_git(self, args: list, cwd: str):
        return subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)