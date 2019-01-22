#!/usr/bin/python

import time
import os
import sys
import socket
import json
import psutil
from multiprocessing import Process, Queue

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

def kill_player_process(name):
    for p in psutil.process_iter():
        if name in p.name() or name in ' '.join(p.cmdline()):
            p.terminate()
            p.wait()

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
    p = None

    if cmmd[:10] == 'play song ': 
        p = Process(target = play_sound, args = 
            (find_songs(search_dir(None), [cmmd[10:]])))

    elif cmmd[:9] == 'play all':
        p = Process(target = play_sound, args = 
            (find_songs(search_dir(None), None)))
    elif cmmd[:4] == 'stop':
        kill_player_process('mpg321')

    if p: 
        p.start()

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
        if type(names) is not list:
            names = [names] 

        for name in names:
            os.system('mpg321 ' + './' + name)

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
