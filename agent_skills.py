from pydantic import BaseModel, Field
from typing import List, Dict, Any

class AgentSkill(BaseModel):
    """Defines the engineering constraints and standards for a specific agent."""
    agent_name: str
    naming_conventions: Dict[str, str] = Field(description="Regex or patterns for naming (e.g., snake_case)")
    coding_standards: List[str] = Field(description="Coding rules (e.g., 'No global variables')")
    mandatory_security: List[str] = Field(description="Security requirements (e.g., 'IAM Least Privilege')")
    output_schema: Dict[str, Any] = Field(description="The JSON structure the agent must return")
    approved_templates: List[str] = Field(description="Paths to Jinja2 or standard text templates")
    required_inputs: List[str] = Field(description="Mandatory data points required before generation")
    default_values: Dict[str, Any] = Field(description="Fallbacks for non-mandatory missing inputs")
    interaction_rules: List[str] = Field(description="Guidelines for how to prompt the user via CLI")

# Example Definition for the Scaffolding Engine
SCAFFOLD_SKILLS = AgentSkill(
    agent_name="Scaffolding Engine",
    naming_conventions={
        "folders": "kebab-case",
        "files": "snake_case",
        "classes": "PascalCase"
    },
    coding_standards=[
        "Follow Hexagonal Architecture",
        "Use dependency injection for all services",
        "Interface-first design for internal APIs",
        "Follow SOLID principles and standard .NET Middleware patterns",
        "Use Global Exception Handling and Serilog for logging"
    ],
    mandatory_security=[
        "Sensitive data must be fetched via AWS SSM/Secrets Manager",
        "No hardcoded credentials in code",
        "Prioritize latest secure versions of dependencies; flag unavoidable vulnerabilities for human review."
    ],
    required_inputs=["service_name", "api_type", "target_directory"],
    default_values={
        "language": "C#",
        "framework": ".NET 8.0"
    },
    interaction_rules=[
        "Ask for service_name if missing from markdown.",
        "Confirm the target_directory if it differs from the current working directory."
    ],
    output_schema={
        "files": "List[Dict[str, str]]",
        "dependencies": "List[str]",
        "security_alerts": "List[Dict[str, str]]"
    },
    approved_templates=["templates/dotnet/Program.cs.j2", "templates/dotnet/appsettings.json.j2", "templates/dotnet/Project.csproj.j2"]
)

# Example Definition for the Terraform Agent
TERRAFORM_SKILLS = AgentSkill(
    agent_name="Terraform Agent",
    naming_conventions={
        "resource_names": "snake_case",
        "tags": "PascalCase"
    },
    coding_standards=[
        "Use approved organizational modules only",
        "Mandatory 'Environment' and 'Owner' tags"
    ],
    mandatory_security=[
        "S3 buckets must have public access blocks",
        "KMS encryption enabled for all storage resources",
        "IAM roles must utilize specialized trust policies"
    ],
    required_inputs=["aws_region", "environment"],
    default_values={
        "aws_region": "us-east-1",
        "environment": "dev",
        "enable_versioning": True,
        "encryption_enabled": True
    },
    interaction_rules=[
        "If 'bucket_name' is missing, suggest a name based on the service_name.",
        "Always ask for confirmation before applying non-standard region settings."
    ],
    output_schema={
        "hcl_content": "str",
        "audit_log": "str"
    },
    approved_templates=["templates/terraform/aws_s3.j2"]
)

# Definition for the PR Explainer Agent
PR_EXPLAINER_SKILLS = AgentSkill(
    agent_name="PR Explainer",
    naming_conventions={},
    coding_standards=[
        "Generate clear, concise technical summaries",
        "Use Markdown tables for decision transparency",
        "Highlight security implications and assumptions"
    ],
    mandatory_security=[
        "Must prominently flag any known vulnerabilities or IAM overrides",
        "Identify sensitive resources created (e.g., S3, Databases)"
    ],
    required_inputs=["decisions", "files_generated"],
    default_values={},
    interaction_rules=[
        "Ask for a custom PR prefix (e.g., JIRA-123) if not found in requirements."
    ],
    output_schema={
        "pr_title": "str",
        "pr_description_markdown": "str",
        "review_priority": "str (High/Medium/Low)",
        "labels": "List[str]"
    },
    approved_templates=[]
)

# Definition for the Git Manager Agent
VCS_SKILLS = AgentSkill(
    agent_name="Git Manager",
    naming_conventions={
        "branches": "feature/scaffold-*"
    },
    coding_standards=[
        "Ensure a .gitignore is present",
        "Create a clean initial commit",
        "Follow standard branch naming conventions"
    ],
    mandatory_security=[
        "Validate that no secrets are in the staging area"
    ],
    required_inputs=["remote_url"],
    default_values={"branch_name": "main"},
    interaction_rules=[
        "If .git is missing, ask: 'Initialize new Git repository in this folder?'",
        "Prompt for the Remote Origin URL to support PR generation."
    ],
    output_schema={
        "repo_initialized": "bool",
        "remote_set": "bool",
        "current_branch": "str"
    },
    approved_templates=[]
)