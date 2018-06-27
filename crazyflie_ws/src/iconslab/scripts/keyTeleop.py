#!/usr/bin/env python
import io
import rospy
import curses

from sensor_msgs.msg import Joy


class KeyTeleop():
    def __init__(self, stdscr, publisher):
        self.screen = stdscr
        self.pub = publisher
        self._running = True
        self._joy = {"land": 0, "emergency": 1, "launch": 2}
        self._keys = {
            ord('q'): self.niceQuit,
            ord('l'): self.toggleFlight,
            ord(' '): self.emergency
        }
        self._flying = False

    def toggleFlight(self, msg):
        if self._flying:
            self.land(msg)
        else:
            self.launch(msg)

    def land(self, msg):
        msg[0] = 1
        self._flying = False

    def launch(self, msg):
        msg[2] = 1
        self._flying = True

    def quit(self, msg):
        self._running = False

    def emergency(self, msg):
        self.quit(msg)
        self._flying = False
        msg[1] = 1

    def niceQuit(self, msg):
        self.land(msg)
        self.quit(msg)

    def read_key(self, stdscr):
        keycode = stdscr.getch()
        return keycode if keycode != -1 else None

    def set_joy_msg(self, msg, key):
        buttons = [0] * 11
        axis = [0.0] * 8
        if key in self._keys.keys():
            self._keys[key](buttons)
            msg.buttons = buttons
            msg.axes = axis

    def run(self):
        # Clear screen
        self.screen.clear()
        self.screen.addstr(0, 0, "Iconslab control center.")
        self.screen.addstr(1, 0, "Use 'l' to launch/land.")
        self.screen.addstr(2, 0, "Use SPACE to trigger emergency")
        self.screen.addstr(2, 0, "Use 'q' to land and quit")
        rate = rospy.Rate(2)
        msg = Joy()

        while not rospy.is_shutdown() and self._running:
            keycode = self.read_key(self.screen)
            self.set_joy_msg(msg, keycode)

            self.pub.publish(msg)

            rate.sleep()

        rospy.signal_shutdown('Exit triggered.')


def main(stdscr):
    rospy.init_node('key_joy', anonymous=True)
    pub = rospy.Publisher("joy", Joy, queue_size=10)
    teleop = KeyTeleop(stdscr, pub)
    teleop.run()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except rospy.ROSInterruptException:
        pass
