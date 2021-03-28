from fei.ppds import Mutex, Semaphore, Thread


class Shared:
    def __init__(self):
        self.police_count = 0
        self.criminals_count = 0
        self.mutex = Mutex()
        self.police_sem = Semaphore(0)
        self.criminals_sem = Semaphore(0)


def board():
    pass


def row_boat():
    pass


def police(id):
    pass


def criminal(id):
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
