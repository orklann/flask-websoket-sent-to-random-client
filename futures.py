from concurrent.futures import ThreadPoolExecutor
from time import sleep


def task(message):
    sleep(int(message))
    print(message)
    return message


def main():
    executor = ThreadPoolExecutor(6)
    for i in [5,  4, 3, 2, 1]:
        future = executor.submit(task, ("%d" % i))
        future
    sleep(10)


if __name__ == '__main__':
    main()
