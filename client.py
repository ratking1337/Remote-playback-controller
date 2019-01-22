#!/usr/bin/python

import os
import sys
import time
import socket
import json

def get_arg(arg, status, arr):
    if arg in arr:
        return arr[arr.index(arg) + 1]
    else:
        sys.exit(status)

def interpret_args():
    args = {}
    args['host'] = get_arg('-h', 'ERR: No host to connect to', sys.argv)
    args['port'] = get_arg('-p', 'ERR: No port specified', sys.argv)
    return args

s = None

def connection():
    global s
    args = interpret_args()
    print(args)

    s = socket.socket()
    host = args['host']
    port = int(args['port'])
    s.connect((host, port))

def read_commands(s):
    cmmd = input('#-> ')
    s.send(cmmd.encode())

def to_list(json_string):
    dec_list = json.loads(json_string)
    for key in dec_list:
        print(key, '->', dec_list[key])

def main():
    connection()

    while True:
        r_data = s.recv(1024)
        to_list(r_data)
        read_commands(s)
        time.sleep(0.1)
        pass

if __name__ == '__main__':
    main()
