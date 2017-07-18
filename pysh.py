#!/usr/bin/python3

from collections import ChainMap
from sys import stdin
from os import system, execvpe, environ as sysenv
import tty
import termios

localenv = {}
localenv.setdefault('PS1', 'pysh@{path}> ')

env = ChainMap(localenv, sysenv)


def ps1parse(ps1):
    path = sysenv['PWD']
    home = sysenv['HOME']
    if path.startswith(home):
        path = '~' + path[len(home):]
    return ps1.format(path=path)


def main():
    old_screen_settings = termios.tcgetattr(stdin.fileno())
    tty.setcbreak(stdin.fileno())
    while True:
        try:
            print(ps1parse(env['PS1']), end='', flush=True)
            line = ''
            while True:
                c = stdin.read(1)
                if c == '\n':
                    print()
                    break
                if c == '\t':
                    continue
                print(c, end='', flush=True)
                line += c
            if line in {'quit', 'exit', '\x04'}:
                break
            if line[0] == ':':
                system(line[1:])
                continue
            if line[-1] == ':':
                print
                exec()
        except KeyboardInterrupt:
            print('^C')
    print()
    termios.tcsetattr(stdin.fileno(), termios.TCSADRAIN, old_screen_settings)


if __name__ == '__main__':
    main()
