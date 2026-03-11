# Question Bank

Organized questions for each CLAUDE.md creation mode. Select questions based on what codebase exploration has NOT already answered. Never ask all questions; pick the most relevant 8-15 across 3-5 rounds.

## New Project Mode

### Round 1: Purpose & Architecture (always ask first)

```
Q: "What is this project in one sentence? What problem does it solve?"
Header: "Purpose"
Options:
  - Web app / SaaS product
  - Mobile app
  - API / backend service
  - CLI tool or library

Q: "How is this project structured?"
Header: "Structure"
Options:
  - Monorepo with multiple apps/packages
  - Single app with standard folders (src/, lib/, etc.)
  - Microservices
  - Library/SDK
```

```
Q: "Who works on this codebase?"
Header: "Team"
Options:
  - Just me
  - Small team (2-5)
  - Large team (5+)
  - Open source with contributors
```

### Round 2: Workflow & Tools

```
Q: "What package manager and runtime do you use?"
Header: "Runtime"
Options:
  - npm
  - pnpm
  - bun
  - yarn
[Skip if detected from lockfile]

Q: "How do you run tests?"
Header: "Testing"
Options:
  - [Detected command] (confirm)
  - Custom command (specify)
  - No tests yet
  - Multiple test suites
[Skip if test scripts found in package.json or equivalent]

Q: "How do you deploy?"
Header: "Deploy"
Options:
  - CI/CD pipeline (GitHub Actions, etc.)
  - Manual deploy commands
  - Platform auto-deploy (Vercel, Netlify, Railway)
  - Not deployed yet
```

### Round 3: Conventions & Constraints

```
Q: "Are there any project-specific conventions Claude should know? (e.g., naming patterns, file organization rules, API design choices)"
Header: "Conventions"
Options:
  - Yes, naming/file conventions to follow
  - Yes, architectural patterns to follow
  - Yes, API design conventions
  - None beyond standard practices

Q: "Are there any operations Claude should NEVER perform? (e.g., push to production DB, modify certain folders, run specific commands)"
Header: "Constraints"
Options:
  - Yes (specify) - these will become hook suggestions
  - No dangerous operations to guard against

Q: "Are there known gotchas or quirks in this codebase that trip people up?"
Header: "Gotchas"
Options:
  - Yes, environment/setup gotchas
  - Yes, code/architecture gotchas
  - Yes, deployment/build gotchas
  - None that I know of
```

### Round 4: Context Depth (ask if project is complex)

```
Q: "Are there any external services, APIs, or databases with non-obvious setup?"
Header: "Services"
Options:
  - Yes (will create agent_docs/ pointers)
  - No, standard setup

Q: "Is there detailed documentation (schemas, API docs, architecture docs) that Claude should reference when working in specific areas?"
Header: "Deep docs"
Options:
  - Yes (will suggest agent_docs/ or nested CLAUDE.md files)
  - No, codebase is self-explanatory
```

## Existing Project Audit Mode

### Round 1: Current State

```
Q: "When was your CLAUDE.md last updated? Has the project changed significantly since?"
Header: "Freshness"
Options:
  - Recently updated and mostly current
  - Months old, project has evolved
  - Never really maintained it
  - Not sure

Q: "Have you noticed Claude making mistakes that your CLAUDE.md should have prevented?"
Header: "Gaps"
Options:
  - Yes (specify what mistakes)
  - No, but file feels bloated
  - Yes AND it's bloated
```

### Round 2: Pain Points

```
Q: "What's your biggest frustration when Claude works on this project?"
Header: "Pain point"
Options:
  - Makes wrong architectural choices
  - Doesn't follow project conventions
  - Uses wrong commands or tools
  - Over-engineers simple tasks
[Let user type freely as alternative]

Q: "Are there instructions in your CLAUDE.md that you suspect Claude ignores?"
Header: "Ignored rules"
Options:
  - Yes (will review and possibly convert to hooks)
  - Not sure
  - No, it follows everything
```

## Nested CLAUDE.md Mode

### Round 1: Scope

```
Q: "What does this directory handle?"
Header: "Purpose"
Options:
  - Backend/API logic
  - Frontend/UI components
  - Database/migrations
  - Shared utilities/libraries

Q: "What specific workflows happen in this directory that differ from the rest of the project?"
Header: "Workflows"
Options:
  - Unique build/compile steps
  - Special testing procedures
  - Migration or deploy workflows
  - No different workflows, just scoped conventions
```

### Round 2: Boundaries

```
Q: "Are there any commands or operations specific to this directory? (e.g., migration commands, build steps, test commands)"
Header: "Commands"
Options:
  - Yes (specify)
  - No, same as project root

Q: "Are there constraints that apply ONLY when working in this directory?"
Header: "Constraints"
Options:
  - Yes (specify)
  - No additional constraints
```

## Root Config Mode (~/.claude/CLAUDE.md)

### Round 1: Global Preferences

```
Q: "What formatting preferences do you want applied across ALL projects?"
Header: "Formatting"
Options:
  - Punctuation/grammar rules (e.g., no em dashes)
  - Code style preferences (e.g., single quotes)
  - Output formatting (e.g., concise responses)
  - No universal formatting rules

Q: "What workflow preferences do you have across all projects?"
Header: "Workflow"
Options:
  - Always ask before committing
  - Prefer planning before coding
  - Run tests after every change
  - Minimal output, skip explanations
[multiSelect: true]
```

### Round 2: Communication Style

```
Q: "How do you prefer Claude to communicate?"
Header: "Style"
Options:
  - Concise and direct
  - Detailed explanations
  - Ask before making decisions
  - Act autonomously, report results

Q: "Are there any tools, languages, or frameworks you always or never want used?"
Header: "Preferences"
Options:
  - Yes, always-use preferences (specify)
  - Yes, never-use preferences (specify)
  - Both always-use and never-use rules
  - No strong tool preferences
```

### Round 3: Cross-Project Rules

```
Q: "Any universal rules for how Claude should handle git, testing, or deployments across all your projects?"
Header: "Git/CI rules"
Options:
  - Yes, git workflow rules (e.g., commit style, branching)
  - Yes, testing requirements (e.g., always test before commit)
  - Yes, deployment rules (e.g., never push to prod)
  - No universal git/CI rules

Q: "Anything else that applies to every project you work on?"
Header: "Other"
Options:
  - Yes, additional rules to add
  - That covers everything
```
