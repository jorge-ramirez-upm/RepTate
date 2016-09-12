import enum
from CmdBase import *
from DataTable import *

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


class Theory(CmdBase):
    """Abstract class to describe a theory
            thname            (str): Theory name
            description     (str): Description of theory
    """
    thname=""
    description=""

    def __init__(self, name="Theory", parent_dataset=None, ax=None):
        """Constructor:
        Args:
            name            (str): Name used internally by the dataset
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
        super(Theory, self).__init__() 
        self.name=name
        self.parent_dataset = parent_dataset
        self.ax = ax
        self.thtype=TheoryType.point
        self.parameters={}
        self.tables={}
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

        # Pre-create as many tables as files in the dataset
        for f in parent_dataset.files:
            self.tables[f.file_name_short]=DataTable(ax)

    def precmd(self, line):
        """ This method is called after the line has been input but before
            it has been interpreted. If you want to modifdy the input line
            before execution (for example, variable substitution) do it here.
            TODO: Substitute parameter values if symbol {param} is used
        """
        super(Theory,self).precmd(line)
        return line
        
    def do_calculate(self, line):
        """Calculate the theory"""
        for f in self.parent_dataset.files:
            if self.thtype==TheoryType.point:
                self.point_function(f)
            elif self.thtype==TheoryType.line:
                self.line_function(f)
            elif self.thtype==TheoryType.user:
                self.user_function(f)
            else:
                print("Theory type must be set!")
    
    def do_error(self, line):
        """Report the error of the current theory on the given filename
           The error is calculated with least-squares
        """
        f = self.parent_dataset.current_file
        if self.thtype == TheoryType.point:
            view = self.parent_dataset.parent_application.current_view
            xexp, yexp, success = view.view_proc(f.data_table, f.file_parameters)
            xth, yth, success = view.view_proc(self.tables[f.file_name_short], f.file_parameters)
            print(yexp)
            print(yth)
            print(np.mean((yth-yexp)**2))
        else:
            print("Not implemented yet")

    def do_print(self, line):
        """Print the theory table associated with the given file name"""
        if line in self.tables:
            print(self.tables[line].data)
        else:
            print("Theory table for \"%s\" not found"%line)

    def complete_print(self, text, line, begidx, endidx):
        file_names=list(self.tables.keys())
        if not text:
            completions = file_names[:]
        else:
            completions = [ f
                            for f in file_names
                            if f.startswith(text)
                            ]
        return completions
        
    def do_parameters(self, line):
        """View and/or change the values of the theory parameters
           parameters A=0.4 B=0.3
           With no arguments, show the current values
        """
        if (line==""):
            print(self.parameters)
        else:
            args={}
            for s in line.split():
                par=s.split("=")
                args[par[0]]=float(par[1])
            self.parameters.update(args)

    def complete_parameters(self, text, line, begidx, endidx):
        parameter_names=list(self.parameters.keys())
        if not text:
            completions = parameter_names[:]
        else:
            completions = [ f
                            for f in parameter_names
                            if f.startswith(text)
                            ]
        return completions