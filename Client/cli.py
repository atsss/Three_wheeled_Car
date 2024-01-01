# -*- coding: utf-8 -*-
########################################################################
# Filename    : main.py
# Description : Module implementing MainWindow.
# auther      : www.freenove.com
# modification: 2020/03/26
########################################################################
from TCPClient import TCPClient
from Command import COMMAND as cmd
import sys,getopt
import time

class CommandLineInterface():
    tcp = TCPClient()
    SERVO_MIN_ANGLE = 0
    SERVO_MAX_ANGLE = 180
    SPEED_UNIT = 35
    TURN_ANGLE_UNIT = 35

    def __init__(self, parent=None):
        try:
            self.opts,self.args = getopt.getopt(sys.argv[1:],"a:t:fbslrc")
        except getopt.GetoptError as err:
            print(str(err))
            return

        for o,a in self.opts:
            if o in ("-a"):
                self.connect_tcp(a)
            elif o in ("-t"):
                self.tilt_camera(a)
            elif o in ("-f"):
                self.move_forward()
            elif o in ("-b"):
                self.move_backword()
            elif o in ("-s"):
                self.stop_moving()
            elif o in ("-l"):
                self.turn_left()
            elif o in ("-r"):
                self.turn_right()
            elif o in ("-c"):
                self.turn_center()

        time.sleep(0.1)
        self.disconnect_tcp()

    def connect_tcp(self, server_ip):
        print(("Connecting......", server_ip))
        try:
            self.tcp.connectToServer(address = (server_ip, 12345))
        except Exception as e:
            print(("Connect to server Faild!: Server IP is right? Server is opend?", e))
            self.msgDlg.showMessage("Connect to server Faild! \n\t1. Server IP is right? \n\t2. Server is opend?")
            return
        print("Connecttion Successful!")

    def disconnect_tcp(self):
        self.tcp.disConnect()

    def tilt_camera(self, angle):
        target_angle = min(max(int(angle), self.SERVO_MIN_ANGLE), self.SERVO_MAX_ANGLE)
        self.tcp.sendData(cmd.CMD_CAMERA_UP + str(target_angle))

    def move_forward(self):
        self.setMoveSpeed(cmd.CMD_FORWARD, self.SPEED_UNIT)

    def move_backword(self):
        self.setMoveSpeed(cmd.CMD_BACKWARD, self.SPEED_UNIT)

    def stop_moving(self):
        self.tcp.sendData(cmd.CMD_STOP)

    def setMoveSpeed(self, CMD, spd):
        self.tcp.sendData(CMD + str(int(spd//3)))
        self.tcp.sendData(CMD )
        time.sleep(0.07)
        self.tcp.sendData(CMD + str(int(spd//3*2)))
        time.sleep(0.07)
        self.tcp.sendData(CMD + str(int(spd)))

    def turn_left(self):
        self.tcp.sendData(cmd.CMD_TURN_LEFT + str(self.TURN_ANGLE_UNIT))

    def turn_right(self):
        self.tcp.sendData(cmd.CMD_TURN_RIGHT + str(self.TURN_ANGLE_UNIT))

    def turn_center(self):
        self.tcp.sendData(f"{cmd.CMD_TURN_CENTER}90")


if __name__ == "__main__":
    CommandLineInterface()
