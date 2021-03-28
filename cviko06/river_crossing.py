from fei.ppds import Mutex


class Shared:
    def __init__(self):
        self.police_count = 0
        self.criminal_count = 0
        self.mutex = Mutex()


def board():
    pass


def row_boat():
    pass


if __name__ == '__main__':
    pass
