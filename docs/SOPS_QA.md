# SOP - Quality Assurance and Release Checks

## Purpose
Ensure each deliverable meets quality and compliance standards before release.

## Inputs
- Final masters, captions, metadata, sponsor read notes.

## Outputs
- QA-approved release artifacts and logged issues.

## Checklist - Video QA
- [ ] Resolution and aspect ratio match platform specs.
- [ ] No dropped frames or sync drift.
- [ ] Color grading consistent across scenes.
- [ ] Overlays and graphics aligned correctly.

## Checklist - Audio QA
- [ ] Loudness meets target (see `docs/DELIVERABLES.md`).
- [ ] No clipping, pops, or distortion.
- [ ] Consistent levels between speakers.

## Checklist - Captions and Metadata
- [ ] Captions align to speech and have correct names.
- [ ] Titles, descriptions, and tags are accurate.
- [ ] Sponsor links and disclosures included.

## Checklist - Social QA
- [ ] Post copy matches approved templates.
- [ ] Links resolve to the correct destination.
- [ ] Scheduled time matches target release window.

## Diagnostics
- [ ] Run `python scripts/diagnostics.py --format text` for a snapshot.
- [ ] Run `python -m scripts.cli credentials --mode offline` for credential coverage.

## Issue Logging
- [ ] Record any QA failures with timestamp and impact.
- [ ] Flag blocking issues before publish.
- [ ] Add a follow-up task in `tasks.md` if needed.
