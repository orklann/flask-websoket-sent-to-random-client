from concurrent.futures import ThreadPoolExecutor
from time import sleep


def task(message):
    sleep(int(message))
    print(message)
    return message


futures = []


def test():
    print(futures[0].done())


def main():
    executor = ThreadPoolExecutor(6)
    for i in [5,  4, 3, 2, 1]:
        future = executor.submit(task, ("%d" % i))
        futures.append(future)
    test()
    sleep(10)
    test()


if __name__ == '__main__':
    main()
