#!/usr/bin/env python

import rospy
import numpy
import math
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Time

def figure8Goal():
    rospy.init_node('figure8Goal', anonymous=True)

    pubname = rospy.Publisher('goal', PoseStamped, queue_size=10) 
    pubtime = rospy.Publisher('time', Time, queue_size=10)

    loop_rate = 30
    rate = rospy.Rate(loop_rate)
    radians = 0
    pos = PoseStamped()
    radius = 0.5
    i = 0
    while not rospy.is_shutdown() and i != 500:
	pos.pose.position.x = 0
        pos.pose.position.y = 0
        pos.pose.position.z = 1
        i+=1
        pubtime.publish(pos.header.stamp)
        pubname.publish(pos)
        rate.sleep()
    while not rospy.is_shutdown():
        pos.pose.position.x = math.cos(radians) * radius
        pos.pose.position.y = math.sin(2*radians) * radius
        pos.pose.position.z = 1
	pubtime.publish(pos.header.stamp)
        radians += 0.020
        pubname.publish(pos)
        rate.sleep()
        
        

if __name__=="__main__":
    try:
        figure8Goal()
    except rospy.ROSInterruptException:
        pass
