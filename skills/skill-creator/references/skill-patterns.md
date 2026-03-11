# Skill Patterns Reference

Patterns that separate great skills from mediocre ones. Apply these during Step 4 (Edit the Skill) of the creation process. Every pattern includes what it is, why it matters, and a concrete example.

---

## Pattern 1: Mandatory Q&A Gate

**What:** Define the exact questions that must be answered before any work begins. Split into "Required" (must ask) and "Optional" (ask if relevant) groups.

**Why:** Skills fail when Claude starts building with incomplete context. A Q&A gate forces context gathering upfront and prevents backtracking.

**How to write it:**

```markdown
## Step 1: Ask the User These Questions

Before writing ANY code, ask the user all of these. Do not proceed until you have answers:

### Required
1. **[Input name]** - "[Exact question to ask]"
2. **[Input name]** - "[Exact question to ask]"

### Optional
3. **[Input name]** - "[Exact question to ask]"
```

**Rules:**
- Number every question. Users can respond by number.
- Bold the input name so it's scannable.
- Put the actual question in quotes so Claude asks it verbatim.
- Group by Required vs Optional. Never let Claude skip Required questions.
- Keep it under 10 questions. If you need more, the skill is too broad.

---

## Pattern 2: Derived Decisions

**What:** Explicitly mark decisions Claude should make autonomously based on the user's answers, without asking.

**Why:** Users don't want to make every micro-decision. Good skills define where Claude exercises judgment vs. where it gathers input. This is the difference between a helpful agent and a question machine.

**How to write it:**

```markdown
### Derived from answers (do NOT ask, decide yourself)

Based on the user's [input], decide:
- **[Decision area]**: [guidance on how to decide]
- **[Decision area]**: [guidance on how to decide]
```

**Example:** In an app-store-screenshots skill, the user provides brand colors and style direction. Claude then decides gradient directions, decorative elements, dark vs light slides, and typography treatment without asking.

**Rules:**
- List every derived decision explicitly. Don't leave it implicit.
- Provide enough guidance that Claude makes good decisions, not random ones.
- Draw a clear line: "Ask about X. Decide Y yourself."

---

## Pattern 3: Strong Opinions

**What:** Encode opinionated defaults and principles that override Claude's generic tendencies. State them as absolutes, not suggestions.

**Why:** Claude defaults to safe, generic output. Skills exist to push past generic. Without opinions, the skill produces the same output Claude would produce without the skill.

**How to write it:**

Use declarative, absolute statements:
- "Screenshots are advertisements, not documentation."
- "Each slide sells ONE idea. Never two features on one slide."
- "If you're showing UI, you're doing it wrong."

**Anti-pattern:** Weak phrasing that Claude will ignore:
- "Consider making screenshots more like advertisements"
- "Try to keep each slide focused on one idea"
- "It's generally better to sell a feeling"

**Rules:**
- Use imperative language. "Do X." Not "Consider X."
- State the principle, then state why. "Each slide sells ONE idea. Never two features on one slide."
- If an opinion can be stated as a rule, state it as a rule.
- Bold or uppercase the most critical opinions so they can't be skimmed.

---

## Pattern 4: Domain Methodology

**What:** Embed frameworks, taxonomies, or structured approaches from the domain the skill operates in. These are the "how to think about it" instructions, not just "what to do."

**Why:** Claude has surface knowledge of most domains but lacks the structured thinking experts use. A methodology transforms generic output into expert-level output.

**How to write it:**

```markdown
### Three Approaches (pick one per [unit of work])

| Type | What it does | Example |
|------|-------------|---------|
| **[Approach A]** | [Description] | "[Concrete example]" |
| **[Approach B]** | [Description] | "[Concrete example]" |
| **[Approach C]** | [Description] | "[Concrete example]" |
```

**Examples of domain methodologies:**
- Copywriting: "Paint a moment / State an outcome / Kill a pain" with examples
- Code review: "Correctness / Performance / Readability" priority framework
- UX design: "Information hierarchy / Interaction cost / Error recovery" checklist
- Sales emails: "Problem / Agitation / Solution" framework with word-count targets

**Rules:**
- Always include concrete examples. Frameworks without examples are useless.
- Show what GOOD looks like and what BAD looks like side by side.
- Keep frameworks to 3-5 options. More than that and Claude won't internalize them.

---

## Pattern 5: Anti-Pattern Tables

**What:** A table of common mistakes paired with their fixes. Written as "Mistake | Fix" pairs.

**Why:** Claude makes predictable mistakes in every domain. Listing them explicitly prevents them. This is the single highest-ROI section of any skill because it catches failures before they happen.

**How to write it:**

```markdown
## Common Mistakes

| Mistake | Fix |
|---------|-----|
| [Specific bad output] | [Specific correction] |
| [Specific bad output] | [Specific correction] |
```

**Example:**

| Mistake | Fix |
|---------|-----|
| All slides look the same | Vary phone position (center, left, right, two-phone, no-phone) |
| Copy is too complex | "One second at arm's length" test |
| Export is blank | Use double-call trick; move element on-screen before capture |

**Rules:**
- Be specific. "Output is bad" is not a mistake. "All slides use the same centered phone layout" is.
- The fix should be actionable in one sentence.
- Include 5-15 mistakes. Fewer means you haven't thought hard enough. More means the skill is too broad.
- Add to this table every time you discover a new failure mode during iteration.

---

## Pattern 6: Technical Specifications

**What:** Exact values, measurements, configurations, and implementation details that took effort to discover. The hard-won knowledge that would otherwise require trial and error.

**Why:** Claude will guess at technical details and often guess wrong. Encoding exact specs eliminates entire categories of bugs and produces production-ready output on the first attempt.

**How to write it:**

```markdown
### Phone Mockup Measurements
const MK_W = 1022;  // mockup image width
const MK_H = 2082;  // mockup image height
const SC_L = (52 / MK_W) * 100;   // screen left offset %
```

```markdown
### Export Sizes (Apple Required)
const SIZES = [
  { label: '6.9"', w: 1320, h: 2868 },
  { label: '6.5"', w: 1284, h: 2778 },
];
```

**What to encode:**
- Pixel dimensions, offsets, border radii
- API response formats and required fields
- Library-specific workarounds (e.g., "call toPng twice, first warms up fonts")
- Platform requirements (export sizes, file naming conventions)
- Configuration values that took debugging to discover

**Rules:**
- Include comments explaining WHY, not just WHAT.
- If a value was discovered through debugging, note that: "CRITICAL: Double-call trick..."
- Prefer code blocks with actual usable values over prose descriptions.
- If a specification has a source (Apple docs, API reference), mention it.

---

## Pattern 7: Reference Benchmarks

**What:** Name specific real-world examples of the quality bar you're targeting. Apps, websites, products, or content that exemplifies "good."

**Why:** "Make it good" is subjective. "Match the copy style of Raycast's App Store listing" is concrete. Reference benchmarks align Claude's output to a specific quality standard.

**How to write it:**

```markdown
### Reference Apps for Copy Style
- **Raycast** - specific, descriptive, one concrete value per slide
- **Turf** - ultra-simple action verbs, conversational
- **Mela / Notion** - warm, minimal, elegant
```

**Rules:**
- Pick 2-5 references. One is too narrow, more than five is noise.
- Say WHY each reference is relevant, not just the name.
- References can be apps, websites, books, writing styles, design systems.
- Update references as the domain evolves.

---

## Pattern 8: Architecture Blueprints

**What:** Define the exact file structure, component tree, or system architecture that the skill's output should follow. Include the full structure, not just "organize your code well."

**Why:** Without a blueprint, Claude invents a new architecture every time. This causes inconsistency and over-engineering. A fixed blueprint produces predictable, maintainable output.

**How to write it:**

```markdown
### Architecture

page.tsx
├── Constants (dimensions, design tokens)
├── Component A (description)
├── Component B (description)
├── Slide1..N components (one per slide)
├── SCREENSHOTS array (registry)
├── Preview (ResizeObserver scaling + export)
└── Page (grid + toolbar + export logic)
```

**Rules:**
- Show the full tree, not a partial one.
- Annotate each node with its purpose.
- Specify constraints: "Single file. No routing. No API routes."
- Include the WHY behind structural decisions.

---

## Pattern 9: Output Constraints

**What:** Hard limits on the scope and shape of what the skill produces. Constraints prevent over-engineering and scope creep.

**Why:** Claude's default tendency is to add more. More files, more abstractions, more "just in case" code. Constraints focus output on what matters.

**Examples:**
- "The entire generator is a single page.tsx file. No routing, no extra layouts, no API routes."
- "Each email is under 150 words. No exceptions."
- "Maximum 3 colors per slide. Background, text, accent."
- "One headline per slide. Never join two ideas with 'and.'"

**Rules:**
- State constraints as absolutes, not preferences.
- Explain the reasoning: "Single file because multi-file adds complexity without value for this use case."
- Constraints should be testable. "Keep it simple" is not testable. "Under 150 words" is.

---

## Pattern 10: Variation Rules

**What:** Explicit instructions for introducing variety across repeated outputs (slides, emails, sections, pages) so they don't all look identical.

**Why:** Claude defaults to repetition. If it finds a pattern that works, it applies it identically across all items. This produces monotonous output.

**How to write it:**

```markdown
### Layout Variation Rules
Vary across slides. NEVER use the same layout twice in a row:

- **Centered phone** (hero, single-feature)
- **Two phones layered** (comparison)
- **Phone + floating elements** (detail)
- **Left-aligned text, right phone** (asymmetric)
- **Right-aligned text, left phone** (mirror)
- **No phone** (more features, trust signal)

Include 1-2 contrast slides (inverted background) for visual rhythm.
```

**Rules:**
- List the specific variations available.
- State the constraint: "Never repeat the same [layout/structure/approach] twice in a row."
- Specify rhythm: "Include 1-2 [contrast/different] items per [set]."

---

## Applying These Patterns: Checklist

Use this during Step 4 (Edit the Skill) of the creation process. Not every skill needs every pattern, but consider each one:

- [ ] **Q&A Gate**: What must be known before starting? Write the exact questions.
- [ ] **Derived Decisions**: What should Claude decide without asking? Draw the line.
- [ ] **Strong Opinions**: What principles override Claude's generic defaults? State them as rules.
- [ ] **Domain Methodology**: What framework do experts use in this domain? Encode it with examples.
- [ ] **Anti-Patterns**: What are the 5-15 most common failure modes? List them with fixes.
- [ ] **Technical Specs**: What exact values/configs took effort to discover? Include them as code.
- [ ] **Reference Benchmarks**: What does "good" look like? Name 2-5 real examples.
- [ ] **Architecture Blueprint**: What's the exact structure of the output? Define the tree.
- [ ] **Output Constraints**: What limits prevent over-engineering? State them as absolutes.
- [ ] **Variation Rules**: How should repeated items differ from each other? List the variations.

## The Test

After writing a skill, ask: "If I gave this to a competent developer with zero context, could they produce expert-level output on the first attempt?" If the answer is no, the skill is missing something. Revisit the checklist.
