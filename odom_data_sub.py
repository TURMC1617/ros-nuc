#!/usr/bin/env python
#Will eventually turn into the movement planning node
import rospy

from nav_msgs.msg import Odometry
from geometry_msgs.msg import *
from tf.msg import *

#Mapping Knowns

#Input  predefined mining coords based off of robot initial position,
# and it's relationship to the beacon
def targetcoords(coords):
    #yes






#filtered odom data from localization node
def Position(odom_data):
    rospy.sleep(1)
    curr_time = odom_data.header.stamp
    pose = odom_data.pose.pose #  the x,y,z pose and quaternion orientation
    print curr_time
    print pose



def sendVelocity():
    #send velocities into the pi based off of current pose and its distance away from goal



if __name__ == "__main__":
    rospy.init_node('motion_planner',anonymous=True)
    rospy.Subscriber('odom',Odometry,odometryCb)
    rospy.spin() # not really necessary because we have while not rospy.is_shutdown()