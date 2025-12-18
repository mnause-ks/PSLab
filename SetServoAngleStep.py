"""
Test step to set the angle of a connected servo on a SQ1-4 pin
"""

from OpenTap import Display, Unit, Verdict
from System import Double
from opentap import *

from .Servos import *


@attribute(Display("Set Servo Angle", "Sets angle of a connected servo", Groups=["PSLab", "Servo"]))
class SetServoAngleStep(TestStep):
    # Properties
    pin = property(SquareWavePin, SquareWavePin.SQ1) \
        .add_attribute(Display("Pin", "Pin on which the square wave is generated", "", -50))

    angle = property(float, 0) \
        .add_attribute(Display("Angle", "The angle to be set on a chosen SQ pin", "", -40)) \
        .add_attribute(Unit("°"))

    Servos = property(Servos, None) \
        .add_attribute(Display("Servo", "", "Resources", 0))

    def __init__(self):
        super(SetServoAngleStep, self).__init__()

        self.Rules.Add(
            Rule("angle", lambda: self.angle >= self.Servos.get_min_angle(),
                 lambda: f'Angle must be at least {self.Servos.get_min_angle()}°.'))
        self.Rules.Add(
            Rule("angle", lambda: self.angle <= self.Servos.get_max_angle(),
                 lambda: f'Angle must not exceed {self.Servos.get_max_angle()}°.'))

    def Run(self):
        self.Servos.set_angle(self.pin, self.angle)
        self.UpgradeVerdict(Verdict.Pass)
