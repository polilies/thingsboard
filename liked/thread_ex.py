from time import sleep
from threading import Thread
from datetime import datetime


def func():
    connect()
    find_links()
    find_numbers()
    print(datetime.now())


if __name__ == '__main__':

    Thread(target = func).start()
    while True:
        sleep(3600)
        Thread(target = func).start()