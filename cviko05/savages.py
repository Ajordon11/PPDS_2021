"""
Riesenie modifikovaneho problemu divochov.
"""

from fei.ppds import Semaphore, Mutex, Thread, print
from random import randint
from time import sleep

"""
Parametre modelu, nie synchronizacie ako takej.
Preto ich nedavame do zdielaneho objektu.
    n_servings - pocet porcii misionara, ktore sa zmestia do hrnca.
    n_savages - pocet divochov v kmeni (kuchara nepocitame).
    n_cooks - pocet kucharov
"""
n_servings = 5
n_savages = 12
n_cooks = 7


class SimpleBarrier:
    """
    Vlastna implementacia bariery
    kvoli specialnym vypisom vo funkcii wait().
    """

    def __init__(self, N):
        self.N = N
        self.mutex = Mutex()
        self.cnt = 0
        self.sem = Semaphore(0)

    def wait(self,
             print_str,
             savage_id,
             print_last_thread=False,
             print_each_thread=False):
        self.mutex.lock()
        self.cnt += 1
        if print_each_thread:
            print(print_str % (savage_id, self.cnt))
        if self.cnt == self.N:
            self.cnt = 0
            if print_last_thread:
                print(print_str % savage_id)
            self.sem.signal(self.N)
        self.mutex.unlock()
        self.sem.wait()


class Shared:
    """
    V tomto pripade musime pouzit zdielanu strukturu.
    Kedze Python struktury nema, pouzijeme triedu bez vlastnych metod.
    Preco musime pouzit strukturu? Lebo chceme zdielat hodnotu
    pocitadla servings, a to jednoduchsie v Pythone asi neurobime.
    Okrem toho je rozumne mat vsetky synchronizacne objekty spolu.
    Pri zmene nemusime upravovat API kazdej funkcie zvlast.
    """

    def __init__(self):
        self.mutex = Mutex()
        self.cook_mutex = Mutex()
        self.servings = 0
        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(0)
        self.barrier1 = SimpleBarrier(n_savages)
        self.barrier2 = SimpleBarrier(n_savages)
        self.eating = False


def get_serving_from_pot(savage_id, shared):
    """
    Pristupujeme ku zdielanej premennej.
    Funkcia je volana pri zamknutom mutexe,
    preto netreba riesit serializaciu v ramci
    samotnej funkcie.
    """

    print("divoch %2d: beriem si porciu" % savage_id)
    shared.servings -= 1


def eat(savage_id):
    print("divoch %2d: hodujem" % savage_id)
    # Zjedenie porcie misionara nieco trva...
    sleep(0.2 + randint(0, 3) / 10)


def savage(savage_id, shared):
    while True:
        """
        Pred kazdou hostinou sa divosi musia pockat.
        Kedze mame kod vlakna(divocha) v cykle,
        musime pouzit dve jednoduche bariery za sebou
        alebo jednu zlozenu, ale kvoli prehladnosti vypisov
        sme sa rozhodli pre toto riesenie.
        """
        shared.barrier1.wait(
            f'divoch %2d: prisiel som na veceru, uz nas je %2d',
            savage_id,
            print_each_thread=True)
        shared.barrier2.wait(f'divoch %2d: uz sme vsetci,',
                             savage_id,
                             print_last_thread=True)

        # Nasleduje klasicke riesenie problemu hodujucich divochov.
        shared.mutex.lock()
        shared.eating = True
        print("divoch %2d: pocet zostavajucich porcii v hrnci je %2d" %
              (savage_id, shared.servings))
        if shared.servings == 0:
            shared.eating = False
            print("divoch %2d: budim kuchara" % savage_id)
            shared.empty_pot.signal(n_cooks)
            shared.full_pot.wait()
            shared.eating = True
        shared.cook_mutex.lock()
        get_serving_from_pot(savage_id, shared)
        shared.cook_mutex.unlock()
        shared.mutex.unlock()
        eat(savage_id)


def put_servings_in_pot(cook_id, shared):
    """
    Hrniec je reprezentovany zdielanou premennou servings.
    Ta udrziava informaciu o tom, kolko porcii je v hrnci k dispozicii.
    """

    print(f'kuchar {cook_id}: varim')
    # navarenie jedla tiez cosi trva...
    sleep(0.4 + randint(0, 2) / 10)
    shared.cook_mutex.lock()
    if shared.servings >= n_servings or shared.eating:
        print(f'kuchar {cook_id}: vidi ze uz je plno a jedia, tak ide prec')
        shared.cook_mutex.unlock()
        return
    shared.servings += 1
    print(f'kuchar {cook_id}: navaril, pocet porcii v hrnci: {shared.servings}')
    shared.cook_mutex.unlock()


def cook(id,  shared):
    """
    Na strane kuchara netreba robit ziadne modifikacie kodu.
    Riesenie je standardne podla prednasky.
    Navyse je iba argument M, ktorym explicitne hovorime, kolko
    porcii ktory kuchar vari. Kedze v nasom modeli mame iba jedneho
    kuchara, ten navari vsetky potrebne porcie a vlozi ich do hrnca.
    """

    while True:
        shared.empty_pot.wait()
        put_servings_in_pot(id, shared)
        if shared.servings == n_servings and not shared.eating:
            print(f'kuchar {id}: vidi ze hrniec je plny a vola divochov')
            shared.full_pot.signal()
        else:
            shared.empty_pot.signal(n_cooks)


def init_and_run(savages, servings, cooks):
    """
    Spustenie modelu
    """
    threads = list()
    shared = Shared()
    for savage_id in range(0, savages):
        threads.append(Thread(savage, savage_id, shared))

    for cook_id in range(0, cooks):
        threads.append(Thread(cook, cook_id, servings, shared))

    for t in threads:
        t.join()


if __name__ == "__main__":
    init_and_run(n_savages, n_servings, n_cooks)
