#!/usr/bin/env python

import rospy as rp
from std_msgs.msg import String
from sensor_msgs.msg import Image
from turmc.motor_control.camera_stepper import CameraStepper
from turmc.tools.textutils import String2Dictionary as Str2Dict
from turmc.vision.cameras import Ted
from turmc.vision.utils import Mat2ImgMsg
from turmc.vision.advanced_utils import BeaconTracking2017 as BeaconTracking

#Publishes a single image from Ted
def publish():
    tedPub.publish(Mat2ImgMsg(ted.getImage()))

#Publishes the bearing of the camera stepper to the center of the specified color beacon
def locateBeacon(color):

    #This will handle the entire process of tracking moving the stepper, taking pictures, and processing the images
    stepperBearing = BeaconTracking(color, ted, stepper)

    #Creates the message object
    message = String(data = str(stepperBearing))

    #Publishes the stepper bearing to target on the data publishing topic
    dataPub.publish(message)

def callback(data):
    #Get a dictionary of commands from the string
    commands = Str2Dict(data.data)

    #A single message could carry up to one copy of each command
    for command in commands:
        if command == 'publish':
            publish()
        elif command == 'goto':
            stepper.goto(commands[command])
        elif command == 'beacon':
            locateBeacon(commands[command])

#Initializes objects used in this publisher
def init():
    #Reference the global namespace
    global ted, tedPub, tedSub, dataPub, stepper

    stepper = CameraStepper()

    #Initialize the camera
    ted = Ted()

    #Initialize the publishers
    tedPub = rp.Publisher('images/Ted', Image, queue_size = 5)
    dataPub = rp.Publisher('data/beacontracking', String, queue_size = 3)

    #Initialize the node
    rp.init_node('Ted', anonymous = True)

    #Configures shutdown hook
    rp.on_shutdown(shutdown)

    #Initialize the subscriber
    tedSub = rp.Subscriber('hardware/Ted', String, callback)

#Safely cleans up the camera object
def shutdown():
    ted.release()

#Continously publishes images
def main():
    #Setup
    init()

    #Holds the node alive
    rp.spin()

    #Cleanup
    shutdown()

#Boilerplate for running as a script
if __name__ == '__main__':
    try:
        main()
    except rp.ROSInterruptException:
        rp.loginfo('ImagePublisher interrupted; shutting down...')
        shutdown()
        pass
