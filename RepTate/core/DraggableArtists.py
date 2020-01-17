# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# --------------------------------------------------------------------------------------------------------
#
# Authors:
#     Jorge Ramirez, jorge.ramirez@upm.es
#     Victor Boudara, victor.boudara@gmail.com
#
# Useful links:
#     http://blogs.upm.es/compsoftmatter/software/reptate/
#     https://github.com/jorge-ramirez-upm/RepTate
#     http://reptate.readthedocs.io
#
# --------------------------------------------------------------------------------------------------------
#
# Copyright (2017-2020): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
#
# This file is part of RepTate.
#
# RepTate is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RepTate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RepTate.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------------------------------------------
"""Module DraggableArtists

Module for the definition of interactive graphical objects that the user can move.

""" 
# draggable matplotlib artists with the animation blit techniques; see
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from enum import Enum

class DragType(Enum):
    """[summary]
    
    [description]
    """
    vertical = 1
    horizontal = 2
    both = 3
    none = 4
    special = 5

class DraggableArtist(object):
    """Abstract class for motions of a matplotlib artist
    
    [description]
    """
    lock = None
    def __init__(self, artist=None, mode=DragType.none, function=None, parent_theory=None):
        """Constructor. 
                
        [description]
        
        Arguments:
            - artist {matplotlib artist} -- rectangle,line,patch,series to move.
        
        Keyword Arguments:
            - mode {Dragtype} -- vertical,horizontal,all,none. (default: {DragType.none})
            - function -- function that should interpret the final coordinates of the artist moved (default: {None})
        """
        self.parent_theory = parent_theory
        self.artist = artist
        self.press = None
        self.background = None
        self.mode=mode
        self.function=function
        self.data = None
        self.connect()

    def connect(self):
        """[summary]
        
        [description]
        """
        self.cidpress = self.artist.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.artist.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.artist.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            - event {[type]} -- [description]
        """
        if event.inaxes != self.artist.axes: return
        if DraggableArtist.lock is not None: return
        if event.button != 1: return
        contains, attrd = self.artist.contains(event)
        if not contains: return
        self.get_data()
        self.press = event.xdata, event.ydata
        DraggableArtist.lock = self
        canvas = self.artist.figure.canvas
        axes = self.artist.axes
        self.artist.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.artist.axes.bbox)
        axes.draw_artist(self.artist)
        canvas.update()
        #canvas.blit(axes.bbox)

    def on_motion(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            - event {[type]} -- [description]
        """
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
        # canvas.blit(axes.bbox)
        canvas.update()


    def modify_artist(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            - dx {[type]} -- [description]
            - dy {[type]} -- [description]
        """
        pass

    def get_data(self):
        """[summary]
        
        [description]
        """
        pass

    def on_release(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            event {[type]} -- [description]
        """
        if DraggableArtist.lock is not self: return
        xpress, ypress = self.press
        if event.xdata is None: return
        if event.ydata is None: return
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
        try:
            self.parent_theory.handle_actionMinimize_Error()
        except AttributeError:
            self.parent_theory.do_fit("")


    def disconnect(self):
        """disconnect all the stored connection ids
        
        [description]
        """
        self.artist.figure.canvas.mpl_disconnect(self.cidpress)
        self.artist.figure.canvas.mpl_disconnect(self.cidrelease)
        self.artist.figure.canvas.mpl_disconnect(self.cidmotion)

###############################################################
###############################################################


class DraggableBinSeries(DraggableArtist):
    """[summary]
    
    [description]
    """
    def __init__(self, artist, mode=DragType.none, logx=False, logy=False, function=None):
        """[summary]
        
        [description]
        
        Arguments:
            - artist {[type]} -- [description]
        
        Keyword Arguments:
            - mode {[type]} -- [description] (default: {DragType})
            - logx {[type]} -- [description] (default: {False})
            - logy {[type]} -- [description] (default: {False})
            - function {[type]} -- [description] (default: {None})
        """
        super().__init__(artist, mode, function)
        self.logx = logx
        self.logy = logy
    
    def on_press(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            - event {[type]} -- [description]
        """
        if event.inaxes != self.artist.axes: return
        if DraggableArtist.lock is not None: return 
        if event.button != 1: return
        contains, attrd = self.artist.contains(event)
        if not contains: return
        self.xdata, self.ydata = self.artist.get_data()
        nmodes=len(self.xdata)
        try:
            auxshape = self.xdata.shape[1]
        except IndexError:
            auxshape = 0
        if auxshape>1:
            self.xdata = self.xdata[:,0]
            self.ydata = self.ydata[:,0]
        self.xdata_at_press = self.xdata
        self.ydata_at_press = self.ydata
        self.press = event.xdata, event.ydata
        # Index of mode clicked
        self.index = np.argmin((self.xdata-self.press[0])**2+(self.ydata-self.press[1])**2)
        DraggableArtist.lock = self
        # draw everything but the selected curve and store in 'background'
        canvas = self.artist.figure.canvas
        axes = self.artist.axes
        self.artist.set_animated(True)
        canvas.draw()
        
        self.background = canvas.copy_from_bbox(self.artist.axes.bbox)
        # redraw just the curve
        axes.draw_artist(self.artist)

    def on_motion(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            - event {[type]} -- [description]
        """
        if DraggableArtist.lock is not self:
            return
        if event.inaxes != self.artist.axes:
            return
        self.xpress, self.ypress = self.press
        if self.logx:
            dx = np.log10(event.xdata) - np.log10(self.xpress)
        else:
            dx = event.xdata - self.xpress
        if self.logy:
            dy = np.log10(event.ydata) - np.log10(self.ypress)
        else:
            dy = event.ydata - self.ypress

        self.modify_artist(dx, dy)        
        
        canvas = self.artist.figure.canvas
        axes = self.artist.axes
        # restore the background
        canvas.restore_region(self.background)
        # draw the curve only
        axes.draw_artist(self.artist)
        canvas.update()

    def modify_artist(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            - dx {[type]} -- [description]
            - dy {[type]} -- [description]
        """
        xdata = self.xdata_at_press
        ydata = self.ydata_at_press
        xdataind = xdata[self.index] 
        ydataind = ydata[self.index] 
        nmodes = len(self.xdata)
        if self.logx:
            newx = self.xpress*np.power(10, dx)
        else:
            newx = self.xpress + dx
        if self.logy:
            newy = self.ypress*np.power(10, dy)
        else:
            newy = self.ypress + dy
            
        newxdata=xdata
        newydata=ydata
        # if self.index==0:
        #     newxdata[0] = newx
        #     newydata[0] = newy
        #     newxdata = np.linspace(newx, newxdata[nmodes-1], nmodes)
        #     newxdata=newxdata.reshape(nmodes,1)
        # elif self.index==nmodes-1:
        #     newxdata[self.index] = newx
        #     newydata[self.index] = newy
        #     newxdata = np.linspace(newxdata[0], newx, nmodes)
        #     newxdata=newxdata.reshape(nmodes,1)
        # else:
        newxdata[self.index] = newx
        # newydata[self.index] = newy
            

        self.artist.set_data(newxdata, newydata)

    def on_release(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            - event {[type]} -- [description]
        """
        if DraggableArtist.lock is not self: return
        xpress, ypress = self.press
        if event.xdata is None: return
        if event.ydata is None: return

        #dx = event.xdata - xpress
        #dy = event.ydata - ypress
        #if (self.mode==DragType.none):   
        #    self.function(0, 0)
        #elif (self.mode==DragType.horizontal):
        #    self.function(dx, 0)
        #elif (self.mode==DragType.vertical):
        #    self.function(0, dy)
        #elif (self.mode==DragType.both):
        #    self.function(dx, dy)
        self.press = None
        DraggableArtist.lock = None
        self.artist.set_animated(False)
        # restore the background
        canvas = self.artist.figure.canvas
        axes = self.artist.axes
        canvas.restore_region(self.background)
        # draw the curve only
        axes.draw_artist(self.artist)
        #update
        # canvas.update()
        # canvas.blit(axes.bbox)
        self.background = None
        # self.artist.figure.canvas.draw()
        self.data = self.artist.get_data()
        xdata = self.data[0]
        ydata = self.data[1]
        self.function(xdata, ydata)

################################################################        
################################################################        


class DraggableModesSeries(DraggableArtist):
    """[summary]
    
    [description]
    """
    def __init__(self, artist, mode=DragType.none, parent_application=None, function=None):
        """[summary]
        
        [description]
        
        Arguments:
            - artist {[type]} -- [description]
        
        Keyword Arguments:
            - mode {[type]} -- [description] (default: {DragType})
            - logx {[type]} -- [description] (default: {False})
            - logy {[type]} -- [description] (default: {False})
            - function {[type]} -- [description] (default: {None})
        """
        super(DraggableModesSeries, self).__init__(artist, mode, function)
        self.parent_application = parent_application
        self.update_logx_logy()
    
    def update_logx_logy(self):
        self.logx = self.parent_application.current_view.log_x
        self.logy = self.parent_application.current_view.log_y

    def on_press(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            - event {[type]} -- [description]
        """
        if event.inaxes != self.artist.axes: return
        if DraggableArtist.lock is not None: return
        if event.button != 1: return
        contains, attrd = self.artist.contains(event)
        if not contains: return
        self.xdata, self.ydata = self.artist.get_data()
        nmodes=len(self.xdata)
        auxshape = self.xdata.shape[1]
        if auxshape>1:
            self.xdata = self.xdata[:,0]
            self.ydata = self.ydata[:,0]
        self.xdata_at_press = self.xdata
        self.ydata_at_press = self.ydata
        self.press = event.xdata, event.ydata
        # Index of mode clicked
        self.index = np.argmin((self.xdata-self.press[0])**2+(self.ydata-self.press[1])**2)
        DraggableArtist.lock = self
        # draw everything but the selected curve and store in 'background'
        canvas = self.artist.figure.canvas
        axes = self.artist.axes
        self.artist.set_animated(True)
        canvas.draw()
        
        self.background = canvas.copy_from_bbox(self.artist.axes.bbox)
        # redraw just the curve
        axes.draw_artist(self.artist)
        #canvas.blit(axes.bbox)

    def on_motion(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            - event {[type]} -- [description]
        """
        if DraggableArtist.lock is not self:
            return
        if event.inaxes != self.artist.axes: return
        self.xpress, self.ypress = self.press
        self.update_logx_logy()
        if self.logx:
            dx = np.log10(event.xdata) - np.log10(self.xpress)
        else:
            dx = event.xdata - self.xpress
        if self.logy:
            dy = np.log10(event.ydata) - np.log10(self.ypress)
        else:
            dy = event.ydata - self.ypress

        self.modify_artist(dx, dy)        
        
        canvas = self.artist.figure.canvas
        axes = self.artist.axes
        # restore the background
        canvas.restore_region(self.background)
        # draw the curve only
        axes.draw_artist(self.artist)
        canvas.update()

    def modify_artist(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            - dx {[type]} -- [description]
            - dy {[type]} -- [description]
        """
        xdata = self.xdata_at_press
        ydata = self.ydata_at_press
        xdataind = xdata[self.index] 
        ydataind = ydata[self.index] 
        nmodes = len(self.xdata)
        self.update_logx_logy()
        if self.logx:
            newx = self.xpress*np.power(10, dx)
        else:
            newx = self.xpress + dx
        if self.logy:
            newy = self.ypress*np.power(10, dy)
        else:
            newy = self.ypress + dy
            
        newxdata=xdata
        newydata=ydata
        if self.index==0:
            if self.logx:
                newxdata = np.power(10, np.linspace(np.log10(newx), np.log10(newxdata[nmodes-1]), nmodes))
            else:
                newxdata = np.linspace(newx, newxdata[nmodes-1], nmodes)
            newxdata = newxdata.reshape(nmodes,1)
        elif self.index==nmodes-1:
            if self.logy:
                newxdata = np.power(10, np.linspace(np.log10(newxdata[0]), np.log10(newx), nmodes))
            else:    
                newxdata = np.linspace(newxdata[0], newx, nmodes)
            newxdata=newxdata.reshape(nmodes,1)
        
        newydata[self.index] = newy

        self.artist.set_data(newxdata, newydata)

    def on_release(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            - event {[type]} -- [description]
        """
        if DraggableArtist.lock is not self: return
        xpress, ypress = self.press
        if event.xdata is None: return
        if event.ydata is None: return

        #dx = event.xdata - xpress
        #dy = event.ydata - ypress
        #if (self.mode==DragType.none):   
        #    self.function(0, 0)
        #elif (self.mode==DragType.horizontal):
        #    self.function(dx, 0)
        #elif (self.mode==DragType.vertical):
        #    self.function(0, dy)
        #elif (self.mode==DragType.both):
        #    self.function(dx, dy)
        self.press = None
        DraggableArtist.lock = None
        self.artist.set_animated(False)
        # restore the background
        canvas = self.artist.figure.canvas
        axes = self.artist.axes
        canvas.restore_region(self.background)
        # draw the curve only
        axes.draw_artist(self.artist)
        #update
        # canvas.update()
        # canvas.blit(axes.bbox)
        self.background = None
        # self.artist.figure.canvas.draw()
        tmp_data = self.artist.get_data()
        xdata = tmp_data[0]
        ydata = tmp_data[1]
        # for compatibility with mpldatacursor
        # prevent the modes from disappearing 
        try:
            float(xdata[0])
            self.data = tmp_data
        except TypeError:
            # don't change the modes
            xdata = self.data[0]
            ydata = self.data[1]
        self.function(xdata, ydata)


###########################################################
###########################################################

class DraggableSeries(DraggableArtist):
    """[summary]
    
    [description]
    """
    def __init__(self, artist, mode=DragType.none, logx=False, logy=False, xref=0, yref=0, function=None, functionendshift=None, index=0):
        """[summary]
        
        [description]
        
        Arguments:
            - artist {[type]} -- [description]
        
        Keyword Arguments:
            - mode {[type]} -- [description] (default: {DragType})
            - logx {[type]} -- [description] (default: {False})
            - logy {[type]} -- [description] (default: {False})
        """
        super(DraggableSeries, self).__init__(artist, mode, function)
        self.logx = logx
        self.logy = logy
        self.xref = xref
        self.yref = yref
        self.functionendshift = functionendshift
        self.index = index

        self.dx = 0
        self.dy = 0

    def get_data(self):
        """[summary]
        
        [description]
        """
        self.data = self.artist.get_data()
    
    def on_press(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            - event {[type]} -- [description]
        """
        if event.inaxes != self.artist.axes: return
        if DraggableArtist.lock is not None: return
        if event.button != 1: return
        contains, attrd = self.artist.contains(event)
        if not contains: return
        self.press = event.xdata, event.ydata
        self.get_data()
        DraggableArtist.lock = self
        # draw everything but the selected curve and store in 'background'
        canvas = self.artist.figure.canvas
        axes = self.artist.axes
        self.artist.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.artist.axes.bbox)
        # redraw just the curve
        axes.draw_artist(self.artist)
        #canvas.blit(axes.bbox)

    def on_motion(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            - event {[type]} -- [description]
        """
        if DraggableArtist.lock is not self:
            return
        if event.inaxes != self.artist.axes: return
        xpress, ypress = self.press
        if self.logx:
            self.dx = np.log10(event.xdata) - np.log10(xpress)
        else:
            self.dx = event.xdata - xpress
        if self.logy:
            self.dy = np.log10(event.ydata) - np.log10(ypress)
        else:
            self.dy = event.ydata - ypress

        if (self.mode==DragType.none):   
            self.modify_artist(0, 0)
            self.function(0, 0, self.index)
        elif (self.mode==DragType.horizontal):
            self.modify_artist(self.dx, 0)
            self.function(self.dx, 0, self.index)
        elif (self.mode==DragType.vertical):
            self.modify_artist(0, self.dy)
            self.function(0, self.dy, self.index)
        elif (self.mode==DragType.both):
            self.modify_artist(self.dx, self.dy)
            self.function(self.dx, self.dy, self.index)
        
        canvas = self.artist.figure.canvas
        axes = self.artist.axes
        # restore the background
        canvas.restore_region(self.background)
        # draw the curve only
        axes.draw_artist(self.artist)
        canvas.update()

    def modify_artist(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            - dx {[type]} -- [description]
            - dy {[type]} -- [description]
        """
        if self.logx:
            newx = [x*np.power(10, dx) for x in self.data[0]]
        else:
            newx = [x + dx for x in self.data[0]]
        if self.logy:
            newy = [y*np.power(10, dy) for y in self.data[1]]
        else:
            newy = [y + dy for y in self.data[1]]
        self.artist.set_data(newx, newy)

    def on_release(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            - event {[type]} -- [description]
        """
        if DraggableArtist.lock is not self: return
        if (self.mode==DragType.none):   
            self.functionendshift(0, 0, self.index)
        elif (self.mode==DragType.horizontal):
            self.functionendshift(self.dx, 0, self.index)
        elif (self.mode==DragType.vertical):
            self.functionendshift(0, self.dy, self.index)
        elif (self.mode==DragType.both):
            self.functionendshift(self.dx, self.dy, self.index)
        self.press = None
        DraggableArtist.lock = None
        self.artist.set_animated(False)
        # restore the background
        canvas = self.artist.figure.canvas
        axes = self.artist.axes
        canvas.restore_region(self.background)
        # draw the curve only
        axes.draw_artist(self.artist)
        #update
        # canvas.update()
        # canvas.blit(axes.bbox)
        self.background = None
        # self.artist.figure.canvas.draw()

    def disconnect(self):
        """disconnect all the stored connection ids
        
        [description]
        """
        super().disconnect()

class DraggablePatch(DraggableArtist):
    """[summary]
    
    [description]
    """
    def __init__(self, artist, mode=DragType.none, function=None):
        """[summary]
        
        [description]
        
        Arguments:
            - artist {[type]} -- [description]
        
        Keyword Arguments:
            - mode {[type]} -- [description] (default: {DragType})
            - function {[type]} -- [description] (default: {None})
        """
        super(DraggablePatch, self).__init__(artist, mode, function)

    def get_data(self):
        """[summary]
        
        [description]
        """
        self.data=self.artist.center

    def modify_artist(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            - dx {[type]} -- [description]
            - dy {[type]} -- [description]
        """
        self.artist.center = (self.data[0]+dx, self.data[1]+dy)

class DraggableRectangle(DraggableArtist):
    """[summary]
    
    [description]
    """
    def __init__(self, artist, mode=DragType.none, function=None):
        """[summary]
        
        [description]
        
        Arguments:
            - artist {[type]} -- [description]
        
        Keyword Arguments:
            - mode {[type]} -- [description] (default: {DragType})
            - function {[type]} -- [description] (default: {None})
        """
        super(DraggableRectangle, self).__init__(artist, mode, function)

    def get_data(self):
        """[summary]
        
        [description]
        """
        self.data=self.artist.xy

    def modify_artist(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            - dx {[type]} -- [description]
            - dy {[type]} -- [description]
        """
        self.artist.set_x(self.data[0]+dx)
        self.artist.set_y(self.data[1]+dy)

class DraggableVLine(DraggableArtist):
    """[summary]
    
    [description]
    """
    def __init__(self, artist, mode=DragType.none, function=None, parent_theory=None):
        """[summary]
        
        [description]
        
        Arguments:
            - artist {[type]} -- [description]
        
        Keyword Arguments:
            - mode {[type]} -- [description] (default: {DragType})
            - function {[type]} -- [description] (default: {None})
        """
        super(DraggableVLine, self).__init__(artist, mode, function, parent_theory)
    
    def on_press(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            - event {[type]} -- [description]
        """
        if event.inaxes != self.artist.axes: return
        if DraggableArtist.lock is not None: return
        if event.button != 1: return
        contains, attrd = self.artist.contains(event)
        if not contains: return
        self.get_data()
        self.press = self.data[0][0], 0 # do not use event.xdata, precision matters in non-logscale
        DraggableArtist.lock = self
        canvas = self.artist.figure.canvas
        axes = self.artist.axes
        self.artist.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.artist.axes.bbox)
        axes.draw_artist(self.artist)
        canvas.update()
        #canvas.blit(axes.bbox)

    def get_data(self):
        """[summary]
        
        [description]
        """
        self.data = self.artist.get_data()

    def modify_artist(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            - dx {[type]} -- [description]
            - dy {[type]} -- [description]
        """
        self.artist.set_data([self.data[0][0] + dx, self.data[0][1] + dx], [0, 1])


class DraggableHLine(DraggableArtist):
    """[summary]
    
    [description]
    """
    def __init__(self, artist, mode=DragType.none, function=None, parent_theory=None):
        """[summary]
        
        [description]
        
        Arguments:
            - artist {[type]} -- [description]
        
        Keyword Arguments:
            - mode {[type]} -- [description] (default: {DragType})
            - function {[type]} -- [description] (default: {None})
        """
        super(DraggableHLine, self).__init__(artist, mode, function, parent_theory)
    
    def on_press(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            - event {[type]} -- [description]
        """
        if event.inaxes != self.artist.axes: return
        if DraggableArtist.lock is not None: return
        if event.button != 1: return
        contains, attrd = self.artist.contains(event)
        if not contains: return
        self.get_data()
        self.press = 0, self.data[1][0] # do not use event.ydata, precision matters in non-logscale
        DraggableArtist.lock = self
        canvas = self.artist.figure.canvas
        axes = self.artist.axes
        self.artist.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.artist.axes.bbox)
        axes.draw_artist(self.artist)
        canvas.update()
        #canvas.blit(axes.bbox)
   
    def get_data(self):
        """[summary]
        
        [description]
        """
        self.data = self.artist.get_data()

    def modify_artist(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            - dx {[type]} -- [description]
            - dy {[type]} -- [description]
        """
        self.artist.set_data([0, 1], [self.data[1][0] + dy, self.data[1][1] + dy])

class DraggableVSpan(DraggableArtist):
    """[summary]
    
    [description]
    """
    def __init__(self, artist, mode=DragType.none, function=None):
        """[summary]
        
        [description]
        
        Arguments:
            - artist {[type]} -- [description]
        
        Keyword Arguments:
            - mode {[type]} -- [description] (default: {DragType})
            - function {[type]} -- [description] (default: {None})
        """
        super(DraggableVSpan, self).__init__(artist, mode, function)

    def get_data(self):
        """[summary]
        
        [description]
        """
        self.data=self.artist.get_xy()

    def modify_artist(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            - dx {[type]} -- [description]
            - dy {[type]} -- [description]
        """
        xmin = self.data[0][0]
        xmax = self.data[2][0]
        self.artist.set_xy([[xmin+dx,0],[xmin+dx,1],[xmax+dx,1],[xmax+dx,0],[xmin+dx,0]])

class DraggableHSpan(DraggableArtist):
    """[summary]
    
    [description]
    """
    def __init__(self, artist, mode=DragType.none, function=None):
        """[summary]
        
        [description]
        
        Arguments:
            - artist {[type]} -- [description]
        
        Keyword Arguments:
            - mode {[type]} -- [description] (default: {DragType})
            - function {[type]} -- [description] (default: {None})
        """
        super(DraggableHSpan, self).__init__(artist, mode, function)

    def get_data(self):
        """[summary]
        
        [description]
        """
        self.data=self.artist.get_xy()

    def modify_artist(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            - dx {[type]} -- [description]
            - dy {[type]} -- [description]
        """
        ymin = self.data[0][1]
        ymax = self.data[1][1]
        self.artist.set_xy([[0, ymin+dy], [0, ymax+dy], [1, ymax+dy], [1 ,ymin+dy], [0, ymin+dy]])

class DraggableNote(DraggableArtist):
    """[summary]
    
    [description]
    """
    def __init__(self, artist, mode=DragType.none, function=None, function2=None):
        """[summary]
        
        [description]
        
        Arguments:
            - artist {[type]} -- [description]
        
        Keyword Arguments:
            - mode {[type]} -- [description] (default: {DragType})
            - function {[type]} -- [description] (default: {None})
            - function2 {[type]} -- [description] (default: {None})
        """
        super(DraggableNote, self).__init__(artist, mode, function)
        self.cidpress = self.artist.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.function2=function2

    def get_data(self):
        """[summary]
        
        [description]
        """
        self.data=self.artist.get_position()

    def modify_artist(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            - dx {[type]} -- [description]
            - dy {[type]} -- [description]
        """
        self.artist.set_position([self.press[0]+dx, self.press[1]+dy])

    def on_press(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            - event {[type]} -- [description]
        """
        if not event.dblclick:
            super(DraggableNote, self).on_press(event)
            return

        if event.inaxes != self.artist.axes: return
        if DraggableArtist.lock is not None: return
        if event.button != 1: return
        contains, attrd = self.artist.contains(event)
        if not contains: return
        self.function2(self.artist)
                    
    def on_release(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            - event {[type]} -- [description]
        """
        if DraggableArtist.lock is not self: return
        xpress, ypress = self.press
        if event.xdata is None: return
        if event.ydata is None: return
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.press = None
        DraggableArtist.lock = None
        self.artist.set_animated(False)
        self.background = None
        self.artist.figure.canvas.draw()
