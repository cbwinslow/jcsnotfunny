import os


def test_links_file_exists():
    assert os.path.exists("docs/links_and_channels.md")


def test_playbook_exists():
    assert os.path.exists("docs/growth/GROWTH_PLAYBOOK.md")


def test_channel_monitor_scaffold():
    assert os.path.exists("scripts/automation/channel_monitor.py")
