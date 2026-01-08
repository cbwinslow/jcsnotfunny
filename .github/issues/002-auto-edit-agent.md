# Auto-Edit / Multi-Cam Edit Agent (Priority: 2)

Summary

Build an automated multi-camera editor that takes camera feeds + audio + transcripts/CC and produces an EDL and a rendered video that focuses on the active speaker, with rules for reaction shots, wide shots, and scene-interest switching.

Acceptance criteria (measurable)

- For provided synthetic 1v1 test, the EDL JSON generated matches ground-truth shot list within a tolerance of +/- 0.5s per cut.

- EDL covers >= 95% of the speaker-active intervals (speech time) for the test set.

- Unit tests assert min_shot_length enforcement and guard_time/hysteresis smoothing behavior.

- Render step produces an MP4 (or validated simulated render) artifact that CI uploads as an artifact.

Subtasks / microgoals

- Create `scripts/auto_edit/` skeleton with modules: `ingest.py`, `sync.py`, `audio.py`, `vision.py`, `mapper.py`, `edl.py`, `renderer.py`, and `cli.py`.

- Implement synthetic test videos for 1v1 and 3-way scenarios with ground-truth shot lists.

- Implement MediaPipe-based face detection & tracking and lip-motion correlation mapping.

- Implement EDL generator with min_shot_length, guard_time, and reaction-shot rules.

- Add tests for EDL consistency, face tracker stability, and integration smoke test.

Labels: type/automation, area/editing, priority/high

Estimate: 4–8 days (PoC + tests)
