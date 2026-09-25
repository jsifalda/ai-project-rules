#!/usr/bin/env python3
"""
Quick validation script for skills - minimal version
"""

import sys
import os
import re
import yaml
from pathlib import Path

def validate_skill(skill_path, require_version=False):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read and validate frontmatter
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    # Define allowed properties
    # 'argument-hint' and 'disable-model-invocation' are Claude Code skill keys
    # (manual-invocation control, slash-arg hints); allowed so third-party skills
    # synced verbatim (e.g. via sync-mattpocock-skills) pass without mutation.
    ALLOWED_PROPERTIES = {
        'name', 'description', 'license', 'allowed-tools', 'metadata',
        'argument-hint', 'disable-model-invocation',
    }

    # Check for unexpected properties (excluding nested keys under metadata)
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required fields
    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Extract name for validation
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        # Check naming convention (hyphen-case: lowercase with hyphens)
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        # Check name length (max 64 characters per spec)
        if len(name) > 64:
            return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    # Extract and validate description
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        # Check for angle brackets
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)"
        # Check description length (max 1024 characters per spec)
        if len(description) > 1024:
            return False, f"Description is too long ({len(description)} characters). Maximum is 1024 characters."

    # Optional stricter checks for versioned skills (opt-in via --require-version)
    if require_version:
        metadata = frontmatter.get('metadata')
        if not isinstance(metadata, dict):
            return False, "metadata must be present and a YAML mapping when --require-version is set"

        version = metadata.get('version')
        if version is None:
            return False, "metadata.version is required when --require-version is set"
        if not isinstance(version, str):
            return False, (
                f"metadata.version must be a quoted string, e.g. version: \"1.0\" "
                f"(got {type(version).__name__}: {version!r} — quote it in YAML)"
            )
        if not re.match(r'^\d+\.\d+$', version):
            return False, f"metadata.version '{version}' must match X.Y (e.g. \"1.0\")"

        upstream = metadata.get('upstream')
        if upstream is not None:
            if not isinstance(upstream, str) or not upstream.startswith('https://'):
                return False, "metadata.upstream must be a string starting with 'https://'"

    return True, "Skill is valid!"

if __name__ == "__main__":
    require_version = '--require-version' in sys.argv[1:]
    positional = [a for a in sys.argv[1:] if a != '--require-version']
    if len(positional) != 1:
        print("Usage: python quick_validate.py <skill_directory> [--require-version]")
        sys.exit(1)

    valid, message = validate_skill(positional[0], require_version=require_version)
    print(message)
    sys.exit(0 if valid else 1)