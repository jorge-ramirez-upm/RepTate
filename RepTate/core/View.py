class View(object):
    """Abstract class to describe a view"""
    def __init__(self, name="", description="", x_label="", y_label="", log_x=False, log_y=False, view_proc=None, n=1, snames=[]):
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
        


