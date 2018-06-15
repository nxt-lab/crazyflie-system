#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Time
from std_msgs.msg import String

def circleGoal():
    rospy.init_node('circleGoal', anonymous=True)

    y_offset = int(rospy.get_param("~y", "0"))

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
	pos.pose.position.y = y_offset
	pos.pose.position.z = 1
	i+=1
	pubtime.publish(pos.header.stamp)
	pubname.publish(pos)
	rate.sleep()
    while not rospy.is_shutdown():
        pos.pose.position.x = math.cos(radians) * radius
        pos.pose.position.y = math.sin(radians) * radius + y_offset
        pos.pose.position.z = 1
	pubtime.publish(pos.header.stamp)
        radians += 0.020
        pubname.publish(pos)
        rate.sleep()
        
        

if __name__=="__main__":
    try:
        circleGoal()
    except rospy.ROSInterruptException:
        pass
