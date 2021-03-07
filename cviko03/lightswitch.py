from fei.ppds import Mutex


class Lightswitch:
    def __init__(self):
        self.counter = 0
        self.mutex = Mutex()

    def lock(self):
        pass

    def unlock(self):
        pass


if __name__ == '__main__':
    ls = Lightswitch()
