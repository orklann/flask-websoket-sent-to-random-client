# https://github.com/Pithikos/python-websocket-server

import logging
from websocket_server import WebsocketServer

connections = []
packages = []


def new_client(client, server):
    global connections
    #server.send_message_to_all("Hey all, a new client has joined us")
    connections.append(client)
    print("connections: ", len(connections))


def pack():
    pass


server = WebsocketServer(13254, host='127.0.0.1', loglevel=logging.INFO)
server.set_fn_new_client(new_client)
server.run_forever()
