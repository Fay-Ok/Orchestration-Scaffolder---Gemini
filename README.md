# Orchestration-Scaffolder---Gemini
This is multi agent scaffolder project using Gemini 

An AI-powered service orchestration platform that transforms markdown-based requirements into production-ready backend service scaffolds and deployment workflows.

## Project Overview

The Orchestration Scaffolder leverages a chain of specialized LLM-driven agents to automate the initial stages of the software development lifecycle (SDLC). By reducing the manual overhead of bootstrapping services, the project improves development velocity, ensures architectural consistency, and enhances documentation quality.

## Skills-Based Engineering Governance

To ensure deterministic and production-grade output, each agent is governed by a defined set of **Skills and Engineering Practices**. Rather than relying solely on model reasoning, agents are constrained by:
- **Standardized Templates:** Pre-approved boilerplate and directory structures.
- **Naming Conventions:** Enforced PascalCase, snake_case, or kebab-case across resources.
- **Security Guardrails:** Mandatory IAM least-privilege, encryption-by-default, secret management, and secure dependency selection (vulnerability-free selection with human-review triggers).
- **Validation Rules:** Automated checks to ensure output matches organizational schemas.
- **Interactive CLI Skills:** Ability to inspect requirements, identify missing parameters, and prompt the user for clarification before execution.

## CLI Workflow

The platform operates as a local developer tool:
1. **Initialization:** The user navigates to the target service directory.
2. **Execution:** The user runs the orchestrator, passing the path to a requirements markdown file.
3. **Clarification Loop:** Each agent scans the input. If mandatory fields (e.g., Service Name, AWS Region) are missing, the agent initiates a targeted CLI prompt.
4. **Deterministic Generation:** Once all inputs are satisfied (via spec, user input, or defaults), the agent generates the code and an audit trail of all decisions.

## Multi-Agent Architecture

The system utilizes a series of agents, each equipped with specific engineering skills:

1.  **Requirements Parser:** Extracts structured data and technical constraints using a strict JSON schema.
2.  **Domain Architect:** Defines service boundaries following Hexagonal or Clean Architecture patterns.
3.  **Scaffolding Engine:** Generates application code adhering to approved project structures and dependency rules.
4.  **Documentation Agent:** Populates a standard enterprise README template with technical specifics.
5.  **PR Explainer:** Generates an audit trail of user-provided values, defaulted values, and security assumptions, including flagged vulnerabilities requiring human review.
6.  **Validation Agent:** Runs smoke tests and basic validation checks on the generated output.
7.  **Terraform Agent (IaC):** Generates HCL using approved modules, tagging standards, and encryption defaults.

## Key Features (MVP)

- **Markdown-to-Code:** Direct translation of requirements to service structure.
- **Deployment Workflows:** Automated generation of basic deployment scripts.
- **Interactive IaC:** Terraform generation with intelligent default fallback and decision auditing.
- **Deterministic Generation:** Constrained LLM output through prompt-injected engineering standards.
- **Multi-Model Evaluation:** Comparative analysis of ChatGPT, Claude, and Gemini across metrics like:
    - Code generation quality.
    - Architectural reasoning.
    - Structured output reliability.
    - Enterprise readiness.

## Future Roadmap

- **Cloud Integration:** AWS SSM integration and certificate-based authentication.
- **CI/CD:** Automated pipeline creation for GitHub Actions/GitLab CI.
- **Orchestration:** Kubernetes deployment workflows and Helm chart generation.

## Getting Started

1. **Setup Environment:**
   Create a `.env` file in the root directory and add your Google Gemini API key:
   ```text
   GOOGLE_API_KEY=your_actual_key_here
   ```

2. **Run the Orchestrator:**
   Provide the path to the sample requirements file and a target output directory:
   ```bash
   python main.py sample_requirements.md --output ./TestPaymentService
   ```

---
*Built with Gemini Code Assist.*
