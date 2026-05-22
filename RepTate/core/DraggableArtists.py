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
# Copyright (2017-2026): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
import enum
from typing import Any, ClassVar, TypeAlias, cast

from RepTate.core.typing import ApplicationLike

Callback: TypeAlias = Any
ConnectionId: TypeAlias = int

class DragType(enum.Enum):
    """Describes the type of drag that the graphical object can be subjected to"""
    vertical = 1
    horizontal = 2
    both = 3
    none = 4
    special = 5

class DraggableArtist(object):
    """Abstract class for motions of a matplotlib artist"""
    lock: ClassVar["DraggableArtist | None"] = None

    def __init__(
        self,
        artist: Any = None,
        mode: DragType = DragType.none,
        function: Callback = None,
        parent_theory: Any = None,
    ) -> None:
        """**Constructor**"""
        self.parent_theory: Any = parent_theory
        self.artist: Any = artist
        self.press: Any = None
        self.background: Any = None
        self.mode: DragType = mode
        self.function: Callback = function
        self.data: Any = None
        self.cidpress: ConnectionId
        self.cidrelease: ConnectionId
        self.cidmotion: ConnectionId
        self.connect()

    def connect(self) -> None:
        """Connect events"""
        self.cidpress = self.artist.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.artist.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.artist.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event: Any) -> None:
        """Press events"""
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

    def on_motion(self, event: Any) -> None:
        """Motion event"""
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


    def modify_artist(self, dx: Any, dy: Any) -> None:
        """Do nothing"""
        pass

    def get_data(self) -> None:
        """Do nothing"""
        pass

    def on_release(self, event: Any) -> None:
        """Release event"""
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


    def disconnect(self) -> None:
        """disconnect all the stored connection ids"""
        self.artist.figure.canvas.mpl_disconnect(self.cidpress)
        self.artist.figure.canvas.mpl_disconnect(self.cidrelease)
        self.artist.figure.canvas.mpl_disconnect(self.cidmotion)

###############################################################
###############################################################


class DraggableBinSeries(DraggableArtist):
    """Dragabble histogram"""
    def __init__(
        self,
        artist: Any,
        mode: DragType = DragType.none,
        logx: bool = False,
        logy: bool = False,
        function: Callback = None,
    ) -> None:
        """**Constructor**"""
        super().__init__(artist, mode, function)
        self.logx: bool = logx
        self.logy: bool = logy
    
    def on_press(self, event: Any) -> None:
        """Press event"""
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

    def on_motion(self, event: Any) -> None:
        """Motion event"""
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

    def modify_artist(self, dx: Any, dy: Any) -> None:
        """Change artist coords"""
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

    def on_release(self, event: Any) -> None:
        """Release event"""
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
    """Draggable points of a series"""
    def __init__(
        self,
        artist: Any,
        mode: DragType = DragType.none,
        parent_application: ApplicationLike | None = None,
        function: Callback = None,
    ) -> None:
        """**Constructor**"""
        super(DraggableModesSeries, self).__init__(artist, mode, function)
        self.parent_application: ApplicationLike = cast(ApplicationLike, parent_application)
        self.update_logx_logy()
    
    def update_logx_logy(self) -> None:
        self.logx = self.parent_application.current_view.log_x
        self.logy = self.parent_application.current_view.log_y

    def on_press(self, event: Any) -> None:
        """Press event"""
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

    def on_motion(self, event: Any) -> None:
        """Motion event"""
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

    def modify_artist(self, dx: Any, dy: Any) -> None:
        """Modify artist coords"""
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

    def on_release(self, event: Any) -> None:
        """Release event"""
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


################################################################
################################################################


class DraggableModeIndividual(DraggableArtist):
    """Draggable points of a mode series, one mode at a time.

    This class is intended for theories where every mode has an independent
    horizontal and vertical coordinate.  In contrast to DraggableModesSeries, it
    never redistributes the x-coordinates of the other modes when the first or
    last mode is moved.

    The callback receives the complete updated x and y arrays:

        function(xdata, ydata)

    so theory classes can update their own parameters from the final marker
    positions.
    """

    def __init__(
        self,
        artist: Any,
        mode: DragType = DragType.both,
        parent_application: ApplicationLike | None = None,
        function: Callback = None,
    ) -> None:
        """**Constructor**"""
        super().__init__(artist, mode, function)
        self.parent_application: ApplicationLike = cast(ApplicationLike, parent_application)
        self.logx: bool = False
        self.logy: bool = False
        self.index: int = 0
        self.xdata: Any = None
        self.ydata: Any = None
        self.xdata_at_press: Any = None
        self.ydata_at_press: Any = None
        self.xpress: Any = None
        self.ypress: Any = None
        self.update_logx_logy()

    def update_logx_logy(self) -> None:
        """Update log-axis flags from the active RepTate view."""
        self.logx = self.parent_application.current_view.log_x
        self.logy = self.parent_application.current_view.log_y

    def _get_1d_artist_data(self) -> tuple[Any, Any]:
        """Return artist data as independent 1D float arrays."""
        xdata_raw, ydata_raw = self.artist.get_data()
        xdata = np.asarray(xdata_raw, dtype=float)
        ydata = np.asarray(ydata_raw, dtype=float)

        if xdata.ndim > 1:
            xdata = xdata[:, 0]
        if ydata.ndim > 1:
            ydata = ydata[:, 0]

        return xdata.copy(), ydata.copy()

    def on_press(self, event: Any) -> None:
        """Press event."""
        if event.inaxes != self.artist.axes:
            return
        if DraggableArtist.lock is not None:
            return
        if event.button != 1:
            return
        contains, attrd = self.artist.contains(event)
        if not contains:
            return
        if event.xdata is None or event.ydata is None:
            return

        self.update_logx_logy()
        self.xdata, self.ydata = self._get_1d_artist_data()
        self.xdata_at_press = self.xdata.copy()
        self.ydata_at_press = self.ydata.copy()
        self.press = event.xdata, event.ydata
        self.xpress, self.ypress = self.press

        # Pick the nearest point in the displayed data coordinates.  For log
        # views, use logarithmic distances so mode selection is visually natural
        # across several decades.
        if self.logx:
            xdist = np.log10(np.maximum(self.xdata, _LOG_FLOOR)) - np.log10(max(self.xpress, _LOG_FLOOR))
        else:
            xdist = self.xdata - self.xpress

        if self.logy:
            ydist = np.log10(np.maximum(self.ydata, _LOG_FLOOR)) - np.log10(max(self.ypress, _LOG_FLOOR))
        else:
            ydist = self.ydata - self.ypress

        self.index = int(np.argmin(xdist**2 + ydist**2))
        DraggableArtist.lock = self

        canvas = self.artist.figure.canvas
        axes = self.artist.axes
        self.artist.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.artist.axes.bbox)
        axes.draw_artist(self.artist)

    def on_motion(self, event: Any) -> None:
        """Motion event."""
        if DraggableArtist.lock is not self:
            return
        if event.inaxes != self.artist.axes:
            return
        if event.xdata is None or event.ydata is None:
            return

        self.update_logx_logy()

        if self.logx:
            dx = np.log10(max(event.xdata, _LOG_FLOOR)) - np.log10(max(self.xpress, _LOG_FLOOR))
        else:
            dx = event.xdata - self.xpress

        if self.logy:
            dy = np.log10(max(event.ydata, _LOG_FLOOR)) - np.log10(max(self.ypress, _LOG_FLOOR))
        else:
            dy = event.ydata - self.ypress

        if self.mode == DragType.none:
            self.modify_artist(0, 0)
        elif self.mode == DragType.horizontal:
            self.modify_artist(dx, 0)
        elif self.mode == DragType.vertical:
            self.modify_artist(0, dy)
        elif self.mode in (DragType.both, DragType.special):
            self.modify_artist(dx, dy)

        canvas = self.artist.figure.canvas
        axes = self.artist.axes
        canvas.restore_region(self.background)
        axes.draw_artist(self.artist)
        canvas.update()

    def modify_artist(self, dx: Any, dy: Any) -> None:
        """Move only the selected mode marker."""
        newxdata = self.xdata_at_press.copy()
        newydata = self.ydata_at_press.copy()

        if self.logx:
            newx = self.xdata_at_press[self.index] * np.power(10.0, dx)
        else:
            newx = self.xdata_at_press[self.index] + dx

        if self.logy:
            newy = self.ydata_at_press[self.index] * np.power(10.0, dy)
        else:
            newy = self.ydata_at_press[self.index] + dy

        if self.mode in (DragType.horizontal, DragType.both, DragType.special):
            newxdata[self.index] = newx
        if self.mode in (DragType.vertical, DragType.both, DragType.special):
            newydata[self.index] = newy

        self.artist.set_data(newxdata, newydata)

    def on_release(self, event: Any) -> None:
        """Release event."""
        if DraggableArtist.lock is not self:
            return

        self.press = None
        DraggableArtist.lock = None
        self.artist.set_animated(False)

        canvas = self.artist.figure.canvas
        axes = self.artist.axes
        if self.background is not None:
            canvas.restore_region(self.background)
            axes.draw_artist(self.artist)
        self.background = None

        tmp_data = self.artist.get_data()
        xdata = tmp_data[0]
        ydata = tmp_data[1]

        # Compatibility with mpldatacursor: keep the previous valid data if the
        # artist temporarily returns an unexpected nested structure.
        try:
            float(np.asarray(xdata).ravel()[0])
            self.data = tmp_data
        except (TypeError, ValueError, IndexError):
            xdata = self.data[0]
            ydata = self.data[1]

        if self.function is not None:
            self.function(np.asarray(xdata, dtype=float), np.asarray(ydata, dtype=float))


###########################################################
###########################################################

class DraggableSeries(DraggableArtist):
    """Full draggable series"""
    def __init__(
        self,
        artist: Any,
        mode: DragType = DragType.none,
        logx: bool = False,
        logy: bool = False,
        xref: Any = 0,
        yref: Any = 0,
        function: Callback = None,
        functionendshift: Callback = None,
        index: int = 0,
    ) -> None:
        """**Constructor**"""
        super(DraggableSeries, self).__init__(artist, mode, function)
        self.logx: bool = logx
        self.logy: bool = logy
        self.xref: Any = xref
        self.yref: Any = yref
        self.functionendshift: Callback = functionendshift
        self.index: int = index

        self.dx: Any = 0
        self.dy: Any = 0

    def get_data(self) -> None:
        """Return data"""
        self.data = self.artist.get_data()
    
    def on_press(self, event: Any) -> None:
        """Press event"""
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

    def on_motion(self, event: Any) -> None:
        """Motion event"""
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

    def modify_artist(self, dx: Any, dy: Any) -> None:
        """Modify artist coords"""
        if self.logx:
            newx = [x*np.power(10, dx) for x in self.data[0]]
        else:
            newx = [x + dx for x in self.data[0]]
        if self.logy:
            newy = [y*np.power(10, dy) for y in self.data[1]]
        else:
            newy = [y + dy for y in self.data[1]]
        self.artist.set_data(newx, newy)

    def on_release(self, event: Any) -> None:
        """Release event"""
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

    def disconnect(self) -> None:
        """disconnect all the stored connection ids"""
        super().disconnect()

class DraggablePatch(DraggableArtist):
    """Draggable Patch"""
    def __init__(
        self,
        artist: Any,
        mode: DragType = DragType.none,
        function: Callback = None,
    ) -> None:
        """**Constructor**"""
        super(DraggablePatch, self).__init__(artist, mode, function)

    def get_data(self) -> None:
        """Get data of the artist"""
        self.data=self.artist.center

    def modify_artist(self, dx: Any, dy: Any) -> None:
        """Modify artist coords"""
        self.artist.center = (self.data[0]+dx, self.data[1]+dy)

class DraggableRectangle(DraggableArtist):
    """Draggable rectangle"""
    def __init__(
        self,
        artist: Any,
        mode: DragType = DragType.none,
        function: Callback = None,
    ) -> None:
        """**Constructor**"""
        super(DraggableRectangle, self).__init__(artist, mode, function)

    def get_data(self) -> None:
        """Get data of the artist"""
        self.data=self.artist.xy

    def modify_artist(self, dx: Any, dy: Any) -> None:
        """Modify the artist coords"""
        self.artist.set_x(self.data[0]+dx)
        self.artist.set_y(self.data[1]+dy)

class DraggableVLine(DraggableArtist):
    """Draggable Verticla line"""
    def __init__(
        self,
        artist: Any,
        mode: DragType = DragType.none,
        function: Callback = None,
        parent_theory: Any = None,
    ) -> None:
        """**Constructor**"""
        super(DraggableVLine, self).__init__(artist, mode, function, parent_theory)
    
    def on_press(self, event: Any) -> None:
        """Press event"""
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

    def get_data(self) -> None:
        """Get the data from the artist"""
        self.data = self.artist.get_data()

    def modify_artist(self, dx: Any, dy: Any) -> None:
        """Modify the artist coordinates"""
        self.artist.set_data([self.data[0][0] + dx, self.data[0][1] + dx], [0, 1])


class DraggableHLine(DraggableArtist):
    """Draggable Horizontal line"""
    def __init__(
        self,
        artist: Any,
        mode: DragType = DragType.none,
        function: Callback = None,
        parent_theory: Any = None,
    ) -> None:
        """**Constructor**"""
        super(DraggableHLine, self).__init__(artist, mode, function, parent_theory)
    
    def on_press(self, event: Any) -> None:
        """Press event"""
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
   
    def get_data(self) -> None:
        """Get the artist data"""
        self.data = self.artist.get_data()

    def modify_artist(self, dx: Any, dy: Any) -> None:
        """Modify the artist coordinates"""
        self.artist.set_data([0, 1], [self.data[1][0] + dy, self.data[1][1] + dy])

class DraggableVSpan(DraggableArtist):
    """Draggable Vertical Span"""
    def __init__(
        self,
        artist: Any,
        mode: DragType = DragType.none,
        function: Callback = None,
    ) -> None:
        """**Constructor**"""
        super(DraggableVSpan, self).__init__(artist, mode, function)

    def get_data(self) -> None:
        """Get the artist data"""
        self.data=self.artist.get_xy()

    def modify_artist(self, dx: Any, dy: Any) -> None:
        """Modify the artist coordinates"""
        xmin = self.data[0][0]
        xmax = self.data[2][0]
        self.artist.set_xy([[xmin+dx,0],[xmin+dx,1],[xmax+dx,1],[xmax+dx,0],[xmin+dx,0]])

class DraggableHSpan(DraggableArtist):
    """Draggable Horizontal Span"""
    def __init__(
        self,
        artist: Any,
        mode: DragType = DragType.none,
        function: Callback = None,
    ) -> None:
        """**Constructor**"""
        super(DraggableHSpan, self).__init__(artist, mode, function)

    def get_data(self) -> None:
        """Get the artist data"""
        self.data=self.artist.get_xy()

    def modify_artist(self, dx: Any, dy: Any) -> None:
        """Modify the artist data"""
        ymin = self.data[0][1]
        ymax = self.data[1][1]
        self.artist.set_xy([[0, ymin+dy], [0, ymax+dy], [1, ymax+dy], [1 ,ymin+dy], [0, ymin+dy]])

class DraggableNote(DraggableArtist):
    """Draggable annotation box"""
    def __init__(
        self,
        artist: Any,
        mode: DragType = DragType.none,
        function: Callback = None,
        function2: Callback = None,
    ) -> None:
        """**Constructor**"""
        super(DraggableNote, self).__init__(artist, mode, function)
        self.cidpress = self.artist.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.function2: Callback = function2

    def get_data(self) -> None:
        """Get the artist data"""
        self.data=self.artist.get_position()

    def modify_artist(self, dx: Any, dy: Any) -> None:
        """Modify the artist position"""
        self.artist.set_position([self.press[0]+dx, self.press[1]+dy])

    def on_press(self, event: Any) -> None:
        """Press event"""
        if not event.dblclick:
            super(DraggableNote, self).on_press(event)
            return

        if event.inaxes != self.artist.axes: return
        if DraggableArtist.lock is not None: return
        if event.button != 1: return
        contains, attrd = self.artist.contains(event)
        if not contains: return
        self.function2(self.artist)
                    
    def on_release(self, event: Any) -> None:
        """Release event"""
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
