# SOP - Audio Mixing and Presets

## Purpose
Provide repeatable starting points for mixing board or software filters.

## Inputs
- Raw mic audio, room noise profile, and mic model.

## Outputs
- Clean, consistent dialog mix within loudness targets.

## Preset Source
- Use `configs/audio_presets.yml` as the source of truth.
- Start with the closest voice type, then tune by ear.

## Checklist - Mixing Board Setup
- [ ] Set input gain so peaks land around -6 dB.
- [ ] Enable high-pass filter to reduce rumble.
- [ ] Apply a mild gate to reduce room noise.
- [ ] Add compression for consistent dialog.
- [ ] Use a de-esser to tame sibilance (s pops).
- [ ] Apply a limiter to prevent clipping.

## Notes on Presets
- **Male/Female**: Use `male_standard` or `female_standard` as baseline.
- **High/Low Pitch**: Use `high_pitch` or `low_pitch`.
- **Bassy/Pitchy**: Use `bassy_voice` or `pitchy_voice`.
- **Remote Guest**: Use `guest_remote` and raise noise reduction.

## Placeholders
- [PLACEHOLDER: preferred mixing board model]
- [PLACEHOLDER: plugin chain names if using OBS filters]
