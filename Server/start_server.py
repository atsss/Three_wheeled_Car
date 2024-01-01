# -*- coding: utf-8 -*-
########################################################################
# Filename    : Main.py
# Description : This is the Freenove Three-wheeled Smart Car for Raspberry Pi the Server code.
#               Execute this file with Python3.
# auther      : www.freenove.com
# modification: 2020/03/26
########################################################################

from Camera_Server import *
from mTCPServer import mTCPServer

import sys,getopt
import time


class Main():
    tcp = mTCPServer()
    tcp.setDaemon(True)
    cmr_Thread = Camera_Server()
    #cmr_Thread.setDaemon(True)
    #cmr_Thread = Camera_Server()
    def __init__(self, parent=None):
        self.start_tcp()
        self.start_camera()

    def start_tcp(self):
        self.tcp = mTCPServer()
        self.tcp.setDaemon(True)
        self.tcp.start()

    def start_camera(self):
        self.cmr_Thread = Camera_Server()
        self.cmr_Thread.start()


if __name__ == "__main__":
    dlg = Main()
    while True:
        time.sleep(1000)
