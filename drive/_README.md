# Google Drive — AgentCraft source-of-truth

This local `drive/` folder is a **mirror** of the Google Drive layout described in `agentcraft-strategy-brief.md` §2.1.

> The actual production source of truth is the Google Drive at `My Drive / AgentCraft/`. The `canon/` folder in this repo is a **publishable** mirror of select Drive artifacts — only artifacts that are ready to be public live in `canon/`. The Drive canon folder contains everything, including private / WIP / client-specific.

## Folder layout (mirrors Drive 1:1)

```
AgentCraft/                          ← top-level project folder (share with co-maintainers)
├── _README.md                       ← this file
├── _CHANGELOG.md                    ← appended on every push
├── 00-canon/                        ← canonical, source-of-truth documents
│   ├── drilling/
│   │   ├── upstream/    (depro-calc, cement-job-design, liner-hanger-overview)
│   │   ├── midstream/
│   │   └── downstream/
│   ├── quality/        (api-q1, api-q2, iso-9001)
│   ├── hse/            (iwcf-l4, iadc, well-control-manual)
│   ├── operations/     (lss, sme-audit)
├── 10-skills/                       ← published Hermes skills (one folder each)
├── 20-flows/                        ← published Hermes flows
├── 30-sources/                      ← raw PDFs, decks, sheets (read-only reference)
│   ├── adnoc/
│   ├── weatherford/
│   ├── api-standards/
│   └── iadc/
└── 90-archive/                      ← superseded versions (never delete; date-stamp)
```

## Reserved `NN-` prefixes (filenames)

| Prefix | Folder meaning |
|---|---|
| `00-` | Canon — source-of-truth, versioned, authoritative |
| `10-` | Skills — Hermes `SKILL.md` files |
| `20-` | Flows — multi-stage compositions |
| `30-` | Sources — read-only references (PDFs, decks from third parties) |
| `90-` | Archive — superseded, deprecated, or rolled-back |

## Filename convention

```
<NN>-<artifact-name>-v<MAJOR>.<MINOR.PATCH>-<YYYY-MM-DD>.<ext>
```

Examples:
- `00-depro-formula-v3.2.1-2026-06-03.pdf`
- `00-api-q1-audit-checklist-v1.4.0-2026-05-20.xlsx`
- `00-liner-hanger-overview-v2.0.0-2026-04-12.pptx`

Full rules: `agentcraft-strategy-brief.md` §2.2.

## How to recreate this in your actual Google Drive

1. Open https://drive.google.com
2. Click `+ New` → `Folder` → name it `AgentCraft`
3. Inside `AgentCraft/`, create the subfolders above (one at a time, or use the Apps Script below)
4. Open each folder, click the gear icon → `Manage versions` → `Enable automatically keep forever`
5. Move your existing O&G / API-auditing files into the right canon folder
6. Rename each file to match the §2.2 convention

### Bulk-create via Apps Script (faster)

In the Drive Apps Script editor (Extensions → Apps Script in any Google Doc):

```javascript
function createAgentCraftFolders() {
  const root = DriveApp.getFoldersByName("AgentCraft").next();
  const tree = {
    "00-canon/drilling": ["upstream", "midstream", "downstream"],
    "00-canon/quality":  ["api-q1", "api-q2", "iso-9001"],
    "00-canon/hse":      ["iwcf-l4", "iadc", "well-control-manual"],
    "00-canon/operations": ["lss", "sme-audit"],
    "10-skills": [],
    "20-flows": [],
    "30-sources": ["adnoc", "weatherford", "api-standards", "iadc"],
    "90-archive": []
  };
  for (const [parent, children] of Object.entries(tree)) {
    let p = root;
    for (const seg of parent.split("/")) p = p.createFolder(seg);
    for (const c of children) p.createFolder(c);
  }
  Logger.log("Done. Open AgentCraft/ in Drive.");
}
```

Run it once. ~3 seconds.

## Sync between Drive and the public repo

The public `canon/` folder in this GitHub repo is a **publishable** mirror. The publishing flow:

```
Drive canon file (source of truth)
        ↓
Maintainer (you) opens PR to this repo with the file
        ↓
PR reviewed, CI runs, CHANGELOG updated
        ↓
Merged → public site redeployed
```

The reverse direction: the public site has a `last_tested` date that the maintainer rolls back to Drive if the source PDF is updated. This is why every canon artifact has a `CHANGELOG.md` — it's the audit log from Drive → repo → public site.
