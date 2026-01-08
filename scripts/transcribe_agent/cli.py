"""CLI wrapper for the transcription agent."""
import argparse
from scripts.transcribe_agent.agent import build_transcript_package


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', '-i', required=True)
    p.add_argument('--out', '-o', default='transcripts')
    p.add_argument('--no-diarize', action='store_true')
    p.add_argument('--no-emb', action='store_true')
    args = p.parse_args()

    res = build_transcript_package(args.input, args.out, do_diarize=not args.no_diarize, do_embeddings=not args.no_emb)
    print('Done. Outputs:')
    for k, v in res.items():
        print(k, v)


if __name__ == '__main__':
    main()
