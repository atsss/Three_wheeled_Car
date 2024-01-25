from gpiozero import LED
red = LED(17)

TURN_ON = 'on'
TURN_OFF = 'off'
COMMAND_MAP = { 'Closed_Fist': TURN_OFF, 'Open_Palm': TURN_ON }

class LedControl:
    def __init__(self):
        self._prev_command = None

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

    def update_led(self, current_command: str | None) -> None:
        if not current_command:
            return
        if self.prev_command == current_command:
            return

        if current_command == TURN_ON:
          red.on()
        elif current_command == TURN_OFF:
          red.off()
