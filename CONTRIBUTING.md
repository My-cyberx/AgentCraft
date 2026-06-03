# Contributing to AgentCraft

Thanks for your interest. AgentCraft is a curated library — every artifact is reviewed before it lands.

## What we're looking for

- **O&G and API-auditing specific scripts, skills, or flows.** Generic utilities don't fit.
- **Driven by real field experience.** Every artifact must have a source-of-truth document in `canon/`.
- **Reusable by strangers.** If a script only works on your laptop, it's a private notebook, not a library artifact.

## The 7-stage workflow

Every artifact passes through these stages. Full spec in the strategy brief §6.

1. **Draft** — work in your fork under `canon/<domain>/<vertical>/<artifact>/`
2. **Test** — run with 2-3 real inputs, save outputs to `./test-runs/`
3. **Review** — open a PR, self-review against the [PR checklist](#pr-checklist), tag 1 peer
4. **Version** — bump semver, append CHANGELOG, tag git
5. **Publish** — merge to main, drive canon folder syncs from the published commit
6. **Index** — add to the public catalog with trigger prompt, inputs, sample output
7. **Maintain** — scheduled check (CI runs weekly, manual review monthly)

## PR checklist

```
[ ] Trigger prompt works as written — paste into a fresh Hermes/Claude session, confirm right skill loads
[ ] Inputs are explicit — artifact fails loudly if required input is missing
[ ] Outputs are reproducible — same input → same output (variance documented if not)
[ ] No secrets in source — .env, API keys, tokens referenced, never embedded
[ ] Drive source linked — canon PDF/doc this derives from is in the frontmatter
[ ] CHANGELOG entry added — semver bumped, date set, one-line summary
[ ] Site renders — `mkdocs build --strict` succeeds, the slug resolves
[ ] Tested against latest spec — if API Q1, tested against API Q1 11th ed.
[ ] Filename follows §2.2 convention — `<NN>-<name>-vMAJOR.MINOR.PATCH-YYYY-MM-DD.<ext>`
[ ] No "final" / "v2" / "new" in the filename
```

## File naming

Strict: `<NN>-<artifact-name>-v<MAJOR>.<MINOR>.<PATCH>-<YYYY-MM-DD>.<ext>`

- `NN` = one of `00` (canon), `10` (skill), `20` (flow), `30` (source), `90` (archive)
- Lowercase-kebab-case, no spaces, no underscores, no CamelCase
- ISO date, semver, original extension preserved

Run `python scripts/validate_naming.py` to check your files.

## Code of conduct

Be technical, be direct, be kind. No marketing fluff in code or PRs. If you have to explain why a contribution is good, lead with the artifact it produces, not the relationship you have with the author.
