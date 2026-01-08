import time
from agents.worker import Worker, Task, Executor


class DummyFetcher:
    def fetch_tasks(self):
        return [{'id': 't1', 'title': 'Test Task', 'body': 'Do thing', 'meta': {}}]


class DummyExec(Executor):
    def __init__(self):
        super().__init__(propose_only=True)
        self.processed = []

    def execute(self, task: Task):
        self.processed.append(task.id)
        return {'status': 'proposed', 'task_id': task.id}


def test_worker_run_once():
    fetcher = DummyFetcher()
    executor = DummyExec()
    w = Worker(fetcher=fetcher, executor=executor, poll_interval=0.1, propose_only=True)
    res = w.run_once()
    assert len(res) == 1
    assert executor.processed == ['t1']
