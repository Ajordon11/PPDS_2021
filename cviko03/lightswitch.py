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
        self.n_reads = 0
        self.n_writes = 0
        self.finished_flag = False


def writer_thread(thread_id, shared):
    while True:
        # stop if process is finished (for testing purposes)
        if shared.finished_flag:
            break
        shared.turnstile.wait()
        sleep(randint(0, 10) / 10)
        shared.semaphore.wait()

        # average write time - 0.5s
        sleep(randint(0, 10) / 10)
        shared.semaphore.signal()
        shared.turnstile.signal()

        # increase number of successful writes
        shared.n_writes += 1
        print(f'{thread_id} after write, n.{shared.n_writes}')


def reader_thread(thread_id, shared: SharedData):
    while True:
        # stop if process is finished (for testing purposes)
        if shared.finished_flag:
            break
        shared.turnstile.wait()
        shared.turnstile.signal()

        sleep(randint(0, 10) / 10)
        shared.switch.lock(shared.semaphore)

        # average read time - 0.5s
        sleep(randint(0, 10) / 10)
        shared.switch.unlock(shared.semaphore)

        # increase number of successful reads
        shared.n_reads += 1
        print(f'{thread_id} after read, n.{shared.n_reads}')


if __name__ == '__main__':
    data = SharedData()
    threads = []

    for i in range(10):
        threads.append(Thread(reader_thread, f'Reader n.{i}', data))
    threads.append(Thread(writer_thread, f'Writer', data))
