class View(object):
    """Abstract class to describe a view"""

    def __init__(self, name="", description="", x_label="", y_label="", log_x=False, log_y=False, view_proc=None, n=1, snames=[]):
        """Constructor:
            
        Args:
            name            (str): View name
            description     (str): Description of view
            x_label         (str): X Axis label
            y_label         (str): Y Axis label
            x_units         (???): To be defined
            y_units         (???): To be defined
            log_x          (bool): X axis logarithmic?
            log_y          (bool): Y axis logarithmic?
            view_proc      (func): Function that creates the X, Y1, Y2 values of the view
            n               (int): Number of series that the view represents
            snames         (list): Names of the series represented by the view
        """
        self.name=name
        self.description=description
        self.x_label=x_label
        self.y_label=y_label
        self.x_units=""
        self.y_units=""
        self.log_x=log_x
        self.log_y=log_y
        self.view_proc=view_proc
        self.n=n
        self.snames=snames
