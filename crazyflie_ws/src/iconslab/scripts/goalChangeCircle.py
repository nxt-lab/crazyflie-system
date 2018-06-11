#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Time

def circleGoal():
    rospy.init_node('circleGoal', anonymous=True)

    pubname = rospy.Publisher('goal', PoseStamped, queue_size=10) 
    pubtime = rospy.Publisher('time', Time, queue_size=10)

    loop_rate = 30
    rate = rospy.Rate(loop_rate)
    radians = 0
    pos = PoseStamped()
    radius = 0.5
    while not rospy.is_shutdown():
        pos.pose.position.x = math.cos(radians) * radius
        pos.pose.position.y = math.sin(radians) * radius
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
