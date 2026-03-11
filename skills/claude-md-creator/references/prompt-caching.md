# Prompt Caching & CLAUDE.md

Lessons from the Claude Code team on building agent systems around prompt caching. These patterns apply to anyone building agentic products on the Anthropic API and should inform how you structure CLAUDE.md files and agent harnesses.

Source: Thariq Shihipar (Anthropic), Claude Code engineering team.

## Why This Matters

Prompt caching works by prefix matching. The API caches computation from the start of the request up to each `cache_control` breakpoint. Any change anywhere in the prefix invalidates everything after it. This single constraint should shape your entire system design.

The Claude Code team monitors cache hit rates like uptime and declares incidents when rates drop. A few percentage points of cache miss can dramatically affect cost and latency.

## The Optimal Ordering

Place content in your requests from most-static to most-dynamic:

```
1. Static system prompt & tools  (globally cached)
2. CLAUDE.md content             (cached within a project)
3. Session context               (cached within a session)
4. Conversation messages         (dynamic, appended each turn)
```

This maximizes how many sessions share cache hits. CLAUDE.md content sits in the stable middle: it changes rarely (per project) but is more dynamic than the system prompt.

**Implication for CLAUDE.md**: Stability matters. Frequent edits to CLAUDE.md can invalidate the cache for all sessions in a project. Write it once, write it well, and only update when necessary.

## Common Cache-Breaking Mistakes

Things that seem harmless but break the prefix:

| Mistake | Why it breaks caching |
|---------|----------------------|
| Putting timestamps in the system prompt | Changes every request |
| Shuffling tool definitions non-deterministically | Different ordering = different prefix |
| Updating tool parameters dynamically | Any parameter change invalidates the prefix |
| Adding/removing tools mid-session | Changes the cached prefix for entire conversation |
| Switching models mid-session | Caches are unique per model |

## Key Patterns

### Use Messages for Updates, Not Prompt Changes

When information becomes stale (time, file changes, etc.), don't update the system prompt. Instead, append the update as a `<system-reminder>` in the next user message or tool result. This preserves the cached prefix while still giving the model current information.

**CLAUDE.md implication**: Put stable, rarely-changing instructions in CLAUDE.md. For session-specific context (current date, recent changes), use messages instead.

### Never Add or Remove Tools Mid-Session

Changing the tool set invalidates the cache for the entire conversation. This seems intuitive (give the model only what it needs), but it's costly.

**Pattern**: Keep all tools present at all times. Use state-transition tools instead of swapping tool sets. For example, Claude Code implements plan mode not by removing edit tools, but by adding `EnterPlanMode` and `ExitPlanMode` as tools. The model calls these to change modes without ever changing the tool definitions.

### Defer Instead of Remove

When you have many tools (e.g., dozens of MCP tools), include lightweight stubs with `defer_loading: true` instead of removing them. The model discovers full schemas via a ToolSearch tool when needed. The cached prefix stays stable because the same stubs are always present in the same order.

### Don't Switch Models Mid-Session

Prompt caches are model-specific. If you're 100k tokens into a conversation with Opus and switch to Haiku for a simple question, you pay full price to rebuild the cache for Haiku. It's actually cheaper to let Opus answer.

**Pattern**: Use subagents for model switching. The primary model prepares a focused handoff message to a different model, which runs in its own context. Claude Code does this with Explore agents that use Haiku.

### Cache-Safe Forking (Compaction)

When you run out of context window and need to summarize (compact), don't use a separate API call with a different system prompt. That throws away the entire cache.

**Pattern**: Send the compaction request using the exact same system prompt, tools, and conversation history as the parent conversation. Append the compaction instruction as a new user message at the end. The API sees nearly the same prefix and reuses the cache. Only the compaction prompt itself is new tokens.

Reserve a "compaction buffer" in your context window so you have room for the compaction message and summary output.

## CLAUDE.md Design Implications

These caching lessons directly affect how you should write CLAUDE.md:

1. **Stability is a feature** - A CLAUDE.md that rarely changes means better cache hit rates across sessions. This reinforces the "start small, add on mistakes" principle.

2. **Don't put dynamic content in CLAUDE.md** - Timestamps, version numbers, or anything that changes frequently should go in session messages, not CLAUDE.md.

3. **Ordering within CLAUDE.md matters less than ordering of CLAUDE.md in the prompt** - The system prompt loads CLAUDE.md at a specific position. What matters most is that CLAUDE.md content is stable and sits between the static system prompt and dynamic session context.

4. **Nested CLAUDE.md files are cache-friendly** - They only load when Claude reads files in that directory. This means they don't affect the cached prefix for sessions that never touch that directory.

5. **Hooks > CLAUDE.md for enforcement** - Hooks run deterministically and don't consume instruction budget or affect caching. Moving "never do X" rules to hooks keeps CLAUDE.md smaller and the prefix more stable.

## Monitoring Guidance

If you're building an agentic product:

- Track prompt cache hit rate as a key metric
- Alert on cache breaks and treat them as incidents
- Audit any change to system prompts, tool definitions, or CLAUDE.md for cache impact
- Test that tool ordering is deterministic across requests
- Verify that compaction and summarization use cache-safe forking
