from datetime import datetime, timedelta, timezone

from scripts.live_director_agent import LiveDirectorAgent


def test_live_director_switch():
    agent = LiveDirectorAgent(scene_map={'host': 'SceneHost', 'guest': 'SceneGuest'}, threshold_db=-40, cooldown_seconds=5)
    now = datetime(2024, 1, 1, tzinfo=timezone.utc)
    levels = {'host': -20.0, 'guest': -35.0}
    decision = agent.decide_switch(levels, now=now)
    assert decision.reason == 'switch'
    assert decision.scene == 'SceneHost'
    # cooldown prevents rapid switch
    levels2 = {'guest': -15.0, 'host': -30.0}
    decision2 = agent.decide_switch(levels2, now=now + timedelta(seconds=2))
    assert decision2.reason == 'no_switch'
    # after cooldown, switch allowed
    decision3 = agent.decide_switch(levels2, now=now + timedelta(seconds=6))
    assert decision3.reason == 'switch'
    assert decision3.scene == 'SceneGuest'


def test_live_director_below_threshold():
    agent = LiveDirectorAgent(scene_map={'host': 'SceneHost'}, threshold_db=-10, cooldown_seconds=1)
    levels = {'host': -20.0}
    decision = agent.decide_switch(levels)
    assert decision.reason == 'no_switch'
