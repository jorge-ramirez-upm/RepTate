import numpy as np
import ctypes as ct
import react_ctypes_helper as rch
#BoB form
from PyQt5.QtWidgets import QDialog, QToolBar, QVBoxLayout,QHBoxLayout, QDialogButtonBox, QLineEdit, QGroupBox, QFormLayout, QLabel, QFileDialog, QRadioButton, QSpinBox, QGridLayout, QSizePolicy, QSpacerItem, QScrollArea, QWidget, QCheckBox
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QIcon
from PyQt5.QtCore import QSize, Qt
import psutil

def request_more_polymer(parent_theory):
    """Generic function called when run out of polymers"""
    success_increase_memory = None
    success_increase_memory = handle_increase_records(parent_theory, 'polymer')
    while success_increase_memory is None:
        pass
    # except:
    #     success_increase_memory = False
    if not success_increase_memory:
        message = 'Ran out of storage for polymer records. Options to avoid this are:'
        message += '(1) Reduce number of polymers requested'
        message += '(2) Close some other theories'
        parent_theory.print_signal.emit(message)
    else:
        parent_theory.print_signal.emit('Number of polymers was increased')
    
    parent_theory.success_increase_memory = success_increase_memory

def request_more_arm(parent_theory):
    """Generic function called when run out of arms"""
    success_increase_memory = None
    success_increase_memory = handle_increase_records(parent_theory, 'arm')
    while success_increase_memory is None:
        pass
    # except:
    #     success_increase_memory = False

    if not success_increase_memory:
        message = 'Ran out of storage for arm records. Options to avoid this are:\n'
        message += '(1) Reduce number of polymers requested\n'
        message += '(2) Adjust BoB parameters so that fewer polymers are saved\n'
        message += '(3) Close some other theories\n'
        message += '(4) Adjust parameters to avoid gelation'
        parent_theory.print_signal.emit(message)
        # i = numtomake
        # rch.tCSTR_global.tobitaCSTRerrorflag = True
    else:
        parent_theory.print_signal.emit('Number of arms was increased')
    parent_theory.success_increase_memory = success_increase_memory

def request_more_dist(parent_theory):
    """Generic function called when run out of distributions"""
    success_increase_memory = None
    success_increase_memory = handle_increase_records(parent_theory, 'dist')
    # parent_theory.increase_memory.emit("dist")
    while success_increase_memory is None:
        pass
    # except:
    #     success_increase_memory = False
    if success_increase_memory:
        rch.link_react_dist() #re-link the python array with the C array
        parent_theory.print_signal.emit('Number of dist. was increased')
        parent_theory.handle_actionCalculate_Theory()
    else:
        parent_theory.print_signal.emit('Too many theories open for internal storage.\nPlease close a theory or increase records"')


def initialise_tool_bar(parent_theory):
    """Add icons in theory toolbar"""
    #disable buttons 
    parent_theory.parent_dataset.actionMinimize_Error.setDisabled(True)
    # parent_theory.parent_dataset.actionCalculate_Theory.setDisabled(True)
    parent_theory.parent_dataset.actionShow_Limits.setDisabled(True)
    parent_theory.parent_dataset.actionVertical_Limits.setDisabled(True)
    parent_theory.parent_dataset.actionHorizontal_Limits.setDisabled(True)

    ######toolbar
    tb = QToolBar()
    tb.setIconSize(QSize(24,24))
    parent_theory.thToolsLayout.insertWidget(0, tb)

    #BOB settings buttons
    parent_theory.bob_settings_button = tb.addAction(QIcon(':/Icon8/Images/new_icons/icons8-bob-hat.png'), 'Edit BoB Binning Settings')
    parent_theory.save_bob_configuration_button = tb.addAction(QIcon(':/Icon8/Images/new_icons/icons8-money-box.png'), 'Save Polymer Configuration for BoB')
    #stop calculation button
    parent_theory.stop_calulation_button = tb.addAction(QIcon(':/Icon8/Images/new_icons/icons8-road-closure.png'), 'Stop Current Calulation')
    parent_theory.stop_calulation_button.setDisabled(True)

    #signals
    connection_id = parent_theory.bob_settings_button.triggered.connect(parent_theory.handle_edit_bob_settings)
    connection_id = parent_theory.save_bob_configuration_button.triggered.connect(parent_theory.handle_save_bob_configuration)
    connection_id = parent_theory.stop_calulation_button.triggered.connect(parent_theory.handle_stop_calulation)

def theory_buttons_disabled(parent_theory, state):
    """
    Enable/Disable theory buttons, typically called at the start and stop of a calculation.
    This is relevant in multithread mode only.
    """
    parent_theory.bob_settings_button.setDisabled(state)
    parent_theory.save_bob_configuration_button.setDisabled(state)
    parent_theory.stop_calulation_button.setDisabled(not state)


def handle_stop_calulation(parent_theory):
    """
    Raise a flag to kindly notify the thread Calc routine to stop.
    This is relevant in multithread mode only.
    """
    parent_theory.print_signal.emit("Stop current calculation requested")
    parent_theory.stop_theory_calc_flag = True
    parent_theory.stop_calulation_button.setDisabled(True)



def handle_save_mix_configuration(parent_theory):
    """
    Launch a dialog to select a filename where to save the polymer configurations.
    Then call the C routine 'multipolyconfwrite' that the data into the selected file
    """
    stars = '*************************'
    if parent_theory.simexists:
        ndist = parent_theory.ndist
        rch.react_dist[ndist].contents.M_e = parent_theory.parameters['Me'].value
        rch.react_dist[ndist].contents.monmass = parent_theory.parameters['mon_mass'].value

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dir_start = "data/React/polyconf.dat"
        dilogue_name = "Save"
        ext_filter = "Data Files (*.dat)"
        out_file = QFileDialog.getSaveFileName(parent_theory, dilogue_name, dir_start, options=options)
        if out_file[0] == "":
            return
        # output polymers
        b_out_file = out_file[0].encode('utf-8')
        rch.polyconfwrite(ct.c_int(ndist), ct.c_char_p(b_out_file))
        message = stars + '\nSaved %d polymers in %s\n'%(rch.react_dist[ndist].contents.nsaved, out_file[0]) + stars
    else:    
        message = stars + '\nNo simulation performed yet\n' + stars
    parent_theory.print_signal.emit(message)

def handle_save_bob_configuration(parent_theory):
    """
    Launch a dialog to select a filename where to save the polymer configurations.
    Then call the C routine 'polyconfwrite' that the data into the selected file
    """
    stars = '*************************'
    if parent_theory.simexists:
        ndist = parent_theory.ndist
        rch.react_dist[ndist].contents.M_e = parent_theory.parameters['Me'].value
        rch.react_dist[ndist].contents.monmass = parent_theory.parameters['mon_mass'].value

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dir_start = "data/React/polyconf.dat"
        dilogue_name = "Save"
        ext_filter = "Data Files (*.dat)"
        out_file = QFileDialog.getSaveFileName(parent_theory, dilogue_name, dir_start, options=options)
        if out_file[0] == "":
            return
        # output polymers
        b_out_file = out_file[0].encode('utf-8')
        rch.polyconfwrite(ct.c_int(ndist), ct.c_char_p(b_out_file))
        message = stars + '\nSaved %d polymers in %s\n'%(rch.react_dist[ndist].contents.nsaved, out_file[0]) + stars
    else:    
        message = stars + '\nNo simulation performed yet\n' + stars
    parent_theory.print_signal.emit(message)

def handle_edit_bob_settings(parent_theory):
    """Launch a dialog and modify the BoB binning settings if the user press "OK", else nothing happend."""
    ndist = parent_theory.ndist
    numbobbins = rch.react_dist[ndist].contents.numbobbins
    bobmax = np.power(10, rch.react_dist[ndist].contents.boblgmax)
    bobmin = np.power(10, rch.react_dist[ndist].contents.boblgmin)
    bobbinmax = rch.react_dist[ndist].contents.bobbinmax

    d = EditBobSettingsDialog(parent_theory, numbobbins, bobmax, bobmin, bobbinmax)
    if d.exec_():
        try:
            numbobbins = int(d.e1.text())
            bobmax = float(d.e2.text())
            bobmin = float(d.e3.text())
            bobbinmax = int(d.e4.text())
        except ValueError:
            pass
        rch.react_dist[ndist].contents.numbobbins = ct.c_int(numbobbins)
        rch.react_dist[ndist].contents.boblgmax = ct.c_double(np.log10(bobmax))
        rch.react_dist[ndist].contents.boblgmin = ct.c_double(np.log10(bobmin))
        rch.react_dist[ndist].contents.bobbinmax = ct.c_int(bobbinmax)

def handle_increase_records(parent_theory, name):
    """Launch a dialog asking if the user what to allocate more memory for arms, polymers, or distribution.
        'name' should be "arm", "polymer", or "dist".
    """
    if name == "arm":
        current_max = rch.pb_global_const.maxarm
        f = rch.increase_arm_records_in_arm_pool
        size_of = 75e-6 #size of an 'arm' structure (MB) in C
    elif name == "polymer":
        current_max = rch.pb_global_const.maxpol
        f = rch.increase_polymer_records_in_br_poly
        size_of = 45e-6 #size of a 'polymer' structure (MB) in C
    elif name == "dist":
        current_max = rch.pb_global_const.maxreact
        f = rch.increase_dist_records_in_react_dist
        size_of = 60097e-6 #size of a 'dist' structure (MB) in C
    else:
        return False 
    d = IncreaseRecordsDialog(parent_theory, current_max, name, size_of) #create the dialog
    if d.exec_():
        if d.r1.isChecked():
            new_max = int(np.ceil(current_max*1.5))
        if d.r2.isChecked():
            new_max = int(current_max*2)
        if d.r3.isChecked():
            new_max = int(current_max*5)
        success = f(ct.c_int(new_max)) #call C routine to allocate more memory (using 'realloc')
        if not success:
            parent_theory.print_signal.emit("Allocation of new memory failed\n%d %s records in memory"%(current_max, name))
        return success
    else:
        return False

###################

class ParameterReactMix(QDialog):
    """Create form to input the MultiMetCSTR parameters"""

    def __init__(self, parent_theory):
        super().__init__(parent_theory)
        self.parent_theory = parent_theory
        self.opened_react_theories = []
        self.list_all_open_react_theories()
        self.make_lines()
        self.createFormGroupBox(self.opened_react_theories)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept_)
        buttonBox.rejected.connect(self.reject)
        apply_button = buttonBox.button(QDialogButtonBox.Apply)
        apply_button.clicked.connect(self.handle_apply)
 
        #insert widgets
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.scroll)
        self.mainLayout.addStretch()
        self.mainLayout.addWidget(buttonBox)
        self.setLayout(self.mainLayout)
        self.setWindowTitle("Enter Mix Parameters")
        self.resize(self.mainLayout.sizeHint())
    
    def accept_(self):
        """
        Triggered when 'OK' button is pushed. Call 'get_lines()'
        
        """
        self.compute_weights()
        self.get_lines()
        self.accept()

    def compute_weights(self):
        """Update the 'weight' column based on the 'ratio' values"""
        sum_ratio = 0
        for i in range (len(self.opened_react_theories)):
            # IF 'is included?' is checked and Ratio > 0
            is_checked = self.lines[i][3].isChecked()
            ratio = float(self.lines[i][4].text())
            if is_checked and ratio > 0: 
                sum_ratio += ratio 
        
        for i in range (len(self.opened_react_theories)):
            is_checked = self.lines[i][3].isChecked()
            ratio = float(self.lines[i][4].text())
            if is_checked and ratio > 0: 
                weight = ratio/sum_ratio
                self.lines[i][5].setText('%.7g'%weight)
            else:
                self.lines[i][3].setChecked(False)
                self.lines[i][5].setText('0')

    def handle_apply(self):
        """
        Update the values of 'is checked?' and 'weight' columns.
        Triggered when 'Apply' button is pushed.
        
        """
        self.compute_weights()

    def make_lines(self):
        """Create the input-parameter-form lines with default parameter values"""
        dvalidator = QDoubleValidator() #prevent letters etc.
        dvalidator.setBottom(0) #minimum allowed value
        self.lines = []
        for th in self.opened_react_theories:
            line = []
            ndist = th.ndist
            ds = th.parent_dataset
            #find theory tab-name
            th_index = ds.TheorytabWidget.indexOf(th)
            th_tab_name =  ds.TheorytabWidget.tabText(th_index)
            #find applicatino tab-name
            app = ds.parent_application
            manager = app.parent_manager
            app_index = manager.ApplicationtabWidget.indexOf(app)
            app_tab_name =  manager.ApplicationtabWidget.tabText(app_index)

            line.append(QLabel('%s/%s'%(app_tab_name, th_tab_name))) #Name
            line.append(QLabel('%.4g'%rch.react_dist[ndist].contents.npoly)) #no. generated
            line.append(QLabel('%.4g'%rch.react_dist[ndist].contents.nsaved)) #no. saved
            line.append(QCheckBox()) #is included? - unchecked by default
            qledit = QLineEdit()
            qledit.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Maximum)
            qledit.setValidator(dvalidator)  
            qledit.setText('0.0')
            line.append(qledit) #ratio
            line.append(QLabel('0.0')) #weight
            self.lines.append(line)
    
    def get_lines(self):
        """Called when 'OK' is pressed"""
        self.parent_theory.dists = []
        self.parent_theory.weights = []
        self.parent_theory.theory_names = []
        for i in range(len(self.opened_react_theories)):
            if self.lines[i][3].isChecked():
                self.parent_theory.dists.append(self.opened_react_theories[i].ndist) #get ndist
                self.parent_theory.weights.append(self.lines[i][5].text()) #get weight
                self.parent_theory.theory_names.append(self.lines[i][0].text()) #get theory name
        self.parent_theory.n_inmix = len(self.parent_theory.weights) #get number of included theories in mix


    def createFormGroupBox(self, theory_list):
        """Create a form to set the new values of mix parameters"""
        self.formGroupBox = QGroupBox()
        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(QLabel('<b>App/Theory</b>'), 0, 1)
        layout.addWidget(QLabel('<b>No. generated</b>'), 0, 2)
        layout.addWidget(QLabel('<b>No. saved</b>'), 0, 3)
        layout.addWidget(QLabel('<b>Include?</b>'), 0, 4)
        layout.addWidget(QLabel('<b>Ratio</b>'), 0, 5)
        layout.addWidget(QLabel('<b>Weight fraction</b>'), 0, 6)

        for i in range(len(theory_list)):
            layout.addWidget(QLabel('<b>%d</b>'%(i + 1)), i + 1, 0)
            for j in range(len(self.lines[0])):
                layout.addWidget(self.lines[i][j], i + 1, j + 1)
        self.formGroupBox.setLayout(layout)
                
        #Scroll Area Properties
        self.scroll = QScrollArea()
        self.scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.formGroupBox)
        
    def list_all_open_react_theories(self):
        """List all oppened React theories in RepTate, excluding the Mix theories"""
        self.opened_react_theories = []
        current_manager = self.parent_theory.parent_dataset.parent_application.parent_manager

        for app in current_manager.applications.values(): #list all opened apps
            if (app.name.rstrip("0123456789") == 'React'): #select only React application
                for ds in app.datasets.values(): #loop over datasets
                    for th in ds.theories.values(): #loop over theories
                        if th.reactname != 'ReactMix' and th.simexists: # exclude React Mix theories
                            self.opened_react_theories.append(th)


###################

class ParameterMultiMetCSTR(QDialog):
    """Create form to input the MultiMetCSTR parameters"""

    def __init__(self, parent_theory):
        super().__init__(parent_theory)
        self.parent_theory = parent_theory
        self.numcat_max = parent_theory.numcat_max #maximum number of catalysts
        self.make_lines(parent_theory.pvalues)
        self.createFormGroupBox(parent_theory.numcat)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept_)
        buttonBox.rejected.connect(self.reject)
 
        hwidget = QGroupBox()
        hlayout = QHBoxLayout()
        #set spinBox ncatalyst
        hlayout.addWidget(QLabel('<b>N. of catalysts</b>') )
        self.sb_ncatalyst = QSpinBox()
        self.sb_ncatalyst.setMinimum(1)
        self.sb_ncatalyst.setMaximum(self.numcat_max)
        self.sb_ncatalyst.setValue(parent_theory.numcat)
        self.sb_ncatalyst.valueChanged.connect(self.handle_sb_ncatalyst_valueChanged)
        hlayout.addWidget(self.sb_ncatalyst)
        #set time const box
        hlayout.addStretch()
        hlayout.addWidget(QLabel('<b>Time constant</b>'))
        dvalidator = QDoubleValidator() #prevent letters etc.
        dvalidator.setBottom(0) #minimum allowed value
        self.time_const = QLineEdit()
        self.time_const.setValidator(dvalidator)  
        self.time_const.setText('%s'%parent_theory.time_const)
        hlayout.addWidget(self.time_const)
        #set monomer concentration box
        hlayout.addStretch()
        hlayout.addWidget(QLabel('<b>Monomer conc.</b>'))
        dvalidator = QDoubleValidator() #prevent letters etc.
        dvalidator.setBottom(0) #minimum allowed value
        self.monomer_conc = QLineEdit()
        self.monomer_conc.setValidator(dvalidator)  
        self.monomer_conc.setText('%s'%parent_theory.monomer_conc)
        hlayout.addWidget(self.monomer_conc)
        #set horizontal layout
        hwidget.setLayout(hlayout)

        #insert widgets
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(hwidget)
        self.mainLayout.addWidget(self.scroll)
        self.mainLayout.addStretch()
        self.mainLayout.addWidget(buttonBox)
        self.setLayout(self.mainLayout)
        self.setWindowTitle("Enter Metallocene Polymerisation Parameters")

    def accept_(self):
        """
        Triggered when 'OK' button is pushed. Call 'get_lines()'
        
        """
        self.get_lines()
        self.accept()

    def make_lines(self, source):
        """Create the input-parameter-form lines with default parameter values"""
        dvalidator = QDoubleValidator() #prevent letters etc.
        dvalidator.setBottom(0) #minimum allowed value
        qledit = QLineEdit()
        qledit.setValidator(dvalidator)  
        qledit.setText('0.0') #new lines contain zeros
        self.lines = []
        for i in range(self.numcat_max):
            line = []
            for j in range(5):
                qledit = QLineEdit()
                qledit.setValidator(dvalidator)  
                qledit.setText(source[i][j])
                line.append(qledit)
            self.lines.append(line)

    def save_lines(self):
        """Save the current form values.
        Called when the number of lines in the form is changed.
        """
        self.lines_saved = [['0' for j in range(5)] for i in range(self.numcat_max)]
        for i in range(self.numcat_max):
            for j in range(5):
                self.lines_saved[i][j] = self.lines[i][j].text()
    
    def get_lines(self):
        """Save input parameters. Called when 'OK' is pressed"""
        self.parent_theory.numcat = self.sb_ncatalyst.value()
        self.parent_theory.time_const = float(self.time_const.text())
        self.parent_theory.monomer_conc = float(self.monomer_conc.text())
        for i in range(self.numcat_max):
            for j in range(5):
                self.parent_theory.pvalues[i][j] = self.lines[i][j].text()

    def handle_sb_ncatalyst_valueChanged(self, ncatalyst):
        """Handle a change of the number of catalysts.
        Destroy the form and create new one with the selected number of line
        Keep the values previously entered
        """
        self.save_lines()
        self.mainLayout.removeWidget(self.scroll)
        self.scroll.deleteLater()
        self.scroll = None
        self.make_lines(self.lines_saved)
        self.createFormGroupBox(ncatalyst)
        self.mainLayout.insertWidget(1, self.scroll) #insert above OK/Cancel buttons

    def createFormGroupBox(self, ncatalyst):
        """Create a form to set the new values of polymerisation parameters"""
        self.formGroupBox = QGroupBox()

        layout = QGridLayout()
        layout.setSpacing(10)
        
        layout.addWidget(QLabel('<center><b>Catalyst conc.</center></b>'), 0, 1)
        layout.addWidget(QLabel('<center><b>K<sub>p</sub></b></center>'), 0, 2)
        layout.addWidget(QLabel('<center><b>K<sup>=</sup></b></center>'), 0, 3)
        layout.addWidget(QLabel('<center><b>K<sub>s</sub></b></center>'), 0, 4)
        layout.addWidget(QLabel('<center><b>K<sub>pLCB</sub></b></center>'), 0, 5)
        for i in range(ncatalyst):
            layout.addWidget(QLabel('<b>%d</b>'%(i + 1)), i + 1, 0)
            for j in range(5):
                layout.addWidget(self.lines[i][j], i + 1, j + 1)
        self.formGroupBox.setLayout(layout)
                
        #Scroll Area Properties
        self.scroll = QScrollArea()
        self.scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.formGroupBox)

###############################################


class EditBobSettingsDialog(QDialog):
    """Create the form that is used to modify the BoB binning settings"""

    def __init__(self, parent_theory, numbobbins, bobmax, bobmin, bobbinmax):
        super().__init__(parent_theory)
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
        """Create a form to set the new values of the BoB binning parameters"""
        self.formGroupBox = QGroupBox("Edit BoB Binning Settings")
        layout = QFormLayout()
        
        val_double = QDoubleValidator()
        val_double.setBottom(1) #set smalled double allowed in the form
        val_int = QIntValidator()
        val_int.setBottom(0) #set smalled int allowed in the form
        val_int.setTop(rch.pb_global_const.maxbobbins) #set smalled int allowed in the form
        
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


###########################



class IncreaseRecordsDialog(QDialog):
    """
    Dialog containing radio buttons to choose a new memory size for the records of "name" 
    """
    def __init__(self, parent_theory, current_max, name, size_of):
        super().__init__()
        self.createExclusiveGroup(current_max, name, size_of)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle("Edit")

    def createExclusiveGroup(self, current_max, name, size_of):
        """Create the radio buttons choices"""
        self.formGroupBox = QGroupBox("Increase the number of %s records?"%name)
        self.r1 = QRadioButton("%.4g (1.5x) requests %dMB of RAM"%(np.ceil(1.5*current_max), size_of*np.ceil(0.5*current_max)))
        self.r2 = QRadioButton("%.4g (2x) requests %dMB of RAM"%(2*current_max, size_of*current_max))
        self.r3 = QRadioButton("%.4g (5x) requests %dMB of RAM"%(5*current_max, size_of*current_max*4))
        self.r1.setChecked(True)
        
        layout = QVBoxLayout()     
        layout.addWidget(QLabel("Current number of %s records: %.4g.\nIncrease to:"%(name, current_max)))
        layout.addWidget(self.r1)
        layout.addWidget(self.r2)
        layout.addWidget(self.r3)
        layout.addWidget(QLabel("(%dMB of RAM available)"%(psutil.virtual_memory()[1]/2.**20))) # size of free RAM avaliable
        layout.addWidget(QLabel("Or press Cancel."))
        self.formGroupBox.setLayout(layout)
