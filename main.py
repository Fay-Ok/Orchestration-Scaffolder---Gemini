import argparse
import sys
from pathlib import Path
from core.orchestrator import Orchestrator

def main():
    parser = argparse.ArgumentParser(
        description="AI-Powered Service Orchestration Scaffolder"
    )
    parser.add_argument(
        "requirements", 
        help="Path to the markdown requirements or user story file"
    )
    parser.add_argument(
        "--output", 
        default=".", 
        help="Target directory for generation (defaults to current directory)"
    )

    args = parser.parse_args()
    req_path = Path(args.requirements)

    if not req_path.exists():
        print(f"Error: Requirements file not found at {req_path}")
        sys.exit(1)

    orchestrator = Orchestrator(target_dir=Path(args.output))
    orchestrator.run(req_path)

if __name__ == "__main__":
    main()