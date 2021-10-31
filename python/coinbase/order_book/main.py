from multiprocessing import Process, Manager
from datetime import datetime
from time import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import websocket
import argparse
import json

ZERO_STR = '0.00000000'


def main(args):

    def on_open(ws):
        print('Socket has been opened')
        subscribe_message = {
                'type': 'subscribe',
                'channels': [
                    {'name':'level2', 'product_ids':[f'{args.coin}-USD']}
                    ]
                }
        ws.send(json.dumps(subscribe_message))

    def on_message(ws, message):
        d = json.loads(message)
        print(d)

    def on_error(ws,error):
        print(error)

    socket = 'wss://ws-feed.pro.coinbase.com'
    ws = websocket.WebSocketApp(socket, 
            on_open = on_open,
            on_message = on_message,
            on_error = on_error
            )
    ws.run_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--coin', default = 'BTC', type=str)
    parser.add_argument('--delta', default = -250, type=int)

    args = parser.parse_args()
    main(args)
