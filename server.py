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
    args['port'] = get_arg('-p', 'ERR: No port specified', sys.argv)
    return args

def connection():
    args = interpret_args()
    port = args['port']

    s = socket.socket(socket.AF_INET)
    s.setsockopt(socket.IPPROTO_IP, socket.SO_REUSEADDR, 1)
    s.bind(("", port))
    s.listen(1)
    (conn, address) = s.accept()
    print(conn, '\n', address)

def main():
    connection()

if __name__ == '__main__':
    main()