#!/usr/bin/env python

import rospy
import numpy
import math
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Time

def point_gen():
	radius =  0.5
	inputpoints = numpy.linspace(0.0, 2*math.pi , num = 300, endpoint=True)
	for radians in inputpoints:
		x = math.cos(radians) * radius
		y = math.sin(2*radians) * radius
		z = 1
		yield x,y,z

def figure8Goal():
    rospy.init_node('figure8Goal', anonymous=True)

    pubname = rospy.Publisher('goal', PoseStamped, queue_size=10) 
    pubtime = rospy.Publisher('time', Time, queue_size=10)

    loop_rate = 30
    rate = rospy.Rate(loop_rate)
    pos = PoseStamped()
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
	for x,y,z in point_gen():
       		pos.pose.position.x = x
        	pos.pose.position.y = y
        	pos.pose.position.z = z
		pubtime.publish(pos.header.stamp)
        	pubname.publish(pos)
        	rate.sleep()
        
        

if __name__=="__main__":
    try:
        figure8Goal()
    except rospy.ROSInterruptException:
        pass
