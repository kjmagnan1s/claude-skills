# CLAUDE.md Best Practices

Synthesized from community research, public analysis of 1000+ CLAUDE.md files, and expert guidance.

## The Leverage Hierarchy

Each layer multiplies the impact of mistakes below it:

```
Bad CLAUDE.md line
  → Many bad research directions
    → Many bad plan lines
      → Hundreds of bad code lines
```

CLAUDE.md sits at the top of this hierarchy. It affects every task in every session.

## Instruction Budget

LLMs reliably follow approximately 150-250 instructions before accuracy degrades. The Claude Code system prompt uses ~50 of those. Your CLAUDE.md and prompts share the remaining budget.

**Implication:** Every instruction in CLAUDE.md has a cost. Low-value instructions crowd out high-value ones. The system prompt also includes a note that CLAUDE.md context "may or may not be relevant" and should only be used when "highly relevant," meaning bloated files get increasingly ignored.

## The Three Essential Components

Structure around WHAT, WHY, and HOW:

- **WHAT** - Tech stack, project structure, codebase architecture. Critical for monorepos where apps/packages need mapping.
- **WHY** - Project purpose. What different parts accomplish. This grounds planning decisions.
- **HOW** - Workflow, tools (npm vs bun), testing procedures, build and deploy commands.

## Length Guidelines

| File Type | Target | Max |
|-----------|--------|-----|
| Root CLAUDE.md | < 60 lines | 100 lines |
| Nested CLAUDE.md | < 40 lines | 80 lines |
| Total across all files | < 200 lines | 300 lines |

Analysis of 1000+ public repos found ~10% had files over 500 lines, which correlated with degraded model performance.

## What to Include

- Project description (1-2 sentences)
- Non-obvious build/test/lint commands
- Architecture overview for complex projects
- Project-specific conventions that deviate from defaults
- Known gotchas and quirks
- Pointers to detailed docs (agent_docs/ directory) with brief descriptions

## What NOT to Include

- **Things Claude already knows** - Common best practices, language features, standard patterns. These waste instruction budget and may constrain the model from applying even better approaches it has learned.
- **Code style rules** - Use linters and formatters via hooks instead. Style enforcement is deterministic work, not LLM work.
- **Code examples** - These go stale. Use `file:line` references to authoritative source code.
- **History/changelog entries** - CLAUDE.md is not a journal. Only current state matters.
- **Obvious commands** - If `npm install` or `git commit` appear, they're wasting space.
- **Random prompts from the internet** - Generic prompt engineering tips often degrade performance by adding noise.
- **Overly specific edge-case handling** - Don't try to handle every edge case. Trust the model's judgment.

## Positioning Matters

LLMs weigh content near the beginning and end of instructions more heavily than content in the middle. Place the most critical information (project description, key commands) at the top.

## The Three-Layer System (Boris Chenry, Claude Code Creator)

Claude Code walks up from your working directory loading every CLAUDE.md it finds. This gives you three layers:

- **~/.claude/CLAUDE.md** = Global rules. Commit style, workflow preferences, quality standards. Every project sees these automatically. Write once.
- **repo/CLAUDE.md** = Project-specific. One-liner, tech stack, commands, architecture rules. Committed and shared with collaborators.
- **repo/.claude/CLAUDE.md** = Local overrides. Personal preferences, dev server ports. Gitignored. Never committed.

Most people put everything in one file. The smart move: global rules go global, project rules go in the repo, personal stuff stays local. No duplication.

Source: @garrytan (594 likes), @theo (53K views), Boris Chenry interview with @JohnKimDev. Community synthesis by @mvanhorn: https://x.com/i/status/2025980195732418694

## Progressive Disclosure with Nested Files

Root CLAUDE.md is loaded at conversation start. Nested CLAUDE.md files are injected when Claude reads files in their directory. Use this:

```
project/
├── CLAUDE.md              (lightweight, universal instructions)
├── supabase/
│   └── CLAUDE.md          (migration workflow, DB-specific rules)
├── api/
│   └── CLAUDE.md          (API conventions, endpoint patterns)
└── frontend/
    └── CLAUDE.md          (component patterns, styling approach)
```

Benefits:
- Root stays lightweight and universally relevant
- Context injected at the right time, in the right place
- Avoids loading database instructions when editing frontend code

## Hooks Over Instructions

For constraints that must never be violated, use pre-tool-use hooks instead of CLAUDE.md lines:

| Instead of this in CLAUDE.md | Use a hook that |
|------------------------------|-----------------|
| "Never run `db push` yourself" | Blocks `supabase db push` commands |
| "Never modify the /vendor folder" | Blocks file writes to `/vendor/**` |
| "Always run tests after changes" | Runs test suite after file edits |

Hooks are deterministic and work 100% of the time. CLAUDE.md instructions may be forgotten in long sessions.

## Model Upgrades = Remove Instructions

With each model release, review CLAUDE.md for instructions that newer models handle natively. Common candidates for removal:

- "Don't over-engineer" (newer models are better at this)
- "Ask for clarification when needed" (built into model behavior)
- "Use proper error handling" (standard practice the model knows)
- Workarounds for older model weaknesses

The goal is to remove more than you add over time.

## Prompt Caching Awareness

CLAUDE.md sits in the cached prefix of every API request within a project. Changes to it invalidate the cache for all sessions. This reinforces several best practices:

- **Stability is a feature** - Write it once, write it well. Frequent edits cost real money through cache misses.
- **No dynamic content** - Timestamps, version numbers, or anything that changes per-session belongs in messages, not CLAUDE.md.
- **Nested files are cache-friendly** - They only load when Claude reads files in that directory, so they don't affect the prefix for unrelated sessions.

For the full prompt caching reference (tool ordering, model switching, compaction), see `prompt-caching.md`.

## Audit Checklist

When reviewing an existing CLAUDE.md:

1. Count total lines. Over 100 for root? Start cutting.
2. Read each line and ask: "Would Claude make a mistake without this?"
3. Check for code snippets that should be file references
4. Identify constraints that should be hooks
5. Find task-specific instructions that belong in nested files
6. Look for conflicting or redundant instructions
7. Remove anything the current model handles natively
8. Verify commands are still accurate and up to date
