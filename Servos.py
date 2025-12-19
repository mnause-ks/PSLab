"""
Instrument wrapper for PSLab python API
"""

from time import sleep

from enum import Enum

from OpenTap import Display
from OpenTap import Unit
from opentap import *

from .ConnectionHandler import ConnectionHandler

SquareWavePin = Enum('SquareWavePin', ['SQ1', 'SQ2', 'SQ3', 'SQ4'])

@attribute(Display("Servo", "Servo Instrument", "PSLab"))
class Servos(Instrument):
    min_angle_pulse = property(float, 500)\
        .add_attribute(Unit("ms"))\
        .add_attribute(Display("Min. Angle Pulse", "Pulse length corresponding to the minimum (usually 0 degree) angle of the servo.", "", -50))

    max_angle_pulse = property(float, 2500)\
        .add_attribute(Unit("ms"))\
        .add_attribute(Display("Max. Angle Pulse", "Pulse length corresponding to the maximum (usually 180 degree) angle of the servo.", "", -40))

    angle_range = property(float, 180)\
        .add_attribute(Unit("°"))\
        .add_attribute(Display("Angle Range", "Range of the servo.", "", -30))

    frequency = property(float, 50)\
        .add_attribute(Unit("Hz"))\
        .add_attribute(Display("Frequency", "Frequency of the control signal.", "", -20))

    def __init__(self):
        """Set up the properties, methods and default values of the instrument."""
        super(Servos, self).__init__()  # The base class initializer must be invoked.
        self.instrument = None
        self.Name = "Servo"
        self.Rules.Add(Rule("min_angle_pulse", lambda: self.min_angle_pulse > 0, lambda: 'Angle pulse must be positive.'))
        self.Rules.Add(Rule("max_angle_pulse", lambda: self.max_angle_pulse > 0, lambda: 'Angle pulse must be positive.'))
        self.Rules.Add(Rule("angle_range", lambda: self.angle_range > 0, lambda: 'Angle range must be positive.'))
        self.Rules.Add(Rule("angle_range", lambda: self.angle_range <= 360, lambda: 'Angle range must not exceed 360°.'))
        self.Rules.Add(Rule("frequency", lambda: self.frequency > 0, lambda: 'Frequency must be positive.'))

    def Open(self):
        super(Servos, self).Open()
        # Open COM connection to instrument using ConnectionHandler
        self.instrument = ConnectionHandler.instance().getServos(self.min_angle_pulse, self.max_angle_pulse, self.angle_range, self.frequency)
        """Called by TAP when the test plan starts"""

    def Close(self):
        """Called by TAP when the test plan ends."""
        super(Servos, self).Close()

    def get_min_angle(self):
            return 0

    def get_max_angle(self):
            return self.angle_range

    def _get_servo(self, pin: SquareWavePin):
        match pin:
            case SquareWavePin.SQ1:
                return self.instrument[0]
            case SquareWavePin.SQ2:
                return self.instrument[1]
            case SquareWavePin.SQ3:
                return self.instrument[2]
            case SquareWavePin.SQ4:
                return self.instrument[3]
            case _:
                raise Exception("Unsupported pin " + pin)

    def set_angle(self, pin: SquareWavePin, angle: int):
        """ Wait a few milliseconds to allow the command to be processed between steps.
        Otherwise, movements could be omitted if the commands are sent too quickly one after the other. """
        sleep(20/1000)
        self._get_servo(pin).angle = angle
