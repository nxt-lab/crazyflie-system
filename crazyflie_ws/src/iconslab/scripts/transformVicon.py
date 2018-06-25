#!/usr/bin/env python

import numpy as np
import rospy

from vicon_bridge.msg import Markers
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import TransformStamped


def marker_to_vector(marker):
    array = np.array([marker.x, marker.y, marker.z])
    return array


def get_center(top, left, bottom):
    a = top - left
    b = bottom - left
    aMag = np.linalg.norm(a)
    projection = ((np.dot(a, b) / (aMag * aMag)) * a)
    pos = projection + left
    return pos


def get_rotation(center, front, top, left, bottom):
    return (0, 0, 0, 1)


def start_transformer():
    rospy.init_node('transformer', anonymous=True)

    pubtf = rospy.Publisher('tf', TFMessage, queue_size=10)

    msg = TFMessage()

    crazyflies = {}

    def transformer(data):
        for marker in data.markers:
            if marker.subject_name:
                if marker.subject_name not in crazyflies:
                    crazyflies[marker.subject_name] = {}
                crazyflie = crazyflies[marker.subject_name]
                crazyflie[marker.marker_name] = marker.translation
                crazyflie["frame_id"] = str(data.frame_number)

        transforms = []
        for crazyflie_name in crazyflies:
            crazyflie = crazyflies[crazyflie_name]
            trans = TransformStamped()
            # trans.child_frame_id = crazyflie["frame_id"]
            trans.child_frame_id = "1"
            trans.header.frame_id = crazyflie["frame_id"]

            top = marker_to_vector(crazyflie["top"])
            bottom = marker_to_vector(crazyflie["bot"])
            left = marker_to_vector(crazyflie["left"])
            front = marker_to_vector(crazyflie["front"])

            center = get_center(top, left, bottom)
            rotation = get_rotation(center, front, top, left, bottom)

            mTrans = trans.transform.translation
            mTrans.x, mTrans.y, mTrans.z = center
            mRot = trans.transform.rotation
            mRot.x, mRot.y, mRot.z, mRot.w = rotation
            transforms.append(trans)

        msg.transforms = transforms
        pubtf.publish(msg)

    submarkers = rospy.Subscriber('/vicon/markers', Markers, transformer)
    rospy.spin()


if __name__ == "__main__":
    start_transformer()
