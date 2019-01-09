import os
import sys
import socket

def main():
    s = socket.socket(socket.AF_INET)
    print(socket.IPPROTO_IP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("", 9998))
    s.listen(1)
    (conn, address) = s.accept()
    print(conn, '\n', address)

if __name__ == '__main__':
    main()