# draggable matplotlib artists with the animation blit techniques; see
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from enum import Enum

class DragType(Enum):
    vertical = 1
    horizontal = 2
    both = 3
    none = 4

class DraggableArtist(object):
    """Abstract class for motions of a matplotlib artist"""
    lock = None
    def __init__(self, artist, mode=DragType.none, function=None):
        """Constructor. artist=rectangle,line,patch,series to move. mode:vertical,horizontal,all,none. function: function that should interpret the final coordinates of the artist moved"""
        self.artist = artist
        self.press = None
        self.background = None
        self.mode=mode
        self.function=function
        self.data = None
        self.connect()
        
    def connect(self):
        self.cidpress = self.artist.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.artist.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.artist.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.artist.axes: return
        if DraggableArtist.lock is not None: return
        contains, attrd = self.artist.contains(event)
        if not contains: return
        self.press = event.xdata, event.ydata
        self.get_data()
        DraggableArtist.lock = self
        canvas = self.artist.figure.canvas
        axes = self.artist.axes
        self.artist.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.artist.axes.bbox)
        axes.draw_artist(self.artist)
        canvas.blit(axes.bbox)

    def on_motion(self, event):
        if DraggableArtist.lock is not self:
            return
        if event.inaxes != self.artist.axes: return
        xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        if (self.mode==DragType.none):   
            self.modify_artist(0, 0)
        elif (self.mode==DragType.horizontal):
            self.modify_artist(dx, 0)
        elif (self.mode==DragType.vertical):
            self.modify_artist(0, dy)
        elif (self.mode==DragType.both):
            self.modify_artist(dx, dy)
        canvas = self.artist.figure.canvas
        axes = self.artist.axes
        canvas.restore_region(self.background)
        axes.draw_artist(self.artist)
        canvas.blit(axes.bbox)

    def modify_artist(self, dx, dy):
        pass

    def get_data(self):
        pass

    def on_release(self, event):
        if DraggableArtist.lock is not self: return
        xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        if (self.mode==DragType.none):   
            self.function(0, 0)
        elif (self.mode==DragType.horizontal):
            self.function(dx, 0)
        elif (self.mode==DragType.vertical):
            self.function(0, dy)
        elif (self.mode==DragType.both):
            self.function(dx, dy)
        self.press = None
        DraggableArtist.lock = None
        self.artist.set_animated(False)
        self.background = None
        self.artist.figure.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.artist.figure.canvas.mpl_disconnect(self.cidpress)
        self.artist.figure.canvas.mpl_disconnect(self.cidrelease)
        self.artist.figure.canvas.mpl_disconnect(self.cidmotion)
        

class DraggableSeries(DraggableArtist):
    def __init__(self, artist, mode=DragType.none, function=None):
        super(DraggableSeries, self).__init__(artist, mode, function)

    def get_data(self):
        self.data=self.artist.get_data()

    def modify_artist(self, dx, dy):
        self.artist.set_data(self.data[0]+dx, self.data[1]+dy)

class DraggablePatch(DraggableArtist):
    def __init__(self, artist, mode=DragType.none, function=None):
        super(DraggablePatch, self).__init__(artist, mode, function)

    def get_data(self):
        self.data=self.artist.center

    def modify_artist(self, dx, dy):
        self.artist.center = (self.data[0]+dx, self.data[1]+dy)

class DraggableRectangle(DraggableArtist):        
    def __init__(self, artist, mode=DragType.none, function=None):
        super(DraggableRectangle, self).__init__(artist, mode, function)

    def get_data(self):
        self.data=self.artist.xy

    def modify_artist(self, dx, dy):
        self.artist.set_x(self.data[0]+dx)
        self.artist.set_y(self.data[1]+dy)

class DraggableVLine(DraggableArtist):
    def __init__(self, artist, mode=DragType.none, function=None):
        super(DraggableVLine, self).__init__(artist, mode, function)

    def get_data(self):
        self.data=self.artist.get_data()

    def modify_artist(self, dx, dy):
        self.artist.set_data([self.data[0][0]+dx,self.data[0][1]+dx],[0,1])


class DraggableHLine(DraggableArtist):
    def __init__(self, artist, mode=DragType.none, function=None):
        super(DraggableHLine, self).__init__(artist, mode, function)

    def get_data(self):
        self.data=self.artist.get_data()

    def modify_artist(self, dx, dy):
        self.artist.set_data([0,1],[self.data[1][0]+dy,self.data[1][1]+dy])

class DraggableVSpan(DraggableArtist):
    def __init__(self, artist, mode=DragType.none, function=None):
        super(DraggableVSpan, self).__init__(artist, mode, function)

    def get_data(self):
        self.data=self.artist.get_xy()

    def modify_artist(self, dx, dy):
        xmin = self.data[0][0]
        xmax = self.data[2][0]
        self.artist.set_xy([[xmin+dx,0],[xmin+dx,1],[xmax+dx,1],[xmax+dx,0],[xmin+dx,0]])

class DraggableHSpan(DraggableArtist):
    def __init__(self, artist, mode=DragType.none, function=None):
        super(DraggableHSpan, self).__init__(artist, mode, function)

    def get_data(self):
        self.data=self.artist.get_xy()

    def modify_artist(self, dx, dy):
        ymin = self.data[0][1]
        ymax = self.data[1][1]
        self.artist.set_xy([[0, ymin+dy], [0, ymax+dy], [1, ymax+dy], [1 ,ymin+dy], [0, ymin+dy]])
