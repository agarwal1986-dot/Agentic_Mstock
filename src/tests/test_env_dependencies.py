"""
Dependency health check using packaging for proper version specifier handling.
"""

import os
import sys
import importlib.metadata
from packaging.requirements import Requirement
from packaging.version import Version

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
REQ_ALL = os.path.join(BASE_DIR, "requirements", "requirements-all.txt")

def load_requirements(file_path):
    """Recursively load requirements, resolving -r includes."""
    requirements = []
    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("-r"):
                include_path = os.path.join(os.path.dirname(file_path), line[2:].strip())
                requirements.extend(load_requirements(include_path))
            else:
                requirements.append(line)
    return requirements

def normalize_requirements(requirements):
    """Deduplicate by package name, keep the last specifier."""
    normalized = {}
    for req in requirements:
        try:
            parsed = Requirement(req)
            normalized[parsed.name.lower()] = parsed
        except Exception:
            # Skip invalid lines (like comments)
            continue
    return list(normalized.values())

def check_dependencies():
    errors = []
    requirements = normalize_requirements(load_requirements(REQ_ALL))

    for req in requirements:
        try:
            installed_version = Version(importlib.metadata.version(req.name))
            if installed_version not in req.specifier:
                errors.append(
                    f"{req.name}: required {req.specifier}, installed {installed_version}"
                )
        except importlib.metadata.PackageNotFoundError:
            errors.append(f"{req.name}: not installed")

    if errors:
        print("\n==============================")
        print("❌ ERROR: Dependency issues found")
        for e in errors:
            print(f"- {e}")
        print("==============================\n")
        sys.exit(1)
    else:
        print("\n==============================")
        print("✅ SUCCESS: All dependencies are satisfied")
        print("==============================\n")

if __name__ == "__main__":
    check_dependencies()