#!/usr/bin/env python3
"""Thumbnail renderer skeleton - creates a simple placeholder image file (or text) as thumbnail output.
"""
from pathlib import Path


def render_thumbnail(frame_path: str, overlay_text: str, output_path: str) -> dict:
    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    # create a placeholder file to represent thumbnail
    try:
        from PIL import Image, ImageDraw, ImageFont  # type: ignore

        img = Image.new("RGB", (1280, 720), color=(40, 40, 40))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 64)
        except Exception:
            font = ImageFont.load_default()
        text = overlay_text[:60]
        w, h = draw.textsize(text, font=font)
        draw.text(((1280 - w) / 2, (720 - h) / 2), text, font=font, fill=(255, 255, 255))
        img.save(p)
        return {"thumbnail_path": str(p)}
    except Exception:
        # fallback to text placeholder
        p.write_text(f"Thumbnail for {frame_path} - {overlay_text}\n")
        return {"thumbnail_path": str(p)}
