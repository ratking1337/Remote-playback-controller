#!/usr/bin/python

import time
import os
import sys
import socket
import json

from playsound import playsound
dir = './'

def get_arg(arg, status, arr):
    if arg in arr:
        return arr[arr.index(arg) + 1]
    else:
        sys.exit(status)

def interpret_args():
    args = {}
    args['port'] = get_arg('-p', 'ERR: No port specified', sys.argv)
    return args

s = None

def connection():
    global s

    args = interpret_args()
    port = int(args['port'])

    s = socket.socket(socket.AF_INET)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("", port))
    s.listen(1)
    (conn, address) = s.accept()
    print(conn, '\n', address)
    return conn

def exec_command(cmmd):
    if cmmd[:10] == 'play song ':
        play_sound(find_songs(search_dir(None), [cmmd[10:]]))
    elif cmmd[:9] == 'play all':
        play_sound(find_songs(search_dir(None), None))
    elif cmmd[:11] == 'list songs ':
        pass

def find_songs(json_string, number):
    dict = None
    if json_string:
        dict = json.loads(json_string)
    if number and dict:
        for key in dict:
            if key == number[0]:
                return [dict[key]]
    else:
        temp_arr = []
        for key in dict:
            temp_arr.append(dict[key])
        return temp_arr

def search_dir(none):
    contents = os.listdir(dir)
    indexed_names = {}

    i = 0
    for word in contents:
        indexed_names[i] = word
        i += 1
    return json.dumps(indexed_names)

def play_sound(names):
        for name in names:
            print(name)
            #playsound(name)

def main():
    conn = connection()

    while True:
        conn.send(search_dir(None))
        rcvdData = conn.recv(1024).decode()
        exec_command(rcvdData)
        time.sleep(0.1)
        pass


if __name__ == '__main__':
    main()
