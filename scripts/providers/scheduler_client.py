"""Scheduler client stub (Buffer / Hootsuite / Later)

Provides an abstraction for scheduling posts to multiple platforms. The
implementation should use the provider's API and handle scheduling/rescheduling.
"""
import os
import logging

logger = logging.getLogger('scheduler_client')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(ch)

class SchedulerClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('SCHEDULER_API_KEY')

    def schedule(self, platform, text, when):
        logger.info('Scheduling to %s at %s: %s', platform, when, text[:120])
        # TODO: implement actual scheduling calls
        return {'scheduled_at': when, 'platform': platform, 'status': 'scheduled'}
