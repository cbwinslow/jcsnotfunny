"""Transcript validators"""
import re


def validate_vtt(path):
    errors = []
    with open(path, 'r', encoding='utf-8') as fh:
        text = fh.read()
    if not text.startswith('WEBVTT'):
        errors.append('Missing WEBVTT header')
    # basic timestamp pattern check
    ts_re = re.compile(r"\d{2}:\d{2}:\d{2}[\.,]\d{3}\s-->\s\d{2}:\d{2}:\d{2}[\.,]\d{3}")
    if not ts_re.search(text):
        errors.append('No valid timestamp lines found')
    return (len(errors) == 0, errors)
