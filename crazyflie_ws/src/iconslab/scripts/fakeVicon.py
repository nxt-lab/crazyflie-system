#!/usr/bin/env python

import numpy as np
import rospy
import itertools
import time

from vicon_bridge.msg import Marker, Markers


def data_key(string):
    return string.split(":")[1].strip()


def key_str(string):
    return data_key(string).replace('"', "")


def parse_markers(string):
    markers = []
    for marker_str in string.split(" - ")[1:]:
        marker = Marker()
        marker_str = marker_str.strip().split("\n")
        marker.marker_name = key_str(marker_str[0]).strip().replace("'", "")
        marker.subject_name = key_str(marker_str[1]).strip().replace("'", "")
        marker.segment_name = key_str(marker_str[2]).strip().replace("'", "")
        marker.translation.x = float(data_key(marker_str[4]))
        marker.translation.y = float(data_key(marker_str[5]))
        marker.translation.z = float(data_key(marker_str[6]))
        marker.occluded = bool(data_key(marker_str[7]))
        markers.append(marker)
    return markers


def parse_marker_msg(marker_str):
    marker = {}
    mk_str = marker_str.split("\n")
    marker["frame_id"] = data_key(mk_str[5]).strip().replace("'", "")
    marker["markers"] = parse_markers(marker_str)
    return marker


def parse_markers_msg(marker_strs):
    markers_list = []
    for marker_str in marker_strs:
        marker_str = marker_str.strip()
        if marker_str:
            markers = parse_marker_msg(marker_str)
            markers_list.append(markers)
    return markers_list


def parse_file(filename):
    with open(filename, 'r') as fh:
        content = fh.read()
    marker_strs = content.split("---")
    return parse_markers_msg(marker_strs)


def marker_gen(lst):
    markers = Markers()
    markers_dicts = itertools.cycle(lst)
    counter = itertools.count(0)
    for markers_dict in markers_dicts:
        markers.frame_number = counter.next()
        stime = time.time()
        markers.header.stamp.secs = stime // 1
        markers.header.stamp.nsecs = (stime - int(stime)) * 1000000000
        markers.header.frame_id = markers_dict["frame_id"]
        markers.markers = markers_dict["markers"]
        yield markers


def create_marker_gen(filename):
    lst = parse_file(filename)
    return marker_gen(lst)


def list_gen(list):
    return itertools.cycle(list)


def start_vicon():
    rospy.init_node('fake_vicon', anonymous=True)

    marker_filename = rospy.get_param("vicon_data")
    markers_gen = create_marker_gen(marker_filename)

    # loop_rate = int(rospy.get_param("loop_rate", "30"))
    loop_rate = 30
    rate = rospy.Rate(loop_rate)
    pub = rospy.Publisher('vicon/markers', Markers, queue_size=10)
    while not rospy.is_shutdown():
        markers = markers_gen.next()

        pub.publish(markers)
        rate.sleep()


if __name__ == "__main__":
    try:
        start_vicon()
    except rospy.ROSInterruptException:
        pass
