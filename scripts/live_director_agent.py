"""Live director agent for OBS auto scene switching."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, Tuple


@dataclass
class SwitchDecision:
    speaker: Optional[str]
    scene: Optional[str]
    reason: str


class LiveDirectorAgent:
    def __init__(
        self,
        scene_map: Dict[str, str],
        threshold_db: float = -35.0,
        cooldown_seconds: int = 5,
    ) -> None:
        self.scene_map = scene_map
        self.threshold_db = threshold_db
        self.cooldown = timedelta(seconds=cooldown_seconds)
        self.active_speaker: Optional[str] = None
        self.last_switch_at: Optional[datetime] = None

    def decide_active_speaker(self, levels_db: Dict[str, float]) -> Optional[str]:
        if not levels_db:
            return None
        best_speaker, best_level = max(levels_db.items(), key=lambda item: item[1])
        if best_level < self.threshold_db:
            return None
        return best_speaker

    def should_switch(self, speaker: Optional[str], now: datetime) -> bool:
        if speaker is None:
            return False
        if speaker == self.active_speaker:
            return False
        if self.last_switch_at and now - self.last_switch_at < self.cooldown:
            return False
        return True

    def decide_switch(self, levels_db: Dict[str, float], now: Optional[datetime] = None) -> SwitchDecision:
        now = now or datetime.now(timezone.utc)
        speaker = self.decide_active_speaker(levels_db)
        if not self.should_switch(speaker, now):
            return SwitchDecision(speaker=None, scene=None, reason='no_switch')
        scene = self.scene_map.get(speaker)
        if not scene:
            return SwitchDecision(speaker=None, scene=None, reason='missing_scene')
        self.active_speaker = speaker
        self.last_switch_at = now
        return SwitchDecision(speaker=speaker, scene=scene, reason='switch')

    def switch_scene(self, obs_client, scene: str) -> None:
        """Call an OBS client method to switch scenes.

        The obs_client must provide set_current_scene(scene_name).
        """
        if hasattr(obs_client, 'set_current_scene'):
            obs_client.set_current_scene(scene)
        elif hasattr(obs_client, 'switch_to'):
            obs_client.switch_to(scene)
        else:
            raise AttributeError('obs_client missing scene switch method')
