"""Minimal local stub for googleapiclient.discovery to make tests deterministic.
This stub will be monkeypatched by tests that need to replace `build`.
"""

def build(service, version, credentials=None):
    """Return a minimal dummy object that has the expected `videos().insert()` API used in tests.
    Tests will typically monkeypatch this function; providing a minimal stable object avoids import-time issues.
    """
    class DummyVideos:
        def __init__(self, result):
            self._result = result

        def insert(self, part, body, media_body):
            class DummyReq:
                def __init__(self, result):
                    self._result = result

                def execute(self):
                    return self._result

            return DummyReq({'id': 'LOCAL-DUMMY'})

    class DummyYouTube:
        def __init__(self):
            self._videos = DummyVideos({'id': 'LOCAL-DUMMY'})

        def videos(self):
            return self._videos

    return DummyYouTube()
