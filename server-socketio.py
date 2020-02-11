# https://github.com/Pithikos/python-websocket-server

from flask import Flask, request
from flask_socketio import SocketIO

app = Flask(__name__, static_folder='')
io = SocketIO(app)

clients = []


@app.route('/')
def index():
    return app.send_static_file('client.html')


@io.on('connected')
def connected():
    print("%s connected" % (request.sid))
    clients.append(request.sid)


@io.on('disconnect')
def disconnect():
    print("%s disconnected" % (request.sid))
    clients.remove(request.sid)


def hello_to_random_client():
    import random
    from datetime import datetime
    if clients:
        print(clients)
        k = random.randint(0, len(clients) - 1)
        print("Saying hello to %s" % (clients[k]))
        #clients[k].emit('message', "Hello at %s" % (datetime.now()))
        io.emit('message', "Hello at %s" % (datetime.now()), room=clients[k])


def start(name):
    io.run(app)


if __name__ == '__main__':
    import threading
    import time
    #thread.start_new_thread(lambda: io.run(app), ())
    x = threading.Thread(target=start, args=(1,))
    x.start()

    while True:
        time.sleep(1)
        hello_to_random_client()
