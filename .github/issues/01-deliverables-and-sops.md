Title: Deliverables & SOPs — Formalize specs and checklists

**Description**
Formalize and expand `docs/SOPS.md` and `docs/DELIVERABLES.md` into a concise, testable set of SOPs and checklists for episode production.

**Why this matters**
Consistent deliverables and clear processes reduce rework and speed up turnaround for episodes and clips.

**Acceptance criteria**

- SOPs contain step-by-step instructions for ingest, naming, proxies, edit, audio mixing, clip creation, and publishing
- Deliverables include export presets, thumbnail spec, clip aspect ratios, caption formats
- One or more test scripts (FFmpeg or small Python) to validate export/LUFS exist in `scripts/`

**Checklist**

- [ ] Expand SOPs with naming and folder conventions
- [ ] Add LUFS check example script to `scripts/`
- [ ] Create printable one-page on-site checklist in `docs/`

**Labels**: area/editing, documentation
**Estimate**: 4–8h
**Assignee**: @<you>
**Related files**: `docs/SOPS.md`, `docs/DELIVERABLES.md`, `scripts/`
