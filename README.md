# Claude Skills

Portable [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills for use across projects and machines.

## What are skills?

Skills are markdown-based playbooks that transform Claude from a general-purpose agent into a specialized one. Each skill provides domain expertise, workflows, technical specs, and anti-patterns that produce expert-level output on the first attempt.

## Skills

| Skill | Description |
|-------|-------------|
| [app-store-screenshots](skills/app-store-screenshots/) | Build App Store screenshot pages with Next.js, export at all Apple-required resolutions |
| [skill-creator](skills/skill-creator/) | Create new skills with the enhanced patterns reference (Q&A gates, strong opinions, anti-patterns, etc.) |

## Installation

### Single skill (symlink into global skills)

```bash
# Clone once
git clone git@github.com:kjmagnan1s/claude-skills.git ~/Documents/GitHub/claude-skills

# Symlink a skill into your global Claude skills directory
ln -s ~/Documents/GitHub/claude-skills/skills/app-store-screenshots ~/.claude/skills/app-store-screenshots
```

### Single skill (symlink into a project)

```bash
# Symlink into a specific project's skills
ln -s ~/Documents/GitHub/claude-skills/skills/app-store-screenshots /path/to/project/.claude/skills/app-store-screenshots
```

### All skills

```bash
# Symlink everything at once
for skill in ~/Documents/GitHub/claude-skills/skills/*/; do
  name=$(basename "$skill")
  ln -sf "$skill" ~/.claude/skills/"$name"
done
```

### New machine setup

```bash
git clone git@github.com:kjmagnan1s/claude-skills.git ~/Documents/GitHub/claude-skills
# Then symlink whichever skills you need (see above)
```

## Adding a new skill

1. Create the skill directory under `skills/`
2. Add a `SKILL.md` with YAML frontmatter (`name`, `description`)
3. Add any `references/`, `scripts/`, or `assets/` as needed
4. Use the `skill-creator` skill to guide the process

## Updating skills across machines

```bash
cd ~/Documents/GitHub/claude-skills && git pull
```

Symlinked skills update automatically since they point to the repo files.
