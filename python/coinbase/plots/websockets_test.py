from multiprocessing import Process, Manager
from datetime import datetime
from time import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import websocket
import argparse
import json

def main(args):
    fig = plt.figure()
    ax = fig.subplots(2)

    man = Manager()
    close = man.list()
    highs = man.list()
    lows = man.list()
    sizes = man.list()

    DELTA = args.delta

    def plot(x):
        ax[0].clear()
        ax[0].plot(close[DELTA:])
        ax[0].plot(highs[DELTA:], color= 'red')
        ax[0].plot(lows[DELTA:], color='green')
        ax[1].bar(list(range(len(sizes[DELTA:]))), height=sizes[DELTA:], color='black')

    def on_open(ws):
        print('Socket has been opened')
        subscribe_message = {
                'type': 'subscribe',
                'channels': [
                    {'name':'ticker', 'product_ids':[f'{args.coin}-USD']}
                    ]
                }
        ws.send(json.dumps(subscribe_message))

    def on_message(ws, message):
        d = json.loads(message)
        print(d)
        if d['type'] == 'ticker':
            close.append(float(d['price']))
            highs.append(float(d['best_ask']))
            lows.append(float(d['best_bid']))
            sizes.append(float(d['last_size']))

    def on_error(ws,error):
        print(error)

    socket = 'wss://ws-feed.pro.coinbase.com'
    ani = animation.FuncAnimation(fig, plot, interval = 1)
    ws = websocket.WebSocketApp(socket, 
            on_open = on_open,
            on_message = on_message,
            on_error = on_error
            )

    jobs = [
            Process(target= ws.run_forever),
            #Process(target=plt.show),
            ]

    for j in jobs:
        j.start()
    for j in jobs:
        j.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--coin', default = 'BTC', type=str)
    parser.add_argument('--delta', default = -250, type=int)

    args = parser.parse_args()
    main(args)
