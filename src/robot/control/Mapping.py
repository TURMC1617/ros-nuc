#!/usr/bin/env python

import rospy as rp
from turmc.tools.textutils import unpackDict

def callback(data):
    commands = unpackDict(data.data)

    for command in commands:
        if command == 'pathfind':
            pathfind(commands[command])
        elif command == 'updatePosition':
            robotpos = commands[command]
        elif command == 'addObstacle':
            addObstacle(commands[command])
    return

def init():
    global robotpos
    return

def shutdown():
    return

def main():
    return:

if __name__ == '__main__':
    try:
        main()
    except rp.ROSInterruptException:
        rp.loginfo('Mapping node interrupted; shutting down')
        shutdown()
        pass
