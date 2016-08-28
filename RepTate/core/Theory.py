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
        """Constructor:
        Args:
            name            (str): Theory name
            description     (str): Description of theory
            type           (enum): Type of theory (point, line, user)
            parameters     (dict): Parameters of the theory
            point_function (func): Calculation for point theory
            line_function  (func): Calculation for line theory
            user_function  (func): Calculation for user theory
            citations       (str): Articles that should be cited
       Theory Options:
            min            (real): min for integration/calculation
            max            (real): max
            npoints         (int): Number of points to calculate
            point_distribution   : all_points, linear, log
            dt             (real): default time step
            dt_min         (real): minimum time step for adaptive algorithms
            eps            (real): precision for adaptive algorithms
            integration_method   : Euler, RungeKutta5, AdaptiveDt
            stop_steady    (bool): Stop calculation if steady state of component 0 is attained
        """
        self.name=name 
        self.description = description 
        self.type=type
        self.parameters={}
        self.point_function=None
        self.line_function=None
        self.user_function=None
        self.citations=""

        # THEORY OPTIONS
        self.min=0
        self.max=0
        self.npoints=100
        self.point_distribution = TheoryPointDistributionType.all_points
        self.dt=0.001
        self.dt_min=1e-6 
        self.eps=1e-4
        self.integration_method=LineTheoryIntegrationMethod.AdaptiveDt
        self.stop_steady=False
