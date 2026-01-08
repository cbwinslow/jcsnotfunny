"""Generate synthetic audio fixtures and expected transcript/diarization files for tests."""
import wave
import math
import struct
from pathlib import Path
import json

OUT = Path(__file__).parent

def generate_tone(path: Path, freq: float, duration: float=1.0, rate: int=16000, amplitude=16000):
    n_samples = int(rate * duration)
    with wave.open(str(path), 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        for i in range(n_samples):
            t = float(i) / rate
            val = int(amplitude * math.sin(2 * math.pi * freq * t))
            wf.writeframes(struct.pack('<h', val))


def generate_single_speaker():
    audio = OUT / 'single_speaker.wav'
    generate_tone(audio, 440.0, duration=1.0)
    vtt = OUT / 'single_speaker.vtt'
    vtt.write_text('WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nhello world\n')
    diar = OUT / 'single_speaker.diar.json'
    diar.write_text(json.dumps([{'start':0.0,'end':1.0,'speaker':'S0','confidence':1.0}]))


def generate_two_speaker():
    # 0.5s tone A then 0.5s tone B
    out = OUT / 'two_speaker.wav'
    rate = 16000
    with wave.open(str(out), 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        for freq, dur in [(440.0, 0.5), (660.0, 0.5)]:
            n_samples = int(rate * dur)
            for i in range(n_samples):
                t = float(i) / rate
                val = int(16000 * math.sin(2 * math.pi * freq * t))
                wf.writeframes(struct.pack('<h', val))
    vtt = OUT / 'two_speaker.vtt'
    vtt.write_text('WEBVTT\n\n00:00:00.000 --> 00:00:00.499\nfirst speaker\n\n00:00:00.500 --> 00:00:00.999\nsecond speaker\n')
    diar = OUT / 'two_speaker.diar.json'
    diar.write_text(json.dumps([
        {'start':0.0,'end':0.499,'speaker':'S0','confidence':1.0},
        {'start':0.5,'end':0.999,'speaker':'S1','confidence':1.0},
    ]))


def generate_all():
    OUT.mkdir(parents=True, exist_ok=True)
    generate_single_speaker()
    generate_two_speaker()


if __name__ == '__main__':
    generate_all()
    print('Fixtures generated in', OUT)
