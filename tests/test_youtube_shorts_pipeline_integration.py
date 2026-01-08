import json
from pathlib import Path

from scripts.youtube_shorts_pipeline import YouTubeShortsPipeline


def test_youtube_shorts_pipeline_integration_dry_run(tmp_path, monkeypatch):
    out_dir = tmp_path / "out"
    out_dir.mkdir()

    # Create a fake video file
    video_file = out_dir / "original_video.mp4"
    video_file.write_bytes(b"VIDEO")

    # Create a fake transcript file
    vtt_file = out_dir / "transcript.vtt"
    vtt_file.write_text("WEBVTT\n\n00:00.000 --> 00:06.000\nHa ha\n")

    # Monkeypatch YouTubeShortsPipeline.__init__ to avoid instantiating real agents
    from types import SimpleNamespace

    def fake_init(self):
        self.video_agent = SimpleNamespace(execute_tool=lambda name, params=None: {
            "download_video": {"video_path": str(video_file), "title": "Test Video", "duration": 60, "file_size": 1234},
            "extract_audio": {"output_audio": str(out_dir / "audio.mp3")},
            "trim_video": {"output_video": str(out_dir / "funny_clips" / "short_001.mp4"), "duration": 6}
        }.get(name, {}))

        self.transcription_agent = SimpleNamespace(execute_tool=lambda name, params=None: {
            "transcribe_audio": {"vtt_file": str(vtt_file), "json_file": str(out_dir / "transcript.json"), "transcript": "Ha ha\nLol", "duration": 60}
        }.get(name, {}))

        def fake_analyze(name, params=None):
            return {
                "funny_segments": [
                    {"start_time": 0, "end_time": 6, "text": "Ha ha", "funny_score": 0.7},
                    {"start_time": 30, "end_time": 36, "text": "Lol", "funny_score": 0.8},
                ],
                "total_segments": 2,
                "analysis_method": "fake"
            }

        self.funny_moment_agent = SimpleNamespace(execute_tool=lambda name, params=None: fake_analyze(name, params))

    monkeypatch.setattr(YouTubeShortsPipeline, "__init__", fake_init)

    # Instantiate pipeline (with fake init)
    pipeline = YouTubeShortsPipeline()

    # Monkeypatch internal methods for download/transcribe (not strictly necessary but keep for clarity)
    monkeypatch.setattr(pipeline, "_download_youtube_video", lambda url, out: {"video_path": str(video_file), "title": "Test Video", "duration": 60, "file_size": 1234, "url": url})
    monkeypatch.setattr(pipeline, "_transcribe_video", lambda vp, od: {"audio_file": str(out_dir / "audio.mp3"), "vtt_file": str(vtt_file), "json_file": str(out_dir / "transcript.json"), "transcript": "Ha ha\nLol", "duration": 60})

    # Run pipeline in dry-run mode
    report = pipeline.run_pipeline("https://youtube.fake/watch?v=1", str(out_dir), min_clip_duration=5.0, max_clip_duration=30.0, dry_run=True)

    # Assert EDL and clips were created
    edl_path = Path(report["clips_created"]["clips_info_file"]) if report.get("clips_created") else Path(out_dir / "edl.json")
    assert edl_path.exists(), "EDL JSON was not written"

    edl = json.loads(edl_path.read_text())
    assert edl.get("count", 0) >= 1

    clips_dir = out_dir / "funny_clips"
    assert clips_dir.exists()
    files = list(clips_dir.glob("short_*.mp4"))
    assert len(files) == edl.get("count", 0)
    for f in files:
        assert f.stat().st_size > 0

    # If CI wants artifacts uploaded, copy outputs into ./outputs
    import os
    import shutil

    if os.getenv("WRITE_OUTPUTS"):
        outputs = Path("outputs")
        outputs.mkdir(exist_ok=True)
        shutil.copy(edl_path, outputs / edl_path.name)
        out_clips = outputs / "funny_clips"
        out_clips.mkdir(exist_ok=True)
        for f in files:
            shutil.copy(f, out_clips / f.name)
        # Basic assertion to ensure artifacts were written
        assert (outputs / edl_path.name).exists()
        assert len(list(out_clips.glob("short_*.mp4"))) == len(files)
