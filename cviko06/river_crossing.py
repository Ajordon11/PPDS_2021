from time import sleep

from fei.ppds import Mutex, Semaphore, Thread, print, randint


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
        self.mutex = Semaphore(1)
        self.police_sem = Semaphore(0)
        self.criminal_sem = Semaphore(0)
        self.barrier = SimpleBarrier(4)
        self.cruise_num = 0
        self.cruise_lock = Mutex()


def board(crew):
    # boarding takes some time
    sleep(0.4 + randint(0, 10) / 10)
    print(f'New passenger aboard: {crew}')


def row_boat(crew, captain, shared):
    print(f'Boat {shared.cruise_num} is on the move, crew: {crew}, captain: {captain}')
    print()
    shared.cruise_lock.lock()
    shared.cruise_num += 1
    shared.cruise_lock.unlock()
    sleep(0.8 + randint(0, 10) / 10)


def police(id, shared):
    isCaptain = False
    crew = ''
    while True:
        shared.mutex.wait()
        shared.police_count += 1
        print(f'Policeman {id} ready to board the ship.')

        if shared.police_count == 4:
            isCaptain = True
            shared.police_count = 0
            shared.police_sem.signal(4)
            crew = 'only police'

        elif shared.police_count == 2 and shared.criminal_count == 2:
            isCaptain = True
            shared.police_count = 0
            shared.police_sem.signal(2)

            shared.criminal_count -= 2
            shared.criminal_sem.signal(2)

            crew = 'mixed'

        else:
            shared.mutex.signal()

        shared.police_sem.wait()
        print(f'Policeman {id} is boarding the ship.')
        board(f'Policeman {id}')
        shared.barrier.wait()

        if isCaptain:
            print(f'Policeman {id} is the captain of this cruise.')
            row_boat(crew, f'Policeman {id}', shared)
            shared.mutex.signal()


def criminal(id, shared):
    isCaptain = False
    crew = ''
    while True:
        shared.mutex.wait()
        shared.criminal_count += 1
        print(f'Criminal {id} ready to board the ship.')

        if shared.criminal_count == 4:
            isCaptain = True
            shared.criminal_count = 0
            shared.criminal_sem.signal(4)
            crew = 'only criminals'

        elif shared.police_count == 2 and shared.criminal_count == 2:
            isCaptain = True
            shared.criminal_count = 0
            shared.criminal_sem.signal(2)

            shared.police_count -= 2
            shared.police_sem.signal(2)

            crew = 'mixed'

        else:
            shared.mutex.signal()

        shared.criminal_sem.wait()
        print(f'Criminal {id} is boarding the ship.')
        board(f'Criminal {id}')
        shared.barrier.wait()

        if isCaptain:
            print(f'Criminal {id} is the captain of this cruise.')
            row_boat(crew, f'Criminal {id}', shared)
            shared.mutex.signal()


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
