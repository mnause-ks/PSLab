﻿# Imported the plugin modules.
# These modules should be located relative to this __init__ file.
# The '.' syntax is important for supporting both Python 3 and 2.
# It denotes that the module is in the same folder.
import sys
# if sys.version_info[0] == 3:
    # Enums only works in python 3.x
    # from .EnumUsage import *
from .PowerSupply import *
from .SetCurrentStep import *
from .GetCurrentStep import *
from .SetVoltageStep import *
from .GetVoltageStep import *
from .Oscilloscope import *
from .CaptureVoltageStep import *
from .WaveformGenerator import *
from .GenerateWaveStep import *
from .MeasureRMSVoltage import *
from .GenerateSineWave import * 
from .LogicAnalyzer import *
from .MeasureFrequencyStep import * 
from .MeasureIntervalStep import * 
## Advanced Section ##
IncludeLockManager = False 
#IncludeLockManager = True # Uncomment this to include the lock manager example.
if IncludeLockManager:
    from .LockManager import *

#This only works on with Editor (Community or Enterprise):
IncludeMenuItem = False
#IncludeMenuItem = True # Uncomment this to include the menu item example.
if IncludeMenuItem:
    from .MenuItem import *