#!/usr/bin/env python

import rospy
import numpy
import math
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Time

def figure8Goal():
	rospy.init_node('figure8Goal', anonymous=True)
	pubname = rospy.Publisher('goal', PoseStamped, queue_size = 10) 
	pubtime = rospy.Publisher('time', Time, queue_size = 10)
	radius = 0.5
	inputpoints = numpy.linspace(0.0, 2*math.pi, num = 600, endpoint=True)
	coords = []
	for radians in range(0,len(inputpoints)-1):
		x = math.cos(inputpoints[radians]) * radius
		y = math.sin(2*inputpoints[radians]) * radius
		z = 1
		coords.append((x,y,z))
	i = 0
	while(i<len(coords)-1):
		d = math.sqrt(((coords[i+1][0]-coords[i][0])**2)+((coords[i+1][1]-coords[i][1])**2))
		if (d <= 0.1):
			del coords[i]
			print(d)
			i+=1	
	loop_rate = 30
	rate = rospy.Rate(loop_rate)
	pos = PoseStamped()
	j = 0
	while not rospy.is_shutdown() and j != 500:
		pos.pose.position.x = 0
		pos.pose.position.y = 0
		pos.pose.position.z = 1
		j+=1
		pubtime.publish(pos.header.stamp)
		pubname.publish(pos)
		rate.sleep()
	while not rospy.is_shutdown():
		for i in range (0,len(coords)-1):		
			pos.pose.position.x = coords[i][0]
			pos.pose.position.y = coords[i][1]
			pos.pose.position.z = coords[i][2]
			pubtime.publish(pos.header.stamp)
			pubname.publish(pos)
			rate.sleep()
        
if __name__=="__main__":
	try:
		figure8Goal()
	except rospy.ROSInterruptException:
		pass
'''
import numpy
import math

radius = 0.5
inputpoints = numpy.linspace(0.0, 2*math.pi, num = 600, endpoint=True)
coords = []
for radians in range(0,len(inputpoints)-1):
	x = math.cos(inputpoints[radians]) * radius
	y = math.sin(2*inputpoints[radians]) * radius
	z = 1
	coords.append((x,y,z))
i = 0
while(i<len(coords)-1):
	d = math.sqrt(((coords[i+1][0]-coords[i][0])**2)+((coords[i+1][1]-coords[i][1])**2))
	if (d <= 0.1):
		del coords[i]
		print(d)
	i+=1
print("length: ")
print(len(coords))
for i in range (0, len(coords)-1):
	print(coords[i])
'''

