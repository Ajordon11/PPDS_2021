"""
todo
Cvicenie 3 - Problem Citatelia-Zapisovatelia pomocou ADT Lightswitch

Implementacia:


Odpovede:
    5. Pre aký počet čitateľov s danou priemernou dobou čítania
     sa prejavuje problém vyhladovenia?
     -

    7. Je možné, aby sa prejavilo vyhladovenie aj u čitateľov?
     -

    9. Pre daný počet čitateľov, priemernú dobu čítania, priemernú dobu
     zápisu vieme určit optimálny počet zapisovateľov?
     -
"""

from time import sleep
from random import randint
from fei.ppds import Mutex, Semaphore, Thread, print
import matplotlib.pyplot as plt


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
        self.mutex = Mutex()
        self.results_reads = []
        self.results_writes = []


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
        shared.mutex.lock()
        shared.n_writes += 1
        shared.mutex.unlock()
        # print(f'{thread_id} after write, n.{shared.n_writes}')


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
        shared.mutex.lock()
        shared.n_reads += 1
        shared.mutex.unlock()
        # print(f'{thread_id} after read, n.{shared.n_reads}')


def stop_thread(time, shared: SharedData):
    sleep(time)
    shared.finished_flag = True
    print(f'immediate results-> reads: {shared.n_reads},'
          f' writes: {shared.n_writes}')
    shared.results_reads.append(shared.n_reads)
    shared.results_writes.append(shared.n_writes)
    shared.n_writes = 0
    shared.n_reads = 0


def plot(reads: list, writes: list, writers):
    plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_xlabel('Pocet zapisovatelov')
    ax.set_ylabel('Pocet zapisov')
    ax.set_zlabel('Pocet citani')
    # writers are incremented by 1
    x = list(range(1, writers + 1))
    ax.plot_trisurf(x, writes, reads, cmap='viridis', edgecolor='none')
    plt.show()


if __name__ == '__main__':
    data = SharedData()
    max_writers = 20
    n_readers = 10

    for i in range(max_writers):
        threads = []
        data.finished_flag = False
        for j in range(n_readers):
            threads.append(Thread(reader_thread, f'Reader n.{j}', data))

        for k in range(1, i + 1):
            threads.append(Thread(writer_thread, f'Writer n.{k}', data))
        threads.append(Thread(stop_thread, 1, data))
        for t in threads:
            t.join()

    print(f'final reads: {data.results_reads}')
    print(f'final writes: {data.results_writes}')
    plot(data.results_reads, data.results_writes, max_writers)
