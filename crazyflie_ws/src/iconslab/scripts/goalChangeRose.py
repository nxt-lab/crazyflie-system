#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Time

def roseGoal():
    rospy.init_node('roseGoal', anonymous=True)

    pubname = rospy.Publisher('goal', PoseStamped, queue_size=10) 
    pubtime = rospy.Publisher('time', Time, queue_size=10)

    loop_rate = 30
    rate = rospy.Rate(loop_rate)
    radians = 0
    pos = PoseStamped()
    radius = 0.35
    i = 0
    while not rospy.is_shutdown() and i != 1000:
	pos.pose.position.x = 0
	pos.pose.position.y = 0	
	pos.pose.position.z = 1
	i+=1	
	pubtime.publish(pos.header.stamp)
        pubname.publish(pos)
        rate.sleep()
    while not rospy.is_shutdown():
	pos.pose.position.x = (2 + math.cos(4*radians)) * math.cos(radians) * radius
        pos.pose.position.y = (2 + math.cos(4*radians)) * math.sin(radians) * radius
        pos.pose.position.z = 1
	pubtime.publish(pos.header.stamp)
        radians += 0.025
        pubname.publish(pos)
        rate.sleep()
        
        

if __name__=="__main__":
    try:
        roseGoal()
    except rospy.ROSInterruptException:
        pass
