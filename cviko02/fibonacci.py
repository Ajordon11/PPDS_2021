from fei.ppds import Mutex, Semaphore, Thread, Event


class Shared:
    def __init__(self, data):
        self.data = data
        self.mutex = Mutex()


class Fibonacci:
    """
        1) Aký je najmenší počet synchronizačných objektov (semafory, mutexy, udalosti)
         potrebných na riešenie tejto úlohy?
            - podla riesenia ktore som zostrojil je to 1 Mutex (lock - unlock) a 1 Semaphore / Event

        2) Ktoré z prebratých synchronizačných vzorov (vzájomné vylúčenie, signalizácia,
         rendezvous, bariéra) sa dajú (rozumne) využiť pri riešení tejto úlohy?
            - pri rieseni je nutne vyuzit signalizaciu, kedze kazdy nasledujuci thread moze vykonat
            svoju akciu (pocitanie dalsieho prvku) az po tom ako su vypocitane predchadzajuce prvky postupnosti
    """
    def __init__(self, n, tool=Semaphore()):
        self.n = n
        self.tool = tool
        self.shared = Shared([0, 1])  # 0, 1 su dane
        self.threads = [Thread(self.get_next, i) for i in range(self.n)]

    def get_next(self, i):
        self.shared.mutex.lock()
        self.shared.data.append(self.shared.data[-2] + self.shared.data[-1])
        self.tool.signal()
        self.shared.mutex.unlock()
        self.tool.wait()
        if isinstance(self.tool, Event):
            self.tool.clear()

    def activate_threads(self):
        for t in self.threads:
            t.join()
        print(self.shared.data)


if __name__ == '__main__':
    for _ in range(10):
        f = Fibonacci(100, Event())
        f.activate_threads()
