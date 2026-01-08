#!/usr/bin/env python
import argparse
import json
import os

def generate_metadata(episode_id, guest, output_file):
    """
    Generates metadata for a podcast episode.

    This is a placeholder implementation. It generates a dummy JSON file.
    """
    print(f"Generating metadata for episode: {episode_id}")
    print(f"Guest: {guest}")
    print(f"Outputting metadata to: {output_file}")

    # Dummy metadata
    metadata = {
        "episode_id": episode_id,
        "title": f"Episode {episode_id.split('_')[0]} ft. {guest}",
        "description": f"A fascinating conversation with {guest} about everything and nothing.",
        "tags": ["podcast", "comedy", "interview", guest],
        "publish_date": "2026-01-07T12:00:00Z"
    }

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Write the dummy JSON output
    with open(output_file, 'w') as f:
        json.dump(metadata, f, indent=4)

    print(f"Successfully generated dummy metadata file: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate episode metadata.")
    parser.add_argument("--episode-id", required=True, help="The ID of the episode.")
    parser.add_argument("--guest", required=True, help="The name of the guest.")
    parser.add_argument("--output", required=True, help="Path to the output JSON metadata file.")

    args = parser.parse_args()

    generate_metadata(args.episode_id, args.guest, args.output)
