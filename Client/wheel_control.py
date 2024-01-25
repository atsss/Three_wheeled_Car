from TCPClient import TCPClient
from Command import COMMAND as cmd
import time

MOVE_FOWARD = 'foward'
STOP = 'stop'
COMMAND_MAP = { 'Closed_Fist': MOVE_FOWARD, 'Open_Palm': STOP }

class WheelControl:
    SERVO_MIN_ANGLE = 0
    SERVO_MAX_ANGLE = 180
    SPEED_UNIT = 35
    TURN_ANGLE_UNIT = 35

    def __init__(self, tcp: TCPClient):
        self._prev_command = None
        self.tcp = tcp

    @property
    def prev_command(self):
        return self._prev_command

    @prev_command.setter
    def prev_command(self, command: str | None):
        self._prev_command = command

    def get_command(self, gesture_name: str) -> str | None:
        if gesture_name not in COMMAND_MAP:
            return

        return COMMAND_MAP[gesture_name]

    def drive(self, current_command: str | None) -> None:
        if not current_command:
            return
        if self.prev_command == current_command:
            return

        print(f'Command: {current_command}')
        if current_command == MOVE_FOWARD:
          self.move_forward()
        elif current_command == STOP:
          self.stop_moving()

    def move_forward(self):
        self.setMoveSpeed(cmd.CMD_FORWARD, self.SPEED_UNIT)

    def stop_moving(self):
        self.tcp.sendData(cmd.CMD_STOP)

    def setMoveSpeed(self, CMD, spd):
        self.tcp.sendData(CMD + str(int(spd//3)))
        self.tcp.sendData(CMD )
        time.sleep(0.07)
        self.tcp.sendData(CMD + str(int(spd//3*2)))
        time.sleep(0.07)
        self.tcp.sendData(CMD + str(int(spd)))
