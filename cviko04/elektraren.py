"""
Cvicenie 4 - Atomova elektraren 2
"""

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
        self.ls_monitor = LightswitchMod()
        self.ls_cidlo = LightswitchMod()
        self.validData = Semaphore(0)


def cidlo(shared, cidlo_id, typ):
    while True:
        # check every 50-60ms
        sleep(randint(50, 60) / 1000)
        # sensors are going through turnstile until monitor stops them
        shared.turnstile.wait()
        shared.turnstile.signal()

        # get number of active sensors (current counter in Lightswitch)
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
            f'trvanie_zapisu={write_time} typ {typ}'
        )
        sleep(write_time)
        shared.ls_cidlo.unlock(shared.accessData)


def monitor(shared, monitor_id):
    while True:
        # block until sensors are finished
        shared.validData.wait()
        shared.turnstile.wait()

        # get number of active monitors (current counter in Lightswitch)
        num_active_monitors = shared.ls_monitor.lock(shared.accessData)

        shared.turnstile.signal()
        # simulate data access
        read_time = randint(40, 50) / 1000
        print(
            f'monit {monitor_id}: pocet_citajucich_monitorov={num_active_monitors} '
            f'trvanie_citania:{read_time}'
        )
        sleep(read_time)
        shared.ls_monitor.unlock(shared.accessData)


if __name__ == '__main__':
    num_sensors = 3
    num_monitors = 8
    shared_data = Shared()
    sensor_types = ['P', 'T', 'H']
    monitory = [Thread(monitor, shared_data, i) for i in range(num_monitors)]
    sensors = [Thread(cidlo, shared_data, i, sensor_types[i]) for i in range(num_sensors)]
