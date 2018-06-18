#!/usr/bin/env python

import rospy
import numpy
import math
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Time

def hover(x):
    return (0,0,1)

def circleShape(theta):
    return (math.cos(theta), math.sin(theta), 1)

def figure8(theta):
    return (math.cos(theta),  math.sin(2*theta), 1)

shapeFuncs = {"circle":circleShape, "hover":hover, "figure8":figure8}

def shapeGoal():
    rospy.init_node('shapeGoal', anonymous=True)

    loop_rate = int(rospy.get_param("loop_rate", "30"))
    x_offset = float(rospy.get_param("x", "0"))
    y_offset = float(rospy.get_param("y", "0"))
    z_offset = float(rospy.get_param("z", "0"))
    theta = float(rospy.get_param("theta", "0"))
    hold_center = bool(rospy.get_param("hold", "True"))
    radius = float(rospy.get_param("radius", "1"))
    delay = int(rospy.get_param("delay", "5000")) * loop_rate /1000
    shape = rospy.get_param("shape", "hover")

    shapeFunc = shapeFuncs[shape]

    pubname = rospy.Publisher('goal', PoseStamped, queue_size=10)
    pubtime = rospy.Publisher('time', Time, queue_size=10)

    rate = rospy.Rate(loop_rate)
    pos = PoseStamped()
    radius = 0.5
    i = 0
    while hold_center and not rospy.is_shutdown() and i != delay:
        pos.pose.position.x = x_offset
        pos.pose.position.y = y_offset
        pos.pose.position.z = 1
        i+=1
        pubtime.publish(pos.header.stamp)
        pubname.publish(pos)
        rate.sleep()
    while not rospy.is_shutdown():
        x,y,z = shapeFunc(theta)
        pos.pose.position.x = x * radius + x_offset
        pos.pose.position.y = y * radius + y_offset
        pos.pose.position.z = z + z_offset
	pubtime.publish(pos.header.stamp)
        theta += 0.020
        pubname.publish(pos)
        rate.sleep()

if __name__=="__main__":
    try:
        shapeGoal()
    except rospy.ROSInterruptException:
        pass
