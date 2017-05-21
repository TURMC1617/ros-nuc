#!/usr/bin/env python

import rospy as rp
from turmc.tools.textutils import unpackDict
from turmc.tools.mapping import CoordinateMap
from nav_msgs.msg import Odometry
from geometry_msgs.msg import *
from tf.transformations import euler_from_quaternion

#Defines how to convert the odom data into map/navigation data
xEquivalent = 'x'
yEquivalent = 'y'
yawEquivalent = 'yaw'

def pathfind(positions):
    points = arenaMap.pathfind(positions[0], positions[1])

def addObstacle(coordinate):
    try:
        arenaMap.addCircleObstacle(coordinate, radius = 15)
    except ValueError:
        rp.loginfo('Failed to add an obstacle at {}; outside of map'.format(coordinate))
    except:
        rp.loginfo('Failed to add obstacle')
    rp.loginfo('Added obstacle at {}'.format(coordinate))

def updatePosition(odomData):
    global robotpos

    position = odomData.pose.pose.position

    if xEquivalent == 'x':
        robotpos.x = int(position.x * 100)
    elif xEquivalent == 'y':
        robotpos.x = int(position.y * 100)
    elif xEquivalent == 'z':
        robotpos.x = int(position.z * 100)

    if yEquivalent == 'x':
        robotpos.y = int(position.x * 100)
    elif yEquivalent == 'y':
        robotpos.y = int(position.y * 100)
    elif yEquivalent == 'z':
        robotpos.y = int(position.z * 100)

    quaternion = (
        odomData.pose.pose.orientation.x,
        odomData.pose.pose.orientation.y,
        odomData.pose.pose.orientation.z,
        odomData.pose.pose.orientation.w
        )

    roll, pitch, yaw = euler_from_quaternion(quaternion)

    if yawEquivalent == 'roll':
        robotpos.bearing = roll
    elif yawEquivalent == 'pitch':
        robotpos.bearing = pitch
    elif yawEquivalent == 'yaw':
        robotpos.bearing = yaw

def callback(data):
    commands = unpackDict(data.data)

    for command in commands:
        if command == 'pathfind':
            pathfind(commands[command])
        elif command == 'addObstacle':
            addObstacle(commands[command])

def init():
    global arenaMap, commandSub, localizationSub, pathPub

    arenaMap = CoordinateMap(xmax = 738, ymax = 189, xmin = 0, ymin = -189)

    pathPub = rp.Publisher(TOPIC_PATHFINDING, String, queue_size = 5)

    rp.init_node('Mapping', anonymous = True)

    rp.on_shutdown(shutdown)

    commandSub = rp.Subscriber(TOPIC_MAPPING, String, callback)
    localizationSub = rp.Subscriber(TOPIC_ODOM_FILTERED, Odometry, updatePosition)

def shutdown():

    rp.loginfo('Mapping node shutting down')

def main():

    init()

    rp.spin()

    shutdown()

if __name__ == '__main__':
    try:
        main()
    except rp.ROSInterruptException:
        rp.loginfo('Mapping node interrupted; shutting down')
        shutdown()
        pass
