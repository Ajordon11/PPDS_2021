from time import sleep

from fei.ppds import Mutex, Semaphore, randint, Thread, print


class LightswitchMod:
    def __init__(self):
        self.counter = 0
        self.mutex = Mutex()

    def lock(self, semaphore: Semaphore()):
        self.mutex.lock()
        self.counter += 1
        if self.counter == 1:
            semaphore.wait()
        current = self.counter
        self.mutex.unlock()
        return current

    def unlock(self, semaphore: Semaphore()):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()


class Shared:
    def __init__(self):
        self.accessData = Semaphore(1)
        self.turnstile = Semaphore(1)
        self.ls_cidlo = LightswitchMod()
        self.validData = Semaphore(0)


def cidlo(shared, cidlo_id, typ):
    while True:
        # check every 50-60ms
        sleep(randint(50, 60) / 1000)
        # sensors are going through turnstile until monitor stops them
        shared.turnstile.wait()
        shared.turnstile.signal()

        # get number of active monitors (current counter in Lightswitch)
        num_active_sensors = shared.ls_cidlo.lock(shared.accessData)

        # write time according to assignment
        if typ == 'H':
            write_time = randint(20, 25) / 1000
        else:
            write_time = randint(10, 20) / 1000

        if num_active_sensors == 3:
            # all sensors active, signalize monitors to start
            shared.validData.signal(8)
        print(
            f'cidlo {cidlo_id}:  pocet_zapisujucich_cidiel={num_active_sensors}, '
            f'trvanie_zapisu={write_time} typ {typ}')
        sleep(write_time)
        shared.ls_cidlo.unlock(shared.accessData)


def monitor():
    pass


if __name__ == '__main__':
    pass
