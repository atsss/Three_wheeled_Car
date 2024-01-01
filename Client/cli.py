# -*- coding: utf-8 -*-
########################################################################
# Filename    : main.py
# Description : Module implementing MainWindow.
# auther      : www.freenove.com
# modification: 2020/03/26
########################################################################
from TCPClient import TCPClient
from Command import COMMAND as cmd
import os
import sys,getopt
from Freenove_Math import *
import time
import threading
import math
#import copy
from CloseThreading import *

class CommandLineInterface():
    tcp = TCPClient()
    Camera_H_Pos = 90
    Camera_V_Pos = 90
    SERVO_MIN_ANGLE = 0
    SERVO_MAX_ANGLE = 180
    Is_Paint_Thread_On = False
    global t_Paint_Thread
    sonic_Index = 0
    sonic_buff = [0]*20
    send_Counter = 0
    Is_tcp_Idle = True

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
                self.camera_up()
            elif o in ("-d"):
                self.camera_down()


    def connect_tcp(self, server_ip):
        print(("Connecting......", server_ip))
        try:
            self.tcp.connectToServer(address = (server_ip, 12345))
        except Exception as e:
            print(("Connect to server Faild!: Server IP is right? Server is opend?", e))
            self.msgDlg.showMessage("Connect to server Faild! \n\t1. Server IP is right? \n\t2. Server is opend?")
            return
        print("Connecttion Successful !")

    def camera_up(self):
        self.tcp.sendData(cmd.CMD_CAMERA_UP + str(self.Camera_V_Pos))

    def camera_down(self):
        self.tcp.sendData(cmd.CMD_CAMERA_DOWN + str(self.Camera_V_Pos))

    def move_forward(self):
        self.setMoveSpeed(cmd.CMD_FORWARD,self.slider_Speed.value())

    def move_backword(self):
        self.setMoveSpeed(cmd.CMD_BACKWARD,self.slider_Speed.value())


if __name__ == "__main__":
    CommandLineInterface()
