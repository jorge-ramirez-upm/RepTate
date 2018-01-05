# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Daniel Read, d.j.read@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module TheoryTobitaBatch

TobitaBatch file for creating a new theory
""" 
import numpy as np
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable
from PyQt5.QtWidgets import QToolBar, QTableWidget, QDialog, QVBoxLayout, QDialogButtonBox, QTableWidgetItem, QSizePolicy, QFileDialog, QLineEdit, QGroupBox, QFormLayout
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
#BoB form
from PyQt5.QtWidgets import QVBoxLayout, QDialogButtonBox, QLineEdit, QGroupBox, QFormLayout, QLabel
from PyQt5.QtGui import QIntValidator, QDoubleValidator

from react_ctypes_helper import *
from ctypes import *

class TheoryTobitaBatch(CmdBase):
    """TheoryTobitaBatch
    
    [description]
    """
    thname='TobitaBatchTheory'
    description='TobitaBatch Theory'
    citations=''

    def __new__(cls, name='ThTobitaBatch', parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThTobitaBatch'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUITheoryTobitaBatch(name, parent_dataset, ax) if (CmdBase.mode==CmdMode.GUI) else CLTheoryTobitaBatch(name, parent_dataset, ax)


class BaseTheoryTobitaBatch():
    """[summary]
    
    [description]
    """
    single_file = True # True if the theory can be applied to multiple files simultaneously

    def __init__(self, name='ThTobitaBatch', parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThTobitaBatch'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        
        self.reactname = "LDPE batch %d"%(tb_global.tobbatchnumber)
        tb_global.tobbatchnumber += 1
        self.function = self.Calc
        self.simexists = False
        self.dist_exists = False
        self.ndist = 0
        self.has_modes = False # True if the theory has modes

        self.parameters['tau'] = Parameter(name='tau', value=0.002, description='tau', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['beta'] = Parameter(name='beta', value=0.0, description='beta', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['Cb'] = Parameter(name='Cb', value=0.02, description='Cb', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['Cs'] = Parameter(name='Cs', value=0.0005, description='Cs', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['fin_conv'] = Parameter(name='fin_conv', value=0.4, description='fin_conv', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['num_to_make'] = Parameter(name='num_to_make', value=1000, description='number of molecules made in the simulation', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['mon_mass'] = Parameter(name='mon_mass', value=28, description='this is the mass, in a.m.u., of a monomer (usually set to 28 for PE)', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['Me'] = Parameter(name='Me', value=1000, description='the entanglement molecular weight', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['nbin'] = Parameter(name='nbin', value=100, description='number of bins', 
                                          type=ParameterType.real, opt_type=OptType.const)


# function TTheory_tobita_batch.Calc(var ytheory, ydata: TTable; var FileParam: TStringList;
#   var TheoryParam: array of real): Integer;
    def Calc(self, f=None):
        # var
        # i,nbins,numtomake,m:integer
        # fin_conv, tau, beta, Cb, Cs, monmass, Me:double

        # get parameters
        tau = self.parameters['tau'].value
        beta = self.parameters['beta'].value
        Cb = self.parameters['Cb'].value
        Cs = self.parameters['Cs'].value
        fin_conv = self.parameters['fin_conv'].value
        numtomake = np.round(self.parameters['num_to_make'].value)
        monmass = self.parameters['mon_mass'].value
        Me = self.parameters['Me'].value
        nbins = int(np.round(self.parameters['nbin'].value))
        
        c_ndist = c_int()

        if not self.dist_exists:
            success = request_dist(byref(c_ndist))
            self.ndist = c_ndist.value
            if not success:
                self.Qprint('Too many theories open for internal storage. Please close a theory')
                return
            self.dist_exists = True
        ndist = self.ndist
        # react_dist[ndist].name = self.reactname #TODO: set the dist name in the C library 
        react_dist[ndist].contents.polysaved = False

        if self.simexists:
            return_dist_polys(c_int(ndist))

        # initialise tobita batch
        tobbatchstart(c_double(fin_conv), c_double(tau), c_double(beta), c_double(Cs), c_double(Cb), c_int(ndist))
        react_dist[ndist].contents.npoly = 0

        react_dist[ndist].contents.M_e = Me
        react_dist[ndist].contents.monmass = monmass
        react_dist[ndist].contents.nummwdbins = nbins

        # make numtomake polymers
        i = 0
        while i < numtomake:
            if self.stop_theory_calc_flag:
                self.Qprint('Polymer creation stopped by user')
                break
            # get a polymer
            c_m = c_int()
            success = request_poly(byref(c_m))
            m = c_m.value
            if success: # check availability of polymers
            # put it in list

                if react_dist[ndist].contents.npoly == 0:  # case of first polymer made
                    react_dist[ndist].contents.first_poly = m
                    br_poly[m].contents.nextpoly = 0
                else:           # next polymer, put to top of list
                    br_poly[m].contents.nextpoly = react_dist[ndist].contents.first_poly
                    react_dist[ndist].contents.first_poly = m

                # make a polymer
                if tobbatch(c_int(m), c_int(ndist)): # routine returns false if arms ran out
                    react_dist[ndist].contents.npoly += 1
                    i += 1
                    # check for error
                    if tb_global.tobitabatcherrorflag:
                        self.Qprint('Polymers too large: gelation occurs for these parameters')
                        i = numtomake
                else: # error message if we ran out of arms
                    message = 'Ran out of storage for arm records. Options to avoid this are:\n'
                    message += '(1) Reduce number of polymers requested\n'
                    message += '(2) Adjust BoB parameters so that fewer polymers are saved\n'
                    message += '(3) Close some other theories\n'
                    message += '(4) Adjust parameters to avoid gelation'
                    self.Qprint(message)
                    i = numtomake
                    tb_global.tobitabatcherrorflag = True
                # update on number made
                if react_dist[ndist].contents.npoly % np.trunc(numtomake/20) == 0:
                    self.Qprint('Made %d polymers'%react_dist[ndist].contents.npoly)

            else:   # polymer wasn't available
                message = 'Ran out of storage for polymer records. Options to avoid this are:'
                message += '(1) Reduce number of polymers requested'
                message += '(2) Close some other theories'
                self.Qprint(message)
                i = numtomake
        # end make polymers loop
        calc = 0
        
        # do analysis of polymers made
        if (react_dist[ndist].contents.npoly >= 100) and (not tb_global.tobitabatcherrorflag):
            molbin(ndist)
            ft = f.data_table
            # print("nummwdbins=", polybits.react_dist[ndist].contents.nummwdbins)
            
            #resize theory data table
            ft = f.data_table
            tt = self.tables[f.file_name_short]
            tt.num_columns = ft.num_columns
            tt.num_rows = react_dist[ndist].contents.nummwdbins
            tt.data = np.zeros((tt.num_rows, tt.num_columns))

            for i in range(1, react_dist[ndist].contents.nummwdbins + 1):
                tt.data[i - 1, 0] = np.power(10, react_dist[ndist].contents.lgmid[i])
                tt.data[i - 1, 1] = react_dist[ndist].contents.wt[i]
                tt.data[i - 1, 2] = react_dist[ndist].contents.avg[i]
                tt.data[i - 1, 3] = react_dist[ndist].contents.avbr[i]

            self.Qprint('*************************')
            # self.Qprint('End of calculation \"%s\"'%react_dist[ndist].contents.name)
            self.Qprint('Made %d polymers'%react_dist[ndist].contents.npoly)
            self.Qprint('Saved %d polymers in memory'%react_dist[ndist].contents.nsaved)
            self.Qprint('Mn = %.3g'%react_dist[ndist].contents.m_n)
            self.Qprint('Mw = %.3g'%react_dist[ndist].contents.m_w)
            self.Qprint('br/1000C = %.3g'%react_dist[ndist].contents.brav)
            self.Qprint('*************************')
            # labelout.Caption = 'Made '+inttostr(polybits.react_dist[ndist].contents.npoly)+' polymers, Mn='
            #   +floattostrF(polybits.react_dist[ndist].contents.M_n,ffGeneral,5,2)+', Mw='
            #   +floattostrF(polybits.react_dist[ndist].contents.M_w,ffGeneral,5,2)+', br/1000C='
            #   +floattostrF(polybits.react_dist[ndist].contents.brav,ffGeneral,5,2)

            calc = react_dist[ndist].contents.nummwdbins - 1
            react_dist[ndist].contents.polysaved = True

        self.simexists = True
        self.Qprint('%d arm records left in memory'%pb_global.arms_left) 
        self.Qprint('%s'%ndist)
        return calc

    def do_error(self, line):
        pass

    def get_modes(self):
        """[summary]
        
        [description]
        
        Returns:
            [type] -- [description]
        """
        pass

    def set_modes(self):
        """[summary]
        
        [description]
        
        Arguments:

        """
        pass
        
    def destructor(self):
        """Return arms to pool"""
        return_dist(c_int(self.ndist))

class CLTheoryTobitaBatch(BaseTheoryTobitaBatch, Theory):
    """[summary]
    
    [description]
    """
    def __init__(self, name='ThTobitaBatch', parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThTobitaBatch'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
   
    # This class usually stays empty


class GUITheoryTobitaBatch(BaseTheoryTobitaBatch, QTheory):
    """[summary]
    
    [description]
    """
    def __init__(self, name='ThTobitaBatch', parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThTobitaBatch'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)

        
        #disable buttons 
        self.parent_dataset.actionMinimize_Error.setDisabled(True)
        # self.parent_dataset.actionCalculate_Theory.setDisabled(True)
        self.parent_dataset.actionShow_Limits.setDisabled(True)
        self.parent_dataset.actionVertical_Limits.setDisabled(True)
        self.parent_dataset.actionHorizontal_Limits.setDisabled(True)

        ######toolbar
        tb = QToolBar()
        tb.setIconSize(QSize(24,24))
        self.thToolsLayout.insertWidget(0, tb)

        #BOB settings buttons
        self.bob_settings_button = tb.addAction(QIcon(':/Icon8/Images/new_icons/icons8-bob-hat.png'), 'Edit BoB Binning Settings')
        self.save_bob_configuration_button = tb.addAction(QIcon(':/Icon8/Images/new_icons/icons8-money-box.png'), 'Save Polymer Configuration for BoB')
        #stop calculation button
        self.stop_calulation_button = tb.addAction(QIcon(':/Icon8/Images/new_icons/icons8-road-closure.png'), 'Stop Current Calulation')
        self.stop_calulation_button.setDisabled(True)

        #signals
        connection_id = self.bob_settings_button.triggered.connect(self.handle_edit_bob_settings)
        connection_id = self.save_bob_configuration_button.triggered.connect(self.handle_save_bob_configuration)
        connection_id = self.stop_calulation_button.triggered.connect(self.handle_stop_calulation)
    
    def theory_buttons_disabled(self, state):
        self.bob_settings_button.setDisabled(state)
        self.save_bob_configuration_button.setDisabled(state)
        self.stop_calulation_button.setDisabled(not state)


    def handle_stop_calulation(self):
        self.Qprint("Stop current calculation requested")
        self.stop_theory_calc_flag = True
        self.stop_calulation_button.setDisabled(True)

    def handle_save_bob_configuration(self):
        stars = '*************************\n'
        if self.simexists:
            ndist = self.ndist
            react_dist[ndist].contents.M_e = self.parameters['Me'].value
            react_dist[ndist].contents.monmass = self.parameters['mon_mass'].value

            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            dir_start = "data/React/polyconf.dat"
            dilogue_name = "Save"
            ext_filter = "Data Files (*.dat)"
            out_file = QFileDialog.getSaveFileName(self, dilogue_name, dir_start, options=options)
            if out_file[0] == "":
                return
            # output polymers
            b_out_file = out_file[0].encode('utf-8')
            polyconfwrite(c_int(ndist), c_char_p(b_out_file))
            message = stars + 'Saved %d polymers in %s\n'%(react_dist[ndist].contents.nsaved, out_file[0]) + stars
        else:    
            message = stars + 'No simulation performed yet\n' + stars
        self.Qprint(message)

    def handle_edit_bob_settings(self):
        ndist = self.ndist
        numbobbins = react_dist[ndist].contents.numbobbins
        bobmax = np.power(10, react_dist[ndist].contents.boblgmax)
        bobmin = np.power(10, react_dist[ndist].contents.boblgmin)
        bobbinmax = react_dist[ndist].contents.bobbinmax

        d = EditBobSettingsDialog(self, numbobbins, bobmax, bobmin, bobbinmax)
        if d.exec_():
            try:
                numbobbins = int(d.e1.text())
                bobmax = float(d.e2.text())
                bobmin = float(d.e3.text())
                bobbinmax = int(d.e4.text())
            except ValueError:
                pass
            react_dist[ndist].contents.numbobbins = c_int(numbobbins)
            react_dist[ndist].contents.boblgmax = c_double(np.log10(bobmax))
            react_dist[ndist].contents.boblgmin = c_double(np.log10(bobmin))
            react_dist[ndist].contents.bobbinmax = c_int(bobbinmax)

class EditBobSettingsDialog(QDialog):
    """Create the form that is used to modify the BoB binning settings"""

    def __init__(self, parent, numbobbins, bobmax, bobmin, bobbinmax):
        super().__init__(parent)
        self.createFormGroupBox(numbobbins, bobmax, bobmin, bobbinmax)
 
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
 
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle("Edit")
 
    def createFormGroupBox(self, numbobbins, bobmax, bobmin, bobbinmax):
        self.formGroupBox = QGroupBox("Edit BoB Binning Settings")
        layout = QFormLayout()
        
        val_double = QDoubleValidator()
        val_double.setBottom(0) #set smalled double allowed in the form
        val_int = QIntValidator()
        val_int.setBottom(0) #set smalled int allowed in the form
        
        self.e1 = QLineEdit()
        self.e1.setValidator(val_int)
        self.e1.setMaxLength(6)
        self.e1.setText("%d"%numbobbins)

        self.e2 = QLineEdit()
        self.e2.setValidator(val_double)
        self.e2.setText("%.2e"%bobmax)
        
        self.e3 = QLineEdit()
        self.e3.setValidator(val_double)
        self.e3.setText("%.2e"%bobmin)

        self.e4 = QLineEdit()
        self.e4.setValidator(val_int)
        self.e4.setMaxLength(6)
        self.e4.setText("%d"%bobbinmax)

        layout.addRow(QLabel("Number of bins for Bob:"), self.e1)
        layout.addRow(QLabel("Maximum bin Mw (g/mol):"), self.e2)
        layout.addRow(QLabel("Minimum bin Mw (g/mol):"), self.e3)
        layout.addRow(QLabel("Maximum no. of polymers per bin:"), self.e4)
        self.formGroupBox.setLayout(layout)
