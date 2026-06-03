# How it works

AgentCraft has three artifact types. The decision of which to use is the first thing to learn.

## The decision tree

```
Does the task need an LLM to interpret, decide, or write?
├── NO  → Script.     A single file. Deterministic. Zero API cost.
└── YES
    ├── Does it need only ONE tool/API and <5 steps?    → Skill.
    └── Does it need 3+ tools, 5+ stages, multi-output? → Flow.
```

## The three types

### Script

A single, deterministic, copy-pasteable file (Python, Bash, SQL, JS) that does one job. **No LLM in the loop.** Same input → same output, always. No API cost. Usually stdlib only.

| Example | Domain | What it does |
|---|---|---|
| [DEPRO Calculator](library/drilling/upstream/depro-calc.md) | Drilling | Calculate Daily Equivalent Production Offline + Monte Carlo uncertainty |
| [API Q1 Audit Checklist](library/quality/api-q1/audit-checklist.md) | Quality | Generate 35-clause audit checklist with severity + gap detection |
| Pareto chart | Operations | CSV → ranked bar chart with cumulative % line |
| Fishbone diagram | Operations | Free-text causes → structured Ishikawa SVG |

### Skill

A `SKILL.md` with YAML frontmatter that an agent loads to gain a repeatable procedure + the right tools/env to execute it. The skill teaches the agent *how* to do a specific thing, in your voice, with the right tool calls.

| Example | Domain | What it does |
|---|---|---|
| `skill-iwcf-l4-drill` | HSE | Run a 30-min IWCF L4 well control drill — agent plays examiner, you play candidate |
| `skill-cement-job-design` | Drilling | Produce a cementing job design from a well spec |
| `skill-audit-non-conformance` | Quality | Review an NCR against API Q1 11th ed., output a gap list with severity |
| `skill-depro-calc` (wrapper) | Drilling | Wraps the DEPRO script with the right voice + checklist + chat output |

### Flow

A multi-stage, multi-tool composition (an agent + a sequence of skills + scripts + APIs) that produces a complete deliverable. Flows are the closest thing AgentCraft ships to "an entire product in one run."

| Example | Domain | Stages | Cost / run |
|---|---|---|---|
| [SME Audit Deliverable](library/operations/sme-audit/flow-audit-deliverable.md) | Operations | 8 stages: intake → BMC → PESTEL → gap → roadmap → vendors → package → delivery | ~$0.54 |
| Lead Research | Sales | ICP → Apollo/Apify discover → DeepSeek enrich → Airtable | ~$0.55 |
| Content Publish | Marketing | Topic → Exa research → DeepSeek draft → Gemini visuals → Beehiiv newsletter | ~$0.29 |
| Build Website | Web | Brief → IA → copy → design system → visuals → Next.js code → Vercel deploy | ~$0.17 |

## The three filters visitors use

When you browse the [library](library/index.md), you can filter by:

1. **Domain** — Drilling / Quality / HSE / Operations
2. **Type** — Script / Skill / Flow
3. **Vertical** — Upstream / Midstream / Downstream (drilling); API Q1 / API Q2 / ISO 9001 (quality); IWCF / IADC (HSE); LSS / SME Audit (operations)

Plus a tag overlay (`#offline`, `#needs-api`, `#abu-dhabi`, etc.) for cross-cutting filters.

## What's NOT here

- Generic productivity skills (todos, calendars, email) — those belong in Hermes, not here
- Skills with no source-of-truth document in Drive
- Skills that only work on one specific client's data
- Anything where the LLM does the heavy lifting and the input/output isn't a real artifact

## Why domain-first?

A petroleum engineer asks "do you have anything for cementing?" not "do you have any skills that take a YAML well spec and produce a 12-section markdown report?" Domain-first matches how visitors think. The type filter is secondary because visitors care *that* the answer exists, not *what tech* it uses.

Full taxonomy: `agentcraft-strategy-brief.md` §3.
