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
        print(i)
    print("connections: ", len(connections))


if __name__ == "__main__":
    # websocket.enableTrace(True)
    create_100_connections()

    while True:
        time.sleep(1)
