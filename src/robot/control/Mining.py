#!/usr/bin/env python

import rospy as rp
from std_msgs.msg import String
from turmc.tools.textutils import unpackDict
from turmc.global_constants import *

def miningSequence(data):
    #The mining sequence

def stopMiningSequence(data):
     stopDrill = String(data = hardwareCommands['drillStop'])
     retractDrill = String(data = hardwareCommands['drillRetract'])
     lowerDrill = String(data = hardwareCommands['drillLower'])
     allStop = String(data = hardwareCommands['drillFreeze'])

     motorPub.publish(stopDrill)
     motorPub.publish(retractDrill)

     rp.sleep(10)

     motorPub.publish(lowerDrill)

     rp.sleep(10)

     motorPub.publish(allStop)
     motorPub.publish(lowerDrill)

     rp.sleep(15)

     motorPub.publish(allStop)

def callback(data):
    commands = unpackDict(data.data)

    for command in commands:
        if command == 'begin':
            miningSequence(commands[command])
        elif command == 'stop':
            stopMiningSequence(commands[command])

def init():
    global responsePub, motorPub, miningSub, hardwareCommands

    hardwareCommands = unpackDict('MotorControlCommands.json')

    motorPub = rp.Publisher(TOPIC_MINING_REDIRECT, String, queue_size = 3)
    responsePub = rp.Publisher(TOPIC_MINING_STATE, String, queue_size = 3)

    rp.init_node('Mining', anonymous = True)

    rp.on_shutdown(shutdown)

    miningSub = rp.Subscriber(TOPIC_MINING_CONTROL, String, callback)

def shutdown():
    #Send stop commands

def main():

    init()

    rp.spin()

    shutdown()

if __name__ == '__main__':
    try:
        main()
    except rp.ROSInterruptException:
        rp.loginfo('Ming node interrupted; shutting down')
        shutdown()
        pass
