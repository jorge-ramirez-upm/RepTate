import enum

class TheoryType(enum.Enum):
    point = 0
    line = 1
    user = 2

class LineTheoryIntegrationMethod(enum.Enum):
    Euler = 0
    RungeKutta5 = 1
    AdaptiveDt = 2

class TheoryPointDistributionType(enum.Enum):
    all_points=0
    linear=1
    log = 2


class Theory(object):
    """Abstract class to describe a theory"""
    def __init__(self, name="", description="", type=TheoryType.point):
        self.name=name 
        self.description = description 
        self.type=type
        self.parameters=[]
        self.point_function=None
        self.line_function=None
        self.user_function=None
        self.citations=""

        # THEORY OPTIONS
        self.min=0          # min for integration/calculation
        self.max=0          # max
        self.npoints=100    # Number of points to calculate
        self.point_distribution = TheoryPointDistributionType.all_points
        self.dt=0.001       # default time step
        self.dtmin=1e-6     # minimum time step for adaptive algorithms
        self.eps=1e-4       # precision for adaptive algorithms
        self.integration_method=LineTheoryIntegrationMethod.AdaptiveDt 
        self.stop_steady=False # Stop calculation if steady state of component 0 is attained

        
                 
    

