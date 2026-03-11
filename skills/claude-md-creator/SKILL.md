---
name: claude-md-creator
description: >
  Create, audit, and maintain CLAUDE.md files for Claude Code projects. Use when the user wants to:
  (1) Create a new CLAUDE.md for a project root or globally at ~/.claude/CLAUDE.md,
  (2) Create nested CLAUDE.md files for specific folders within a project (e.g., supabase/, api/, frontend/),
  (3) Audit and trim an existing CLAUDE.md that has grown too large or stale,
  (4) Review and right-size CLAUDE.md files after a model upgrade.
  Triggers on phrases like "create claude.md", "set up claude md", "audit my claude md",
  "clean up my CLAUDE.md", "add a claude.md to this folder", "initialize project instructions".
---

# CLAUDE.md Creator

Create high-leverage CLAUDE.md files through structured user interrogation and codebase analysis.

CLAUDE.md is the single highest-leverage configuration in Claude Code. One bad line cascades through research, planning, and implementation. This skill ensures every line earns its place.

## Core Principles

Before writing any CLAUDE.md content, internalize these rules:

1. **Brevity over completeness** - Root files under 100 lines. Never exceed 300 lines total.
2. **Only what Claude doesn't know** - Never teach Claude things it already knows (encryption, git basics, common patterns). Only add project-specific context.
3. **Universal applicability** - Every instruction in the root file must apply to every task. Move task-specific guidance to nested files.
4. **Hooks over instructions** - If a constraint must never be violated (e.g., "never run db push"), implement it as a hook, not a CLAUDE.md line.
5. **References over snippets** - Point to files with `file:line` notation instead of pasting code that will go stale.
6. **Start small, add on mistakes** - Begin minimal. The interrogation identifies what *could* go in the file, but the draft should only include what the model would get wrong without. When in doubt, leave it out and add later when a mistake occurs.

For detailed best practices, read `references/best-practices.md`. For prompt caching implications when building agentic products, read `references/prompt-caching.md`.

## Workflow

### Step 1: Detect Mode

Determine which mode applies:

- **New Project** - No CLAUDE.md exists at project root. Create one from scratch.
- **Existing Project Audit** - CLAUDE.md exists but needs review/trimming.
- **Nested CLAUDE.md** - Adding a folder-level CLAUDE.md for a specific subdirectory.
- **Root Config** - Creating or updating the global `~/.claude/CLAUDE.md`.

If ambiguous, use AskUserQuestion:

```
"What type of CLAUDE.md work do you need?"
Options: New project | Audit existing | Nested folder | Global root config
```

### Step 2: Explore Context

Before asking questions, gather what you can automatically:

**For New Project / Existing Project:**
1. Read `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, or equivalent to identify tech stack
2. Run `ls` on the project root to understand structure
3. Check for existing CI/CD configs, test scripts, build commands
4. Look for monorepo indicators (workspaces, packages/, apps/)
5. Check git history for project maturity
6. If CLAUDE.md exists, read it fully

**For Nested CLAUDE.md:**
1. Read files in the target directory to understand its purpose
2. Read the root CLAUDE.md to avoid duplication
3. Identify what instructions are specific to this subdirectory

**For Root Config:**
1. Read existing `~/.claude/CLAUDE.md` if it exists
2. Check `~/.claude/settings.json` for existing preferences
3. Note: `settings.json` handles permissions and tool allowlists. CLAUDE.md handles behavioral guidance, conventions, and workflow preferences. Don't duplicate settings.json concerns in CLAUDE.md.

### Step 3: Interrogate the User

Use AskUserQuestion to gather what cannot be inferred from the codebase. Ask in rounds of 2-4 questions max per round. Do 3-5 rounds total depending on mode.

Consult `references/question-bank.md` for the full question bank organized by mode. Select the most relevant questions based on what you learned in Step 2. Skip questions you can already answer from codebase exploration.

**Critical rules for interrogation:**
- Never ask more than 4 questions in a single AskUserQuestion call
- Skip questions whose answers are obvious from the codebase
- Ask the most important questions first
- Follow up on ambiguous or surprising answers
- After each round, briefly summarize what you've learned and what you still need

### Step 4: Draft the CLAUDE.md

Structure the file in this exact order (most important content first, per LLM attention patterns):

#### For Project CLAUDE.md (New or Audited):

```markdown
# [Project Name]

[1-2 sentence description of what this project is and its purpose]

## Tech Stack
[Only if not obvious from config files. Brief list.]

## Key Commands
[Build, test, lint, deploy commands. Only non-obvious ones.]

## Architecture
[Brief description of how the project is organized. For monorepos, map apps/packages.]

## Conventions
[Project-specific patterns that deviate from defaults. NOT general best practices.]

## Gotchas
[Known issues, quirks, or constraints specific to this codebase.]
```

#### For Nested CLAUDE.md:

```markdown
# [Folder Purpose]

[1-2 sentences on what this part of the codebase does]

## Workflow
[Specific procedures for working in this directory]

## Constraints
[Rules that apply only when working in this area]
```

#### For Root Config (~/.claude/CLAUDE.md):

```markdown
# Claude Code Global Preferences

## Formatting Rules
[User's universal formatting preferences]

## Workflow Preferences
[How the user likes to work across all projects]

## Testing & Validation
[Universal testing expectations, e.g., always include tests for new logic]

## Plan Mode
[Where plans are stored, how to resume them across sessions]

## Communication Style
[How the user prefers Claude to communicate, if non-default]
```

Omit any section the user has no preferences for. Only include sections with actual content.

**Drafting rules:**
- Write in imperative form ("Use npm" not "You should use npm")
- No examples of things Claude already knows
- No style guides (delegate to linters/formatters via hooks)
- Every line must pass the test: "Would removing this cause Claude to make a mistake?"
- Prefer bullet points over paragraphs
- Include `file:line` references to authoritative sources instead of copying code

### Step 5: Review with User

Present the draft to the user. Ask using AskUserQuestion:

```
"Review this CLAUDE.md draft. What should I change?"
Options:
  - Looks good, finalize it
  - Too verbose, trim it down
  - Missing important context
  - Need to restructure
```

If changes are requested, iterate. Then write the file.

### Step 6: Suggest Complementary Actions

After writing the CLAUDE.md, suggest (but do not automatically do):

1. **Nested files** - If the root file has section-specific instructions, suggest moving them to nested CLAUDE.md files in relevant directories
2. **Hooks** - If any instructions are "never do X" constraints, suggest implementing them as pre-tool-use hooks instead
3. **agent_docs/** - If there's detailed reference material (schemas, API docs), suggest creating an agent_docs/ directory with pointers from CLAUDE.md. See guidelines below.
4. **Prompt caching awareness** - If the user is building an agentic product, suggest reviewing `references/prompt-caching.md` for CLAUDE.md patterns that preserve cache hit rates.

### agent_docs/ Guidelines

When a project has detailed reference material that Claude needs for specific tasks but that would bloat CLAUDE.md, suggest an `agent_docs/` directory:

- **What goes in agent_docs/**: API schemas, database schema docs, architecture decision records, deployment runbooks, third-party integration guides
- **Naming convention**: Use descriptive kebab-case names (e.g., `api-schema.md`, `db-migrations.md`, `auth-flow.md`)
- **Reference from CLAUDE.md**: Add a brief pointer in the relevant section, e.g., `For database schema details, see agent_docs/db-schema.md`
- **Keep each file focused**: One topic per file. Claude loads these on demand, so smaller focused files are better than one large dump.

### Step 7: Suggest Maintenance Cadence

Remind the user that CLAUDE.md is a living document:

- **After model upgrades**: Review for instructions newer models handle natively. Remove what's no longer needed.
- **After major project changes**: New dependencies, architecture shifts, or team changes should be reflected.
- **When Claude makes repeated mistakes**: Add the missing instruction that would have prevented the error.
- **Quarterly lightweight audit**: Run audit mode to trim bloat before it accumulates.

## Audit Mode

When auditing an existing CLAUDE.md:

1. **Read the file** and count lines/instructions
2. **Flag issues** using this checklist:
   - Lines > 300? Flag as too long
   - Instructions Claude already knows? Flag for removal
   - Code snippets that could be file references? Flag for replacement
   - Style/formatting rules that should be linter hooks? Flag for migration to hooks
   - Task-specific instructions in root file? Flag for nesting into subdirectory CLAUDE.md files
   - Conflicting instructions? Flag for resolution
   - Instructions for older model behaviors that newer models handle natively? Flag for removal
3. **Present findings** to user with specific line-by-line recommendations
4. **Ask permission** before making any changes using AskUserQuestion
5. **Rewrite** the file following the drafting rules above
