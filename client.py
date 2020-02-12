# https://pypi.org/project/websocket_client/

import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time

from concurrent.futures import ThreadPoolExecutor

connections = []

run_loop_executor = ThreadPoolExecutor(100)

FILE_PATH = "/Users/aaron/lofi.zip"

# 5K buffer per connection
BUFFER_PER_CONNECTION = (1024 * 5)


def run_loop(ws):
    ws.run_forever()


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print("opened")


def create_100_connections():
    for i in range(0, 100):
        ws = websocket.WebSocketApp("ws://127.0.0.1:13254",
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        ws.on_open = on_open
        run_loop_executor.submit(run_loop, (ws))
        connections.append(ws)
    print("connections: ", len(connections))


packages = []


def unpack_file():
    f = open(FILE_PATH, "rb")
    content = f.read()
    print("len: ", len(content))
    f.close

    seq = 0
    b = bytearray(b"%d|" % seq)
    global packages
    for i in range(0, len(content)):
        m = i % BUFFER_PER_CONNECTION
        if m == 0 and i != 0:
            b.append(content[i])
            packages.append(b)
            seq += 1
            b = bytearray(b"%d|" % seq)
        elif i == len(content) - 1:
            b.append(content[i])
            a = bytearray(b"end")
            a.extend(b)
            packages.append(a)
        elif m < BUFFER_PER_CONNECTION:
            b.append(content[i])
    # For test
    # f = open("/Users/aaron/lofi_gen.zip", "wb")
    # f.write(b)
    # f.close


def get_package_seq(package):
    seq = ""
    for i in range(0, len(package)):
        c = chr(package[i])
        if c == '|':
            return seq
        else:
            seq += c


def get_package_content(package):
    seq = get_package_seq(package)
    l = len(seq) + 1
    return package[l:]


def pack_file():
    global packages
    packages_dict = {}
    for p in packages:
        seq = get_package_seq(p)
        if seq[0:3] != "end":
            seq = int(seq)
        else:
            seq = int(seq[3:])
        packages_dict[seq] = p

    content = bytearray()
    for i in range(0, len(packages)):
        p = packages_dict[i]
        p_content = get_package_content(p)
        content.extend(p_content)

    # For test
    f = open("/Users/aaron/lofi_gen.zip", "wb")
    f.write(content)
    f.close


def send_file():
    unpack_file()


if __name__ == "__main__":
    # websocket.enableTrace(True)
    create_100_connections()
    unpack_file()
    pack_file()
    while True:
        time.sleep(1)
