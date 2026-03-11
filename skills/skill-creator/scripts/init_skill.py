#!/usr/bin/env python3
"""
Skill Initialization Script

Creates a new skill directory with proper structure:
- SKILL.md with YAML frontmatter template
- scripts/, references/, and assets/ directories
- Example files to demonstrate structure

Usage:
    python init_skill.py <skill-name> --path <output-directory>
    python init_skill.py my-new-skill --path .claude/skills/

Author: Claude Code skill-creator
Version: 1.0
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime


def create_skill_structure(skill_name: str, output_path: str) -> None:
    """
    Create a new skill directory with all necessary files and structure.

    Args:
        skill_name: Name of the skill (will be used for directory name)
        output_path: Parent directory where skill folder will be created
    """
    # Validate skill name
    if not skill_name.replace('-', '').replace('_', '').isalnum():
        print(f"❌ Error: Skill name must be alphanumeric (with hyphens/underscores allowed)")
        print(f"   Invalid name: '{skill_name}'")
        sys.exit(1)

    # Create paths
    skill_path = Path(output_path) / skill_name

    # Check if skill already exists
    if skill_path.exists():
        print(f"❌ Error: Skill directory already exists: {skill_path}")
        print(f"   Choose a different name or delete the existing directory.")
        sys.exit(1)

    print(f"🚀 Creating new skill: {skill_name}")
    print(f"📁 Output path: {skill_path}")
    print()

    # Create main skill directory
    skill_path.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created: {skill_path}/")

    # Create subdirectories
    subdirs = ['scripts', 'references', 'assets']
    for subdir in subdirs:
        subdir_path = skill_path / subdir
        subdir_path.mkdir(exist_ok=True)
        print(f"✅ Created: {skill_path}/{subdir}/")

    # Create SKILL.md
    skill_md_content = f"""---
name: {skill_name}
description: TODO - Describe what this skill does and when it should be used. Be specific about the use cases and triggers. Use third-person (e.g., "This skill should be used when...").
---

# {skill_name.replace('-', ' ').title()} Skill

## Purpose

TODO: Explain the purpose of this skill in 2-3 sentences.

This skill helps with [TASK/DOMAIN]. It provides [WHAT IT PROVIDES] to enable [GOAL/OUTCOME].

## When to Use This Skill

Activate this skill when:
- TODO: List specific scenarios or user requests that should trigger this skill
- TODO: Be concrete about what the user might say or ask
- TODO: Include edge cases if relevant

## Workflow

### Step 1: [First Step Name]

TODO: Describe the first step in detail.

- What information needs to be gathered?
- What validation should be performed?
- What tools or resources are needed?

### Step 2: [Second Step Name]

TODO: Describe the second step.

### Step 3: [Third Step Name]

TODO: Continue with additional steps as needed.

## Using Bundled Resources

### Scripts (scripts/)

TODO: If this skill includes scripts, document them here:

- `scripts/example_script.py` - Description of what this script does
  - Usage: `python scripts/example_script.py <args>`
  - Purpose: Explain when and why to use this script

### References (references/)

TODO: If this skill includes reference documents, document them here:

- `references/example_reference.md` - Description of reference material
  - Contains: What information is in this file
  - Use for: When to consult this reference

### Assets (assets/)

TODO: If this skill includes assets, document them here:

- `assets/example_template.txt` - Description of asset
  - Purpose: How this asset is used in outputs
  - Customization: What can be customized

## Examples

### Example 1: [Use Case Name]

**User Request:** "[Example user request]"

**Workflow:**
1. [Step taken]
2. [Step taken]
3. [Result]

### Example 2: [Another Use Case]

**User Request:** "[Another example]"

**Workflow:**
1. [Step taken]
2. [Step taken]
3. [Result]

## Best Practices

TODO: List best practices for using this skill:

- ✅ Do this
- ✅ Do that
- ❌ Don't do this
- ❌ Avoid that

## Error Handling

TODO: Document common errors and how to handle them:

**Error:** [Error description]
**Solution:** [How to resolve]

## Limitations

TODO: Document what this skill does NOT do:

- ❌ Does not handle [X]
- ❌ Not suitable for [Y]
- ⚠️ Requires [Z] to function

## Notes

TODO: Add any additional notes, tips, or considerations.

---

**Created:** {datetime.now().strftime('%Y-%m-%d')}
**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
**Version:** 1.0
"""

    skill_md_path = skill_path / 'SKILL.md'
    skill_md_path.write_text(skill_md_content)
    print(f"✅ Created: {skill_path}/SKILL.md")

    # Create example script
    example_script_content = """#!/usr/bin/env python3
\"\"\"
Example Script for {skill_name}

This is a placeholder script to demonstrate the scripts/ directory structure.
Delete this file and add your own scripts as needed.

Usage:
    python scripts/example_script.py [args]
\"\"\"

def main():
    print("This is an example script for {skill_name}")
    print("Replace this with your actual script logic.")

if __name__ == "__main__":
    main()
""".format(skill_name=skill_name)

    example_script_path = skill_path / 'scripts' / 'example_script.py'
    example_script_path.write_text(example_script_content)
    print(f"✅ Created: {skill_path}/scripts/example_script.py")

    # Create example reference
    example_reference_content = f"""# Example Reference for {skill_name.replace('-', ' ').title()}

This is a placeholder reference document to demonstrate the references/ directory structure.

## Purpose

Reference documents contain detailed information that Claude can load into context
when needed. This keeps the main SKILL.md concise while providing deep knowledge
on specific topics.

## When to Use References

- Database schemas
- API documentation
- Domain-specific knowledge
- Company policies
- Detailed workflow guides
- Examples and templates (in markdown format)

## Structure

Organize reference documents by topic:

### Topic 1: [Name]

Detailed information about topic 1...

### Topic 2: [Name]

Detailed information about topic 2...

## Best Practices

- Keep each reference focused on a single topic
- Use clear headings and structure
- Include examples where helpful
- Link to external resources when appropriate
- Update regularly as information changes

---

**Note:** Delete this example file and create your own reference documents as needed.
"""

    example_reference_path = skill_path / 'references' / 'example_reference.md'
    example_reference_path.write_text(example_reference_content)
    print(f"✅ Created: {skill_path}/references/example_reference.md")

    # Create example asset README
    example_asset_content = f"""# Assets for {skill_name.replace('-', ' ').title()}

This directory contains files that are used in the skill's outputs, but are not
meant to be loaded into Claude's context.

## What Goes in Assets

- Templates (HTML, Word docs, PDFs, etc.)
- Images (logos, icons, diagrams)
- Fonts
- Boilerplate code
- Sample documents
- Any files that will be copied, modified, or referenced in outputs

## What Doesn't Go in Assets

- Documentation (use references/ instead)
- Scripts/code to be executed (use scripts/ instead)
- Configuration files (put in root of skill directory)

## Examples

Good asset examples:
- `logo.png` - Company logo for branded documents
- `template.docx` - Word template for reports
- `boilerplate.html` - HTML starter template
- `style.css` - CSS stylesheet for web outputs

## Usage in SKILL.md

Document your assets in the main SKILL.md file so Claude knows when and how to use them.

---

**Note:** Delete this README and add your actual asset files as needed.
"""

    example_asset_path = skill_path / 'assets' / 'README.md'
    example_asset_path.write_text(example_asset_content)
    print(f"✅ Created: {skill_path}/assets/README.md")

    # Create .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual environments
venv/
env/
ENV/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.bak
.~*
"""

    gitignore_path = skill_path / '.gitignore'
    gitignore_path.write_text(gitignore_content)
    print(f"✅ Created: {skill_path}/.gitignore")

    print()
    print("=" * 70)
    print(f"✨ Skill '{skill_name}' created successfully!")
    print("=" * 70)
    print()
    print("📝 Next Steps:")
    print()
    print(f"1. Edit {skill_path}/SKILL.md:")
    print("   - Replace all TODO items with actual content")
    print("   - Update the description in YAML frontmatter")
    print("   - Document your workflow and examples")
    print()
    print(f"2. Add your resources:")
    print(f"   - Scripts:     {skill_path}/scripts/")
    print(f"   - References:  {skill_path}/references/")
    print(f"   - Assets:      {skill_path}/assets/")
    print()
    print("3. Delete example files you don't need:")
    print("   - scripts/example_script.py")
    print("   - references/example_reference.md")
    print("   - assets/README.md")
    print()
    print("4. Test your skill with Claude Code")
    print()
    print("5. Package for distribution (optional):")
    print(f"   python scripts/package_skill.py {skill_path}")
    print()
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description='Initialize a new Claude Code skill with proper structure',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s my-skill --path .claude/skills/
  %(prog)s legal-assistant --path ~/projects/my-app/.claude/skills/
  %(prog)s data-analyzer --path ./skills/
        """
    )

    parser.add_argument(
        'skill_name',
        help='Name of the skill (alphanumeric with hyphens/underscores)'
    )

    parser.add_argument(
        '--path',
        default='.claude/skills/',
        help='Parent directory where skill folder will be created (default: .claude/skills/)'
    )

    args = parser.parse_args()

    try:
        create_skill_structure(args.skill_name, args.path)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
