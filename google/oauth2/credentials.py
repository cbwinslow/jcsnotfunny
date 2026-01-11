"""Simple Credentials stub for tests."""

class Credentials:
    def __init__(self, token=None, **kwargs):
        self.token = token

    def __repr__(self):
        return f"<Credentials token={'***' if self.token else None}>"
