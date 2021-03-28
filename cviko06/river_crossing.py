from fei.ppds import Mutex, Semaphore, Thread, print


class SimpleBarrier:
    def __init__(self, size):
        self.size = size
        self.mutex = Mutex()
        self.turnstile = Semaphore(0)
        self.cnt = 0

    def wait(self):
        self.mutex.lock()
        self.cnt += 1
        if self.cnt == self.size:
            self.cnt = 0
            self.turnstile.signal(self.size)
        self.mutex.unlock()
        self.turnstile.wait()


class Shared:
    def __init__(self):
        self.police_count = 0
        self.criminals_count = 0
        self.mutex = Mutex()
        self.police_sem = Semaphore(0)
        self.criminals_sem = Semaphore(0)
        self.barrier = SimpleBarrier(4)


def board():
    pass


def row_boat():
    pass


def police(id, shared):
    pass


def criminal(id, shared):
    pass


if __name__ == '__main__':
    threads = list()
    shared = Shared()
    police_members = 4
    criminals_members = 4

    for police_id in range(0, police_members):
        threads.append(Thread(police, police_id, shared))

    for criminal_id in range(0, criminals_members):
        threads.append(Thread(criminal, criminal_id, shared))

    for t in threads:
        t.join()
