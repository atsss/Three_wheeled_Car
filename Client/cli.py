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

class CommandLineInterface():
    tcp = TCPClient()
    Camera_H_Pos = 90
    Camera_V_Pos = 90
    SERVO_MIN_ANGLE = 0
    SERVO_MAX_ANGLE = 180
    ANGLE_UNIT = 10
    SPEED_UNIT = 50

    def __init__(self, parent=None):
        try:
            self.opts,self.args = getopt.getopt(sys.argv[1:],"a:fbud")
        except getopt.GetoptError as err:
            print(str(err))
            return
        for o,a in self.opts:
            if o in ("-a"):
                self.connect_tcp(a)
            elif o in ("-f"):
                self.move_forward()
            elif o in ("-b"):
                self.move_backword()
            elif o in ("-u"):
                self.tilt_camera_up()
            elif o in ("-d"):
                self.tilt_camera_down()


    def connect_tcp(self, server_ip):
        print(("Connecting......", server_ip))
        try:
            self.tcp.connectToServer(address = (server_ip, 12345))
        except Exception as e:
            print(("Connect to server Faild!: Server IP is right? Server is opend?", e))
            self.msgDlg.showMessage("Connect to server Faild! \n\t1. Server IP is right? \n\t2. Server is opend?")
            return
        print("Connecttion Successful !")

    def tilt_camera_up(self):
        self.Camera_V_Pos = self.Camera_V_Pos + self.ANGLE_UNIT
        self.Camera_V_Pos = constrain(self.Camera_V_Pos, self.SERVO_MIN_ANGLE, self.SERVO_MAX_ANGLE)
        self.tcp.sendData(cmd.CMD_CAMERA_UP + str(self.Camera_V_Pos))

    def tilt_camera_down(self):
        self.Camera_V_Pos = self.Camera_V_Pos - self.ANGLE_UNIT
        self.Camera_V_Pos = constrain(self.Camera_V_Pos, self.SERVO_MIN_ANGLE, self.SERVO_MAX_ANGLE)
        self.tcp.sendData(cmd.CMD_CAMERA_DOWN + str(self.Camera_V_Pos))

    def move_forward(self):
        self.setMoveSpeed(cmd.CMD_FORWARD, self.SPEED_UNIT)

    def move_backword(self):
        self.setMoveSpeed(cmd.CMD_BACKWARD, self.SPEED_UNIT)


if __name__ == "__main__":
    CommandLineInterface()
