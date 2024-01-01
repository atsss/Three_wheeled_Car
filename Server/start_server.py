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
        self.parseOpt()

    def parseOpt(self):
        try:
            self.opts,self.args = getopt.getopt(sys.argv[1:],"mnt")
        except getopt.GetoptError as err:
            print(str(err))
            return
        for o,a in self.opts:
            if o in ("-m"):
                self.cmr_Thread = Camera_Server()
                self.cmr_Thread.start()
            elif o in ("-t"):
                self.tcp = mTCPServer()
                self.tcp.setDaemon(True)
                self.tcp.start()
            elif o in ("-n"):
                self.user_ui = False

if __name__ == "__main__":
    dlg = Main()
    while True:
        time.sleep(1000)
