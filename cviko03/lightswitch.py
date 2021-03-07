from time import sleep
from random import randint
from fei.ppds import Mutex, Semaphore, Thread, print


class Lightswitch:
    def __init__(self):
        self.counter = 0
        self.mutex = Mutex()

    def lock(self, semaphore: Semaphore()):
        self.mutex.lock()
        self.counter += 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.unlock()

    def unlock(self, semaphore: Semaphore()):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()


class SharedData:
    def __init__(self):
        self.switch = Lightswitch()
        self.semaphore = Semaphore(1)
        self.turnstile = Semaphore(1)


def writer_thread(thread_id, shared):
    while True:
        shared.turnstile.wait()
        sleep(randint(0, 10) / 10)
        print(f'{thread_id} before wait...')
        shared.semaphore.wait()
        # priemerna dlzka zapisu - 0.5s
        sleep(randint(0, 10) / 10)
        shared.semaphore.signal()
        shared.turnstile.signal()
        print(f'{thread_id} after wait...')


def reader_thread(thread_id, shared: SharedData):
    while True:
        shared.turnstile.wait()
        shared.turnstile.signal()
        sleep(randint(0, 10) / 10)
        print(f'{thread_id} before wait...')
        shared.switch.lock(shared.semaphore)
        # priemerna dlzka citania - 0.5s
        sleep(randint(0, 10) / 10)
        shared.switch.unlock(shared.semaphore)
        print(f'{thread_id} after wait...')


if __name__ == '__main__':
    data = SharedData()
    threads = []

    for i in range(10):
        threads.append(Thread(reader_thread, f'Reader n.{i}', data))
    threads.append(Thread(writer_thread, f'Writer', data))
