import socket
import threading
import os
import pickle


class Threaded_server(threading.Thread):
    def __init__(self, conn, addr, k):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.k = k
        self.connection_info()
        self.client_handling()

    def connection_info(self):
        print(f'Connected: {self.addr}')

    def client_handling(self):
        page = open(f'{1 if self.k%2 == 1 else 2}.html', mode='r', encoding='utf-8').read()
        page = page[:page.index('</H1>')-1] + f'. Номер клиента: {self.k}' + page[page.index('</H1>')-1:]
        resp = f'''HTTP/1.1 200 OK

        {page}'''
        self.conn.send(resp.encode(encoding='utf-8'))


settings = open('settings.txt', mode='r').readlines()
port, directory, max_bytes = list(map(lambda x: x.split(': ')[1][:-1], settings))

sock = socket.socket()
sock.bind((directory, int(port)))
sock.listen(10)

k = 0
while True:
    k += 1
    conn, addr = sock.accept()
    thread = Threaded_server(conn, addr, k)
    thread.start()

