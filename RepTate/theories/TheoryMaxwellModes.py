from Theory import *

class TheoryMaxwellModesTime(Theory):
    """Fit Maxwell modes to a time depenendent relaxation function"""
    thname="MaxwellModesTime"
    description="Fit Maxwell modes to time dependent function"

    def __init__(self, name="ThMaxwellTime"):
        super(TheoryMaxwellModesTime, self).__init__(name, TheoryType.point)


class TheoryMaxwellModesFrequency(Theory):
    """Fit Maxwell modes to a frequency dependent relaxation function"""
    thname="MaxwellModesFrequency"
    description="Fit Maxwell modes to frequency dependent function"

    def __init__(self, name="ThMaxwellFrequency"):
        super(TheoryMaxwellModesFrequency, self).__init__(name, TheoryType.point)

