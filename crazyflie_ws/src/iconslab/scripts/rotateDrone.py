#!/usr/bin/env python

import rospy
import numpy
import math
from geometry_msgs.msg import PoseStamped
from pyquaternion import Quaternion


def rotateDrone():
    rospy.init_node('rotateDrone', anonymous=True)
    pubname = rospy.Publisher('goal', PoseStamped, queue_size=10)
    loop_rate = 30
    rate = rospy.Rate(loop_rate)
    radians = 0
    pos = PoseStamped()
    radius = 0.5
    i = 0
    while not rospy.is_shutdown() and i != 350:
        pos.pose.position.x = 0
        pos.pose.position.y = 0
        pos.pose.position.z = 1
        i += 1
        pubname.publish(pos)
        rate.sleep()
    while not rospy.is_shutdown():
        my_quaternion = Quaternion(axis=[0, 0, 1], angle=radians)
        pos.pose.position.x = 0
        pos.pose.position.y = 0
        pos.pose.position.z = 1
        pos.pose.orientation.w = my_quaternion[0]
        pos.pose.orientation.x = my_quaternion[1]
        pos.pose.orientation.y = my_quaternion[2]
        pos.pose.orientation.z = my_quaternion[3]
        radians += 0.020
        pubname.publish(pos)
        rate.sleep()


if __name__ == "__main__":
    try:
        rotateDrone()
    except rospy.ROSInterruptException:
        pass
