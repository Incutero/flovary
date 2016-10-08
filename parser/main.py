#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json
import time
#def ask_for_book():


def send_hello(team):
    hello = {}
    hello["type"] = "hello"
    hello["team"] = team
    return json.dumps(hello)

def send_add(order_id, symbol, direction, price, size):
    add = {}
    add["type"] = "add"
    add["order_id"] = order_id
    add["symbol"] = symbol
    add["dir"] = direction
    add["price"] = price
    add["size"] = size
    return json.dumps(add)

def send_convert(order_id, symbol, direction, size):
    convert = {}
    convert["type"] = "convert"
    convert["order_id"] = order_id
    convert["symbol"] = symbol
    convert["dir"] = direction
    convert["size"] = size
    return json.dumps(convert)

def send_cancel(order_id):
    cancel = {}
    cancel["type"] = "cancel"
    cancel["order_id"] = order_id
    return json.dumps(cancel)

def receive_reject(message):
    print(message)

def receive_open(message):
    print(message) 

def receive_trade(message):
    print(message)

def receive_ack(message):
    print(message)

def receive_error(message):
    print(message)

def receive_close(message):
    print(message)

def receive_fill(message):
    print(message)

def receive_out(message):
    print(message)

def receive_message(json_msg):
    message = json.loads(json_msg)
    if message["type"] == "hello":
        receive_hello(message)
    elif message["type"] == "open":
        receive_open(message)
    elif message["type"] == "close":
        receive_close(message)
    elif message["type"] == "error":
        receive_error(message)
    elif message["type"] == "book":
        receive_book(message)
    elif message["type"] == "trade":
        receive_trade(message)
    elif message["type"] == "ack":
        receive_ack(message)
    elif message["type"] == "reject":
        receive_reject(message)
    elif message["type"] == "fill":
        receive_fill(message)
    elif message["type"] == "out":
        receive_out(message)

def receive_book(message):
    global book
    global valbz_prices
    global vale_prices
    global valbz_avg
    global vale_avg
    global vale_sell
    buy = message["buy"]
    sell = message["sell"]
    if buy:
        buy_price = buy[0][0]
    if sell:
        sell_price = sell[0][0]
    fair_price = None
    if buy and sell:
    	fair_price = (buy_price + sell_price) / 2.0
    if message["symbol"] == "VALBZ":
        if fair_price is not None:
            valbz_prices.append(fair_price)
        if len(valbz_prices) > 50:
            valbz_prices = valbz_prices[1:]
        valbz_avg = int(sum(valbz_prices)) / len(valbz_prices)
    if message["symbol"] == "VALE":
        if fair_price is not None:
            vale_prices.append(fair_price)
        if len(vale_prices) > 50:
            vale_prices = vale_prices[1:]
#        vale_avg = int(sum(vale_prices)) / len(vale_prices)

    book[message["symbol"]] = fair_price
    

def connect(): 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#    s.connect(("test-exch-itsjustaname", 25000))
    s.connect(("production", 25000))
    return s.makefile('w+', 1)

def main():
    global book
    global valbz_prices
    global vale_prices
    global valbz_avg
    global vale_avg
    global vale_sell
    team_name = "ITSJUSTANAME"
    order_id = 2 
    buy_bond = [order_id, "BOND", "BUY", 999, 3]
    sell_bond = [order_id, "BOND", "SELL", 1001, 3]
#    convert_sell_vale = [order_id, "VALE", "SELL", 6]
    convert_buy_vale = [order_id, "VALE", "BUY", 6]
    cancel = 5
    exchange = connect()

    book = {}
    valbz_prices = []
    vale_prices = []
    vale_avg = 0
    valbz_avg = 0
    vale_sell = 0
    print(send_hello(team_name), file=exchange)
    hello_from_exchange = exchange.readline().strip()
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)
    while(1):
        time.sleep(0.05)    
        receive_message(exchange.readline().strip())
        if "BOND" in book:
            if book["BOND"] > 1000:
                print(send_add(*sell_bond), file=exchange)
                order_id += 1
            if book["BOND"] < 1000:
                print(send_add(*buy_bond), file=exchange)
                order_id += 1
        if "VALE" in book and "VALBZ" in book:
            buy_vale = [order_id, "VALE", "BUY", int(valbz_avg-2), 10]
            sell_vale = [order_id, "VALE", "SELL", int(valbz_avg+2), 10]
            if book["VALE"] > valbz_avg:
                print(send_add(*sell_vale), file=exchange)
            if book["VALE"] < valbz_avg:
                print(send_add(*buy_vale), file=exchange)
        if "XLF" in book and "BOND" in book and "GS" in book and "MS" in book and "WFC" in book:
            if book["XLF"] is None or book["BOND"] is None or book["GS"] is None or book["MS"] is None or book["WFC"] is None:
                continue
            xlf_actual_price = 10 * book["XLF"]
            xlf_components_price = 3 * book["BOND"] + 2 * book["GS"] + 3 * book["MS"] + 2 * book["WFC"]
            buy_xlf = [order_id, "XLF", "BUY", int(book["XLF"]) - 2, 30]
            sell_xlf = [order_id, "XLF", "SELL", int(book["XLF"]) + 2, 30]
            if xlf_actual_price > xlf_components_price:
                print(send_add(*sell_xlf), file=exchange)
            if xlf_actual_price < xlf_components_price:
                print(send_add(*buy_xlf), file=exchange)

        print('valbz avg', valbz_avg)
        print('vale avg', vale_avg)

	print(book)


if __name__ == "__main__":
    main()
