# Humor Model Fine-Tuning (Local GPU)

## Goal
Train a local humor classifier that scores transcript segments as funny/not funny so clips can be ranked with show-specific taste.

## Hardware
- RTX 3060 works best with LoRA fine-tuning on small/medium models.
- Use Python 3.11 for PyTorch compatibility.

## Setup (One-Time)
```bash
python3.11 -m venv .venv-ml
source .venv-ml/bin/activate
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements-ml.txt
```

## Labeling Data
Use `docs/templates/humor_labels.csv` as the template. Minimum fields:
- `text`: transcript snippet
- `label`: 1 for funny, 0 for not funny

Tip: 200-500 labeled clips from your own show are more useful than large generic datasets.

## Training (LoRA by default)
```bash
python scripts/humor_finetune.py \
  --local_dataset docs/templates/humor_labels.csv \
  --hf_dataset jayavibhav/urfunnyv2_transcripts \
  --output_dir models/humor_classifier
```

Or use the config file:
```bash
python scripts/humor_finetune.py --config configs/humor_training.json
```

To full fine-tune (no LoRA):
```bash
python scripts/humor_finetune.py \
  --local_dataset docs/templates/humor_labels.csv \
  --output_dir models/humor_classifier \
  --full_finetune
```

Outputs are saved to `models/humor_classifier` with:
- `training_summary.json`
- `label_map.json`
- `humor_model_card.md`

## Scoring Clips
```bash
python scripts/humor_score.py \
  --model_dir models/humor_classifier \
  --input downloads/episode.vtt \
  --output exports/humor_scores.json
```

The output JSON includes `humor_score` per segment for downstream ranking.

## Notes
- Prefer `distilroberta-base` or `deberta-v3-small` for RTX 3060.
- If VRAM is tight, reduce `--batch_size` and `--max_length`.
- The model learns your show’s humor best when your labeled data is included.
