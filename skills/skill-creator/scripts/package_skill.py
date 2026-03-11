#!/usr/bin/env python3
"""
Skill Packaging Script

Validates and packages a skill into a distributable zip file.

Validation checks:
- YAML frontmatter format and required fields
- Skill naming conventions
- Directory structure
- Description quality
- File organization

Usage:
    python package_skill.py <path/to/skill-folder>
    python package_skill.py <path/to/skill-folder> --output ./dist

Author: Claude Code skill-creator
Version: 1.0
"""

import os
import sys
import argparse
import zipfile
import re
from pathlib import Path
from typing import List, Tuple, Optional


class SkillValidator:
    """Validates skill structure and content."""

    def __init__(self, skill_path: Path):
        self.skill_path = skill_path
        self.skill_name = skill_path.name
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> bool:
        """Run all validation checks. Returns True if valid."""
        print(f"🔍 Validating skill: {self.skill_name}")
        print(f"📁 Path: {self.skill_path}")
        print()

        self._validate_directory_structure()
        self._validate_skill_md()
        self._validate_yaml_frontmatter()
        self._validate_description()
        self._check_todo_markers()
        self._check_file_organization()

        # Print results
        if self.warnings:
            print("⚠️  Warnings:")
            for warning in self.warnings:
                print(f"   - {warning}")
            print()

        if self.errors:
            print("❌ Validation failed with errors:")
            for error in self.errors:
                print(f"   - {error}")
            print()
            return False

        print("✅ Validation passed!")
        print()
        return True

    def _validate_directory_structure(self):
        """Check that skill has proper directory structure."""
        if not self.skill_path.exists():
            self.errors.append(f"Skill directory does not exist: {self.skill_path}")
            return

        if not self.skill_path.is_dir():
            self.errors.append(f"Skill path is not a directory: {self.skill_path}")
            return

        # Check for SKILL.md
        skill_md = self.skill_path / 'SKILL.md'
        if not skill_md.exists():
            self.errors.append("Missing required file: SKILL.md")

    def _validate_skill_md(self):
        """Validate SKILL.md content."""
        skill_md = self.skill_path / 'SKILL.md'
        if not skill_md.exists():
            return  # Already reported in directory validation

        try:
            content = skill_md.read_text()

            # Check minimum length
            if len(content) < 200:
                self.warnings.append("SKILL.md is very short (< 200 characters)")

            # Check for basic structure
            if '## Purpose' not in content and '## When to Use' not in content:
                self.warnings.append("SKILL.md should include '## Purpose' or '## When to Use' sections")

        except Exception as e:
            self.errors.append(f"Error reading SKILL.md: {e}")

    def _validate_yaml_frontmatter(self):
        """Validate YAML frontmatter in SKILL.md."""
        skill_md = self.skill_path / 'SKILL.md'
        if not skill_md.exists():
            return

        try:
            content = skill_md.read_text()

            # Check for frontmatter
            if not content.startswith('---'):
                self.errors.append("SKILL.md must start with YAML frontmatter (---)")
                return

            # Extract frontmatter
            parts = content.split('---', 2)
            if len(parts) < 3:
                self.errors.append("SKILL.md has incomplete YAML frontmatter (missing closing ---)")
                return

            frontmatter = parts[1].strip()

            # Check for required fields
            if 'name:' not in frontmatter:
                self.errors.append("YAML frontmatter missing required field: name")

            if 'description:' not in frontmatter:
                self.errors.append("YAML frontmatter missing required field: description")

            # Extract name and validate
            name_match = re.search(r'name:\s*(.+)', frontmatter)
            if name_match:
                yaml_name = name_match.group(1).strip()
                if yaml_name != self.skill_name:
                    self.warnings.append(
                        f"YAML name '{yaml_name}' doesn't match directory name '{self.skill_name}'"
                    )

        except Exception as e:
            self.errors.append(f"Error validating YAML frontmatter: {e}")

    def _validate_description(self):
        """Validate description quality."""
        skill_md = self.skill_path / 'SKILL.md'
        if not skill_md.exists():
            return

        try:
            content = skill_md.read_text()
            desc_match = re.search(r'description:\s*(.+)', content)

            if desc_match:
                description = desc_match.group(1).strip()

                # Check length
                if len(description) < 20:
                    self.warnings.append("Description is very short (< 20 characters)")

                if len(description) > 300:
                    self.warnings.append("Description is very long (> 300 characters)")

                # Check for TODO
                if 'TODO' in description.upper():
                    self.errors.append("Description still contains TODO placeholder")

                # Check for third-person language
                if description.lower().startswith(('use this', 'this skill helps you')):
                    self.warnings.append(
                        "Description should use third-person (e.g., 'This skill should be used when...')"
                    )

                # Check specificity
                vague_terms = ['helps with', 'assists with', 'provides help']
                if any(term in description.lower() for term in vague_terms):
                    self.warnings.append("Description could be more specific about use cases and triggers")

        except Exception as e:
            self.errors.append(f"Error validating description: {e}")

    def _check_todo_markers(self):
        """Check for TODO markers in SKILL.md."""
        skill_md = self.skill_path / 'SKILL.md'
        if not skill_md.exists():
            return

        try:
            content = skill_md.read_text()
            todo_count = content.upper().count('TODO')

            if todo_count > 0:
                self.warnings.append(f"SKILL.md contains {todo_count} TODO marker(s) - consider completing them")

        except Exception as e:
            self.errors.append(f"Error checking TODO markers: {e}")

    def _check_file_organization(self):
        """Check file organization and structure."""
        # Check for common directories
        scripts_dir = self.skill_path / 'scripts'
        references_dir = self.skill_path / 'references'
        assets_dir = self.skill_path / 'assets'

        # Check if directories exist but are empty
        for dir_name, dir_path in [
            ('scripts', scripts_dir),
            ('references', references_dir),
            ('assets', assets_dir)
        ]:
            if dir_path.exists():
                # Check if empty (only . and .. or no files)
                files = list(dir_path.iterdir())
                non_hidden = [f for f in files if not f.name.startswith('.')]

                if not non_hidden:
                    self.warnings.append(f"{dir_name}/ directory exists but is empty - consider removing if unused")

        # Check for example files that should be deleted
        example_files = [
            'scripts/example_script.py',
            'references/example_reference.md',
            'assets/README.md'
        ]

        for example_file in example_files:
            example_path = self.skill_path / example_file
            if example_path.exists():
                self.warnings.append(f"Example file still present: {example_file} - consider replacing or removing")


def package_skill(skill_path: Path, output_dir: Optional[Path] = None) -> Path:
    """
    Package skill into a zip file.

    Args:
        skill_path: Path to skill directory
        output_dir: Optional output directory (defaults to current directory)

    Returns:
        Path to created zip file
    """
    skill_name = skill_path.name
    output_dir = output_dir or Path.cwd()
    output_dir.mkdir(parents=True, exist_ok=True)

    zip_path = output_dir / f"{skill_name}.zip"

    print(f"📦 Packaging skill: {skill_name}")
    print(f"📁 Output: {zip_path}")
    print()

    # Create zip file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk the skill directory
        file_count = 0
        for root, dirs, files in os.walk(skill_path):
            # Skip hidden directories and __pycache__
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']

            for file in files:
                # Skip hidden files and Python cache
                if file.startswith('.') or file.endswith('.pyc'):
                    continue

                file_path = Path(root) / file
                arcname = file_path.relative_to(skill_path.parent)

                zipf.write(file_path, arcname)
                file_count += 1
                print(f"  ✅ Added: {arcname}")

    print()
    print(f"✅ Packaged {file_count} files")
    print(f"📦 Zip file: {zip_path}")
    print(f"📊 Size: {zip_path.stat().st_size:,} bytes")

    return zip_path


def main():
    parser = argparse.ArgumentParser(
        description='Validate and package a Claude Code skill',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s .claude/skills/my-skill
  %(prog)s .claude/skills/legal-assistant --output ./dist
  %(prog)s ~/projects/custom-skill --output ~/Desktop
        """
    )

    parser.add_argument(
        'skill_path',
        type=Path,
        help='Path to skill directory to package'
    )

    parser.add_argument(
        '--output',
        '-o',
        type=Path,
        default=None,
        help='Output directory for zip file (default: current directory)'
    )

    parser.add_argument(
        '--skip-validation',
        action='store_true',
        help='Skip validation and package anyway (not recommended)'
    )

    args = parser.parse_args()

    # Validate skill path
    if not args.skill_path.exists():
        print(f"❌ Error: Skill directory does not exist: {args.skill_path}")
        sys.exit(1)

    # Validate skill
    if not args.skip_validation:
        validator = SkillValidator(args.skill_path)
        if not validator.validate():
            print()
            print("❌ Validation failed. Fix errors and try again.")
            print("   Or use --skip-validation to package anyway (not recommended)")
            sys.exit(1)

    # Package skill
    try:
        print()
        zip_path = package_skill(args.skill_path, args.output)
        print()
        print("=" * 70)
        print(f"✨ Success! Skill packaged successfully.")
        print("=" * 70)
        print()
        print("📦 Distribution file:", zip_path)
        print()
        print("To install this skill:")
        print(f"  1. Unzip {zip_path.name}")
        print("  2. Move the skill directory to .claude/skills/")
        print("  3. Restart Claude Code or reload skills")
        print()

    except Exception as e:
        print(f"❌ Error packaging skill: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
