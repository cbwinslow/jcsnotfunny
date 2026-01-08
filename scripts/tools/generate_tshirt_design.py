#!/usr/bin/env python3
"""Generate t-shirt design concepts using an image-generation backend.

Placeholder scaffold: implement a call to stable-diffusion / stable api / dreamstudio.
"""

import os
from typing import List

API_KEY = os.getenv("IMAGE_API_KEY")


def generate_design(prompt: str, width: int = 1024, height: int = 1024) -> bytes:
    """Return PNG bytes of generated design. Implement the image generation call here."""
    # TODO: call Stable Diffusion / API and return image bytes
    raise NotImplementedError("Implement call to image generation API")


if __name__ == "__main__":
    sample_prompt = "Retro comic style t-shirt design: Jared's Not Funny, bold text, limited palette"
    print("Placeholder: generate_design not implemented. Prompt:", sample_prompt)
