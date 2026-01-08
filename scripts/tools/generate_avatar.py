#!/usr/bin/env python3
"""Scaffold to create avatar images and short talking videos from audio and a photo.

Options:
- static avatars: use SD + prompt engineering
- talking avatars: D-ID, Synthesia, First-Order-Motion + audio
- lip sync: Wav2Lip + face tracking
"""

import os

API_KEY = os.getenv("AVATAR_API_KEY")


def generate_static_avatar(prompt: str):
    """Return an avatar image given a text prompt."""
    # TODO: call SD or similar
    raise NotImplementedError


def generate_talking_avatar(image_bytes: bytes, audio_bytes: bytes):
    """Return video bytes of a talking avatar. Use D-ID / First-Order-Motion / custom pipeline."""
    # TODO: implement with chosen provider
    raise NotImplementedError


if __name__ == "__main__":
    print("Placeholder: avatar generation not implemented yet")
