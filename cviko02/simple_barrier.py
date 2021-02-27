from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex, Event

"""Vypisovat na monitor budeme pomocou funkcie 'print'
   importovanej z modulu 'ppds'.
   To kvoli tomu, aby neboli 'rozbite' vypisy.
"""
from fei.ppds import print


class SimpleBarrierSemaphore:
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


class SimpleBarrierEvent:
    def __init__(self, size):
        self.size = size
        self.mutex = Mutex()
        self.event = Event()
        self.cnt = 0

    def wait(self):
        self.mutex.lock()
        self.cnt += 1
        if self.cnt == self.size:
            self.cnt = 0
            self.event.signal()
        self.mutex.unlock()
        self.event.wait()
        self.event.clear()


def barrier_example(barrier, thread_id):
    """Predpokladajme, ze nas program vytvara a spusta 5 vlakien,
    ktore vykonavaju nasledovnu funkciu, ktorej argumentom je
    zdielany objekt jednoduchej bariery
    """
    sleep(randint(1, 10) / 10)
    print("vlakno %d pred barierou" % thread_id)
    barrier.wait()
    print("vlakno %d po bariere" % thread_id)


# priklad pouzitia ADT SimpleBarrier
if __name__ == '__main__':
    sb = SimpleBarrierEvent(5)

    for _ in range(20):
        threads = []
        for i in range(5):
            threads.append(Thread(barrier_example, sb, i))

        for t in threads:
            t.join()
