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
"""Module ApplicationReact

React module

"""
from RepTate.core.CmdBase import CmdBase, CmdMode
from RepTate.core.Application import Application
from RepTate.gui.QApplicationWindow import QApplicationWindow
from RepTate.core.View import View
from RepTate.core.FileType import TXTColumnFile
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


class ApplicationReact(CmdBase):
    """Application for Monte Carlo polymerisation

    """
    appname = 'React'
    description = 'React Application'  #used in the command-line Reptate
    extension = 'reac'

    def __new__(cls, name='React', parent=None):
        """[summary]

        [description]

        Keyword Arguments:
            - name {[type]} -- [description] (default: {'React'})
            - parent {[type]} -- [description] (default: {None})

        Returns:
            - [type] -- [description]
        """
        return GUIApplicationReact(
            name,
            parent) if (CmdBase.mode == CmdMode.GUI) else CLApplicationReact(
                name, parent)


class BaseApplicationReact:
    """[summary]

    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/React/React.html'
    appname = ApplicationReact.appname

    def __init__(self, name='React', parent=None, **kwargs):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {'React'})
            - parent {[type]} -- [description] (default: {None})
        """
        from TheoryLDPEBatch import TheoryTobitaBatch
        from TheoryTobitaCSTR import TheoryTobitaCSTR
        from TheoryMultiMetCSTR import TheoryMultiMetCSTR
        from TheoryReactMix import TheoryReactMix
        from TheoryCreatePolyconf import TheoryCreatePolyconf
        from TheoryDieneCSTR import TheoryDieneCSTR

        super().__init__(name, parent)

        # VIEWS
        # set the views that can be selected in the view combobox
        self.views["w(M)"] = View(
            name="w(M)",
            description="Molecular weight distribution",
            x_label="M",
            y_label="w",
            x_units="g/mol",
            y_units="-",
            log_x=True,
            log_y=False,
            view_proc=self.view_wM,
            n=1,
            snames=["w"])
        self.views["g(M)"] = View(
            name="g(M)",
            description="g(M)",
            x_label="M",
            y_label="g(M)",
            x_units="g/mol",
            y_units="-",
            log_x=True,
            log_y=False,
            view_proc=self.view_gM,
            n=1,
            snames=["g(M)"])
        self.views['br/1000C'] = View(
            name="br/1000C",
            description="br/1000C(M)",
            x_label="M",
            y_label="br/1000C",
            x_units="g/mol",
            y_units="-",
            log_x=True,
            log_y=False,
            view_proc=self.view_br_1000C,
            n=1,
            snames=["br/1000C"])
        self.views["log(w(M))"] = View(
            name="log(w(M))",
            description="Molecular weight distribution",
            x_label="M",
            y_label="log(w)",
            x_units="g/mol",
            y_units="-",
            log_x=True,
            log_y=False,
            view_proc=self.view_logwM,
            n=1,
            snames=["log(w)"])
        self.views["log(g(M))"] = View(
            name="log(g(M))",
            description="log(g(M))",
            x_label="M",
            y_label="log(g)",
            x_units="g/mol",
            y_units="-",
            log_x=True,
            log_y=False,
            view_proc=self.view_loggM,
            n=1,
            snames=["log(g)"])
        self.views['p(mass br) log-lin'] = View(
            name="p(mass br) log-lin",
            description="Prob. dist. of mass segement b/w branch pt log-lin scale",
            x_label="M segment",
            y_label="p(M segment)",
            x_units="g/mol",
            y_units="-",
            log_x=True,
            log_y=False,
            view_proc=self.thview_proba_mass_br,
            n=1,
            snames=["p(M segment)"],
            with_thline=False)
        self.views['p(br/molecule) log-lin'] = View(
            name="p(br/molecule) log-lin",
            description="Prob. dist. of num. branch pt per molecule log-lin scale",
            x_label="Num. br/molecule",
            y_label="p(br/molecule)",
            x_units="-",
            y_units="-",
            log_x=True,
            log_y=False,
            view_proc=self.thview_proba_num_br,
            n=1,
            snames=["p(M segment)"],
            with_thline=False)
        self.views['p(br/molecule) lin-lin'] = View(
            name="p(br/molecule) lin-lin",
            description="Prob. dist. of num. branch pt per molecule lin-lin scale",
            x_label="Num. br/molecule",
            y_label="p(br/molecule)",
            x_units="-",
            y_units="-",
            log_x=False,
            log_y=False,
            view_proc=self.thview_proba_num_br,
            n=1,
            snames=["p(M segment)"],
            with_thline=False)
        #### extra views for P&S:
        self.views['<senio(prio)> log-log'] = View(
            name="<senio(prio)> log-log",
            description="Average seniority vs priority log-log scale",
            x_label="Priority",
            y_label="Average Seniority",
            x_units="-",
            y_units="-",
            log_x=True,
            log_y=True,
            view_proc=self.thview_avsenio_v_prio,
            n=3,
            snames=["av_senio"],
            with_thline=False)
        self.views['<senio(prio)> lin-log'] = View(
            name="<senio(prio)> lin-log",
            description="Average seniority vs priority lin-log scale",
            x_label="Priority",
            y_label="Average Seniority",
            x_units="-",
            y_units="-",
            log_x=False,
            log_y=True,
            view_proc=self.thview_avsenio_v_prio,
            n=3,
            snames=["av_senio"],
            with_thline=False)
        self.views['<senio(prio)> lin-lin'] = View(
            name="<senio(prio)> lin-lin",
            description="Average seniority vs priority lin-lin scale",
            x_label="Priority",
            y_label="Average Seniority",
            x_units="-",
            y_units="-",
            log_x=False,
            log_y=False,
            view_proc=self.thview_avsenio_v_prio,
            n=3,
            snames=["av_senio"],
            with_thline=False)
        #####
        self.views['<prio(senio)> log-log'] = View(
            name="<prio(senio)> log-log",
            description="Average priority vs seniority log-log scale",
            x_label="Seniority",
            y_label="Average Priority",
            x_units="-",
            y_units="-",
            log_x=True,
            log_y=True,
            view_proc=self.thview_avprio_v_senio,
            n=3,
            snames=["av_prio"],
            with_thline=False)
        self.views['<prio(senio)> lin-log'] = View(
            name="<prio(senio)> lin-log",
            description="Average priority vs seniority lin-log scale",
            x_label="Seniority",
            y_label="Average Priority",
            x_units="-",
            y_units="-",
            log_x=False,
            log_y=True,
            view_proc=self.thview_avprio_v_senio,
            n=3,
            snames=["av_prio"],
            with_thline=False)
        self.views['<prio(senio)> lin-lin'] = View(
            name="<prio(senio)> lin-lin",
            description="Average priority vs seniority lin-lin scale",
            x_label="Seniority",
            y_label="Average Priority",
            x_units="-",
            y_units="-",
            log_x=False,
            log_y=False,
            view_proc=self.thview_avprio_v_senio,
            n=3,
            snames=["av_prio"],
            with_thline=False)
        #####
        self.views['p(senio) log-log'] = View(
            name="p(senio) log-log",
            description="seniority prob. dist. log-log",
            x_label="Seniority",
            y_label="Probability",
            x_units="-",
            y_units="-",
            log_x=True,
            log_y=True,
            view_proc=self.thview_proba_senio,
            n=1,
            snames=["proba_senio"],
            with_thline=False)
        self.views['p(senio) lin-log'] = View(
            name="p(senio) lin-log",
            description="seniority prob. dist. lin-log scale",
            x_label="Seniority",
            y_label="Probability",
            x_units="-",
            y_units="-",
            log_x=False,
            log_y=True,
            view_proc=self.thview_proba_senio,
            n=1,
            snames=["proba_senio"],
            with_thline=False)
        #####
        self.views['p(prio) log-log'] = View(
            name="p(prio) log-log",
            description="Priority prob. dist. log-log scale",
            x_label="Priority",
            y_label="Probability",
            x_units="-",
            y_units="-",
            log_x=True,
            log_y=True,
            view_proc=self.thview_proba_prio,
            n=1,
            snames=["proba_prio"],
            with_thline=False)
        self.views['p(prio) lin-log'] = View(
            name="p(prio) lin-log",
            description="Priority prob. dist. lin-log scale",
            x_label="Priority",
            y_label="Probability",
            x_units="-",
            y_units="-",
            log_x=False,
            log_y=True,
            view_proc=self.thview_proba_prio,
            n=1,
            snames=["proba_prio"],
            with_thline=False)
        ####
        self.views['<mass br(senio)> log-log'] = View(
            name="<mass br(senio)> log-log",
            description="Average mol. mass b/w branch pt vs seniority log-log scale",
            x_label="Seniority",
            y_label="Av. strand length",
            x_units="-",
            y_units="g/mol",
            log_x=True,
            log_y=True,
            view_proc=self.thview_avarmlen_v_senio,
            n=1,
            snames=["av_strand_length"],
            with_thline=False)
        self.views['<mass br(senio)> lin-lin'] = View(
            name="<mass br(senio)> lin-lin",
            description="Average mol. mass b/w branch pt vs seniority lin-lin scale",
            x_label="Seniority",
            y_label="Av. strand length",
            x_units="-",
            y_units="g/mol",
            log_x=False,
            log_y=False,
            view_proc=self.thview_avarmlen_v_senio,
            n=1,
            snames=["av_strand_length"],
            with_thline=False)
        ####
        self.views['<mass br(prio)> log-log'] = View(
            name="<mass br(prio)> log-log",
            description="Average mol. mass b/w branch pt vs priority log-log scale",
            x_label="Priority",
            y_label="Av. strand length",
            x_units="-",
            y_units="g/mol",
            log_x=True,
            log_y=True,
            view_proc=self.thview_avarmlen_v_prio,
            n=1,
            snames=["av_strand_length"],
            with_thline=False)
        self.views['<mass br(prio)> lin-lin'] = View(
            name="<mass br(prio)> lin-lin",
            description="Average mol. mass b/w branch pt vs priority lin-lin scale",
            x_label="Priority",
            y_label="Av. strand length",
            x_units="-",
            y_units="g/mol",
            log_x=False,
            log_y=False,
            view_proc=self.thview_avarmlen_v_prio,
            n=1,
            snames=["av_strand_length"],
            with_thline=False)

        self.extra_view_names = [
            '<senio(prio)> log-log', '<senio(prio)> lin-log', '<senio(prio)> lin-lin',
            '<prio(senio)> log-log', '<prio(senio)> lin-log', '<prio(senio)> lin-lin',
            'p(senio) log-log', 'p(senio) lin-log',
            'p(prio) log-log', 'p(prio) lin-log',
            '<mass br(senio)> log-log', '<mass br(senio)> lin-lin',
            '<mass br(prio)> log-log', '<mass br(prio)> lin-lin'
            ]
        #set multiviews
        self.nplots = 3
        self.multiviews = []
        for i in range(self.nplot_max):
            # set views in the same order as declared above
            self.multiviews.append(list(self.views.values())[i])
        self.multiplots.reorg_fig(self.nplots)

        # FILES
        # set the type of files that ApplicationReact can open
        ftype = TXTColumnFile(
            name='React files',
            extension='reac',
            description='Reatc file',
            col_names=['M', 'w(M)', 'g', 'br/1000C'],
            basic_file_parameters=[],
            col_units=['g/mol', '-', '-', '-'])
        self.filetypes[
            ftype.extension] = ftype  #add each the file type to dictionary

        # THEORIES
        # add the theories related to ApplicationReact to the dictionary, e.g.:
        self.theories[TheoryTobitaBatch.thname] = TheoryTobitaBatch
        self.theories[TheoryTobitaCSTR.thname] = TheoryTobitaCSTR
        self.theories[TheoryMultiMetCSTR.thname] = TheoryMultiMetCSTR
        self.theories[TheoryReactMix.thname] = TheoryReactMix
        self.theories[TheoryCreatePolyconf.thname] = TheoryCreatePolyconf
        self.theories[TheoryDieneCSTR.thname] = TheoryDieneCSTR
        self.add_common_theories()

        #set the current view
        self.set_views()
        # for _ in self.extra_view_names:
        #     self.viewComboBox.removeItem(self.viewComboBox.count() - 1)

    def change_view(self):
        """Redefinition to handle the x-range selection when P&S is selected"""
        do_priority_seniority = False
        try:
            ds = self.DataSettabWidget.currentWidget()
            th = ds.TheorytabWidget.currentWidget()
            do_priority_seniority = th.do_priority_seniority
        except Exception as e:
            pass
        super().change_view(x_vis=do_priority_seniority)


    def view_wM(self, dt, file_parameters):
        """Molecular weight distribution :math:`w(M)` vs molecular weight :math:`M` (in logarithmic scale)
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]
        return x, y, True

    def view_logwM(self, dt, file_parameters):
        """Logarithm of the molecular weight distribution :math:`\\log(w(M))` vs molecular weight :math:`M` (in logarithmic scale)
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = np.log10(dt.data[:, 1])
        return x, y, True

    def view_gM(self, dt, file_parameters):
        """:math:`g`-factor as a function of the molecular weight.
        The :math:`g`-factor is defined as :math:`g = \\dfrac{\\langle R^2_g \\rangle_\\text{branched}}{\\langle R^2_g \\rangle_\\text{linear}}`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 2]
        return x, y, True

    def view_loggM(self, dt, file_parameters):
        """Logarithm of the :math:`g`-factor as a function of the molecular weight.
        The :math:`g`-factor is defined as :math:`g = \\dfrac{\\langle R^2_g \\rangle_\\text{branched}}{\\langle R^2_g \\rangle_\\text{linear}}`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = np.log10(dt.data[:, 2])
        return x, y, True

    def view_br_1000C(self, dt, file_parameters):
        """Number of branching points per 1000 carbon as a function of the molecular weight
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 3]
        return x, y, True

    def thview_avprio_v_senio(self, dt, file_parameters):
        try:
            data = dt.extra_tables['avprio_v_senio']
        except:
            x = np.zeros((1, 3))
            y = np.zeros((1, 3))
            y[:] = np.nan
            return x, y, True

        nrows = len(data[:, 0])
        x = np.zeros((nrows, 3))
        y = np.zeros((nrows, 3))

        maxp = np.nanmax(data[:, 1])
        x[:, 0] = data[:, 0]
        y[:, 0] = data[:, 1]
        # comb limit
        x[:, 1] = data[:, 0]
        y[:, 1] = data[:, 0]
        # Cayley tree limit
        x[:, 2] = data[:, 0]
        y[:, 2] = np.power(2, data[:, 0] - 1)
        # avoid large numbers
        y[:, 2] = np.where(y[:, 2] <= maxp , y[:, 2], np.nan)

        return x, y, True

    def thview_avsenio_v_prio(self, dt, file_parameters):
        try:
            data = dt.extra_tables['avsenio_v_prio']
        except:
            x = np.zeros((1, 3))
            y = np.zeros((1, 3))
            y[:] = np.nan
            return x, y, True

        nrows = len(data[:, 0])
        x = np.zeros((nrows, 3))
        y = np.zeros((nrows, 3))

        maxs = np.nanmax(data[:, 1])
        x[:, 0] = data[:, 0]
        y[:, 0] = data[:, 1]
        # comb limit
        x[:, 1] = data[:, 0]
        y[:, 1] = data[:, 0]
        # Cayley tree limit
        x[:, 2] = data[:, 0]
        y[:, 2] = np.log(data[:, 0]) / np.log(2) + 1
        # avoid large numbers
        y[:, 1] = np.where(y[:, 1] <= maxs , y[:, 1], np.nan)

        return x, y, True

    def thview_proba_prio(self, dt, file_parameters):
        try:
            data = dt.extra_tables['proba_prio']
            is_extra = True
        except:
            is_extra = False
        if is_extra:
            nrows = len(data[:, 0])
            x = np.zeros((nrows, 1))
            y = np.zeros((nrows, 1))
            x[:, 0] = data[:, 0]
            y[:, 0] = data[:, 1]
        else:
            x = np.zeros((1, 1))
            y = np.zeros((1, 1))
            y[:] = np.nan
        return x, y, True

    def thview_proba_senio(self, dt, file_parameters):
        try:
            data = dt.extra_tables['proba_senio']
            is_extra = True
        except:
            is_extra = False
        if is_extra:
            nrows = len(data[:, 0])
            x = np.zeros((nrows, 1))
            y = np.zeros((nrows, 1))
            x[:, 0] = data[:, 0]
            y[:, 0] = data[:, 1]
        else:
            x = np.zeros((1, 1))
            y = np.zeros((1, 1))
            y[:] = np.nan
        return x, y, True

    def thview_avarmlen_v_prio(self, dt, file_parameters):
        try:
            data = dt.extra_tables['avarmlen_v_prio']
            is_extra = True
        except:
            is_extra = False
        if is_extra:
            nrows = len(data[:, 0])
            x = np.zeros((nrows, 1))
            y = np.zeros((nrows, 1))
            x[:, 0] = data[:, 0]
            y[:, 0] = data[:, 1]
        else:
            x = np.zeros((1, 1))
            y = np.zeros((1, 1))
            y[:] = np.nan
        return x, y, True

    def thview_avarmlen_v_senio(self, dt, file_parameters):
        try:
            data = dt.extra_tables['avarmlen_v_senio']
            is_extra = True
        except:
            is_extra = False
        if is_extra:
            nrows = len(data[:, 0])
            x = np.zeros((nrows, 1))
            y = np.zeros((nrows, 1))
            x[:, 0] = data[:, 0]
            y[:, 0] = data[:, 1]
        else:
            x = np.zeros((1, 1))
            y = np.zeros((1, 1))
            y[:] = np.nan
        return x, y, True

    def thview_proba_mass_br(self, dt, file_parameters):
        try:
            data = dt.extra_tables['proba_arm_wt']
            is_extra = True
        except:
            is_extra = False
        if is_extra:
            nrows = len(data[:, 0])
            x = np.zeros((nrows, 1))
            y = np.zeros((nrows, 1))
            x[:, 0] = data[:, 0]
            y[:, 0] = data[:, 1]
        else:
            x = np.zeros((1, 1))
            y = np.zeros((1, 1))
            y[:] = np.nan
        return x, y, True

    def thview_proba_num_br(self, dt, file_parameters):
        try:
            data = dt.extra_tables['proba_br_pt']
            is_extra = True
        except:
            is_extra = False
        if is_extra:
            nrows = len(data[:, 0])
            x = np.zeros((nrows, 1))
            y = np.zeros((nrows, 1))
            x[:, 0] = data[:, 0]
            y[:, 0] = data[:, 1]
        else:
            x = np.zeros((1, 1))
            y = np.zeros((1, 1))
            y[:] = np.nan
        return x, y, True

class CLApplicationReact(BaseApplicationReact, Application):
    """[summary]

    [description]
    """

    def __init__(self, name='React', parent=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {'React'})
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)
        #usually this class stays empty


class GUIApplicationReact(BaseApplicationReact, QApplicationWindow):
    """[summary]

    [description]
    """

    def __init__(self, name='React', parent=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {'React'})
            - parent {[type]} -- [description] (default: {None})
        """

        super().__init__(name, parent)

        #add the GUI-specific objects here:
        for _ in self.extra_view_names:
            self.viewComboBox.removeItem(self.viewComboBox.count() - 1)
