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

# Definition for the Requirements Parser
REQUIREMENTS_PARSER_SKILLS = AgentSkill( # This is the correct one to modify
    agent_name="Requirements Parser",
    naming_conventions={},
    coding_standards=[
        "Extract objective technical constraints",
        "Identify explicit service names and domain boundaries",
        "Expect structured markdown input following predefined sections (e.g., Service Name, Endpoints, Infrastructure)",
        "Prioritize explicit declarations over inferred values"
    ],
    mandatory_security=[
        "Identify any mentioned compliance requirements (PII, HIPAA, etc.)"
    ],
    required_inputs=[],
    default_values={},
    interaction_rules=[
        "If the markdown is empty or unreadable, ask the user to provide a valid path."
    ],
    output_schema={
        "service_name": "str",
        "api_type": "str (REST/GraphQL/gRPC)",
        "description": "str",
        "endpoints": "List[Dict[str, str]]",
        "infrastructure_requirements": "List[str]",
        "dependencies": "List[str]"
    },
    approved_templates=[]
)

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