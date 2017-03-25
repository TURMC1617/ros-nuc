#!/usr/bin/env python
#import roslib; roslib.load_manifest('Phoebe')
import rospy

from nav_msgs.msg import Odometry
from geometry_msgs.msg import *
from tf.msg import *



counter = 0

def Position(odom_data):

    global counter
    rospy.sleep(1)
    curr_time = odom_data.header.stamp
    pose = odom_data.pose.pose #  the x,y,z pose and quaternion orientation
    counter= counter+1
    print counter, curr_time
    print pose




if __name__ == "__main__":
    rospy.init_node('odometry',anonymous=True)
    rospy.Subscriber('odom',Odometry,odometryCb)
    rospy.spin() # not really necessary because we have while not rospy.is_shutdown()