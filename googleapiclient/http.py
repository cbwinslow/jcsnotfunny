"""Minimal http stub for googleapiclient used by tests."""

class MediaFileUpload:
    def __init__(self, filepath, chunksize=256*1024, resumable=True, mimetype=None):
        self.filepath = filepath
        self.chunksize = chunksize
        self.resumable = resumable
        self.mimetype = mimetype

    def __repr__(self):
        return f"<MediaFileUpload {self.filepath}>" 
