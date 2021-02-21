import sys
from fei.ppds import Thread, Mutex


class Shared:
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.elms = [0] * end
        self.mutex = Mutex()

    def print_histogram(self):
        hist = {}
        for el in self.elms:
            hist[el] = hist.get(el, 0) + 1
        print(hist)


def counter1(shared):
    """ Counter 1

        Pouzitie zamku po tom ako sa pristupi k urcitemu prvku v poli
        zabrani problemu s pretecenim pola, ale nezabrani pripadnemu
        viacnasobnemu pristupu k jednemu prvku.

        Pravdepodobna pricina: t1 sa posunie na novu poziciu v poli,
        pred uzamknutim aj t2 zvysi poziciu -> preskoci sa jedno miesto v poli,
        potom sa postupne uzamknu zamky a pripocita counter pre oba thready
    """
    while True:
        if shared.counter >= shared.end:
            break
        shared.elms[shared.counter] += 1
        shared.mutex.lock()
        shared.counter += 1
        shared.mutex.unlock()


def counter2(shared):
    """ Counter 2

        Tento sposob je pravdepodobnejsie najbezpecnejsi s tym, ze zaroven zachovava
        principy paralelneho programovania. Unlock je potrebne pouzit na dvoch miestach,
        pretoze pri skonceni pocitania by sa inak nikdy neuvolnil.

        Pri pouzivani zamku na tychto miestach proces zlyhal (nepracoval ako mal) len v malo pripadoch,
        ale stale tu bola moznost chyby.
    """
    while True:
        shared.mutex.lock()
        if shared.counter >= shared.end:
            shared.mutex.unlock()
            break
        shared.mutex.unlock()
        shared.elms[shared.counter] += 1
        shared.counter += 1


def counter3(shared):
    """ Counter 3

        Najbezpecnejsia varianta, ktora uzamkne zamok pocas celeho procesu,
        v ktorom sa manipuluje s datami v zdielanej triede. Nedochadza tu
        k ziadnej "mutacii" ani sucasnemu pristupu, ale tak isto to aj prestava
        byt paralelny proces, kedze stale jeden thread caka kym svoju pracu dokonci 2.
        Z tohto dovodu je tento sposob aj najpomalsi.
    """
    while True:
        shared.mutex.lock()
        if shared.counter >= shared.end:
            shared.mutex.unlock()
            break
        shared.elms[shared.counter] += 1
        shared.counter += 1
        shared.mutex.unlock()


def main():
    for _ in range(10):
        sh = Shared(1000000)
        t1 = Thread(counter2, sh)
        t2 = Thread(counter2, sh)

        t1.join()
        t2.join()

        sh.print_histogram()


if __name__ == '__main__':
    sys.exit(main() or 0)
