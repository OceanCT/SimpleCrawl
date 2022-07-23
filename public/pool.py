import queue


class Pool:
    def __init__(self, max_size=100):
        self.pool = queue.Queue(maxsize=max_size)

    def put(self, proxy):
        self.pool.put(proxy)

    def get(self):
        return None if self.pool.empty() else self.pool.get()
