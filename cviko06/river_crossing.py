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
        self.criminal_count = 0
        self.mutex = Mutex()
        self.police_sem = Semaphore(0)
        self.criminal_sem = Semaphore(0)
        self.barrier = SimpleBarrier(4)


def board():
    pass


def row_boat():
    pass


def police(id, shared):
    isCaptain = False
    while True:
        shared.mutex.lock()
        shared.police_count += 1
        print(f'Policeman {id} ready to board.')

        if shared.police_count == 4:
            isCaptain = True
            shared.police_count = 0
            shared.police_sem.signal(4)

        elif shared.police_count == 2 and shared.criminal_count == 2:
            isCaptain = True
            shared.police_count = 0
            shared.police_sem.signal(2)

            shared.criminal_count -= 2
            shared.criminal_sem.signal(2)

        else:
            shared.mutex.unlock()

        shared.police_sem.wait()
        print(f'Policeman {id} is boarding the ship.')
        board()
        shared.barrier.wait()

        if isCaptain:
            print(f'Policeman {id} is the captain of this cruise.')
            row_boat()
            shared.mutex.unlock()


def criminal(id, shared):
    isCaptain = False
    while True:
        shared.mutex.lock()
        shared.criminal_count += 1
        print(f'Criminal {id} ready to board.')

        if shared.criminal_count == 4:
            isCaptain = True
            shared.criminal_count = 0
            shared.criminal_sem.signal(4)

        elif shared.police_count == 2 and shared.criminal_count == 2:
            isCaptain = True
            shared.criminal_count = 0
            shared.criminal_sem.signal(2)

            shared.police_count -= 2
            shared.police_sem.signal(2)

        else:
            shared.mutex.unlock()

        shared.criminal_sem.wait()
        print(f'Criminal {id} is boarding the ship.')
        board()
        shared.barrier.wait()

        if isCaptain:
            print(f'Criminal {id} is the captain of this cruise.')
            row_boat()
            shared.mutex.unlock()


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
