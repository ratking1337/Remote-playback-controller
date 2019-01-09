#!/usr/bin/python  

import os
import sys
import socket

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

def connection():
    args = interpret_args()
    print(args)

    s = socket.socket()         
    host = args['host'] 
    port = int(args['port'])

    s.connect((host, port))
    print(s.recv(1024))
    s.close()

def main():      
    connection()

if __name__ == '__main__':
    main()