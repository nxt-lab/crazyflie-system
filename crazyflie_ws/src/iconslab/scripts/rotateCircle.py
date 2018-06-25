#!/usr/bin/env python

import rospy
import numpy
import math
from geometry_msgs.msg import PoseStamped
from pyquaternion import Quaternion


def rotCircleGoal():
    rospy.init_node('rotCircleGoal', anonymous=True)
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
        my_quaternion = Quaternion(axis=[1, 0, 0], angle=0.75839816339)
        position_vec = numpy.array(
            [math.cos(radians) * radius,
             math.sin(radians) * radius, 0])
        rotp_vec = my_quaternion.rotate(position_vec)
        pos.pose.position.x = rotp_vec[0]
        pos.pose.position.y = rotp_vec[1]
        pos.pose.position.z = rotp_vec[2] + 1
        radians += 0.020
        pubname.publish(pos)
        rate.sleep()


if __name__ == "__main__":
    try:
        rotCircleGoal()
    except rospy.ROSInterruptException:
        pass
