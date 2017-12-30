# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module TheoryTTS_Automatic

Module for the pseudo theory for Time-Temperature superposition shift of LVE data.

""" 
import os
import time
import getpass
import numpy as np
from scipy import interp
from scipy.optimize import minimize
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from PyQt5.QtWidgets import QWidget, QToolBar, QAction, QStyle, QFileDialog, QComboBox
from PyQt5.QtCore import QSize

class TheoryTTSShiftAutomatic(CmdBase):
    """Basic theory for Time-Temperature Superposition, based on the WLF equation
    
    [description]
    """
    thname="TTSShiftAutomatic"
    description="Basic theory for Time-Temperature Superposition, based on the WLF equation"
    cite=""

    def __new__(cls, name="ThWLFShifTest", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThTTSShiftAutomatic"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUITheoryTTSShiftAutomatic(name, parent_dataset, ax) if (CmdBase.mode==CmdMode.GUI) else CLTheoryTTSShiftAutomatic(name, parent_dataset, ax)

class BaseTheoryTTSShiftAutomatic:
    """[summary]
    
    [description]
    """
    single_file = False 

    def __init__(self, name="ThTTSShiftAutomatic", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThTTSShiftAutomatic"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        self.function = self.TheoryTTSShiftAutomatic
        
        self.parameters["T"]=Parameter(name="T", value=25, description="Temperature to shift to, in °C", type=ParameterType.real, opt_type=OptType.const, display_flag=False)
        self.parameters["vert"]=Parameter(name="vert", value=True, description="Shift vertically", type=ParameterType.boolean, 
                                          opt_type=OptType.const, display_flag=False)    
        self.Mwset, self.Mw, self.Tdict = self.get_cases()
        self.current_master_curve=None
        self.current_table=None
        self.current_file_min=None
        self.shiftParameters = {}
        for k in self.tables.keys():
            self.shiftParameters[k] = (0.0,0.0) # log10 of horizontal, then vertical

    def TheoryTTSShiftAutomatic(self, f=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            f {[type]} -- [description] (default: {None})
        """
        ft=f.data_table
        tt=self.tables[f.file_name_short]
        tt.num_columns=ft.num_columns
        tt.num_rows=ft.num_rows
        tt.data=np.zeros((tt.num_rows, tt.num_columns))

        H, V = self.shiftParameters[f.file_name_short]
        tt.data[:,0] = ft.data[:,0]*np.power(10.0, H)
        tt.data[:,1] = ft.data[:,1]*np.power(10.0, V)
        tt.data[:,2] = ft.data[:,2]*np.power(10.0, V)
                   
    def get_cases(self):
        """Get all different samples in the dataset
        
           Samples are different if Mw, Mw2, phi, phi2 are different
        """
        nfiles=len(self.parent_dataset.files)
        Mw=[]
        Tlist=[]

        for i in range(nfiles):
            Filei=self.parent_dataset.files[i]
            Mwi=Filei.file_parameters["Mw"]
            if "Mw2" in Filei.file_parameters:
                Mw2i=Filei.file_parameters["Mw2"]
            else:
                Mw2i=0
            if "phi" in Filei.file_parameters:
                phii=Filei.file_parameters["phi"]
            else:
                phii=0
            if "phi2" in Filei.file_parameters:
                phi2i=Filei.file_parameters["phi2"]
            else:
                phi2i=0
            Ti = Filei.file_parameters["T"]
            Mw.append((Mwi,Mw2i,phii,phi2i))
            Tlist.append(Ti)
            
        p = list(set(Mw))
        Tdict={}
        for c in p:
            Tdict[c]=[]
        for i in range(nfiles):
            Filei=self.parent_dataset.files[i]
            Tdict[Mw[i]].append([Tlist[i], i, Filei.file_name_short])
        return p, Mw, Tdict
    
        
    def do_error(self, line):
        """Override the error calculation for TTS
        
        The error is calculated as the vertical distance between theory points, in the current view,\
        calculated over all possible pairs of theory tables, when the theories overlap in the horizontal direction and\
        they correspond to files with the same Mw (if the parameters Mw2 and phi exist, their values are also
        used to classify the error). 1/2 of the error is added to each file.
        Report the error of the current theory on all the files.\n\
        File error is calculated as the mean square of the residual, averaged over all calculated points in the shifted tables.\n\
        Total error is the mean square of the residual, averaged over all points considered in all files.
        
        Arguments:
            line {[type]} -- [description]
        """
        total_error=0
        npoints=0
        view = self.parent_dataset.parent_application.current_view
        nfiles=len(self.parent_dataset.files)
        file_error=np.zeros(nfiles)
        file_points=np.zeros(nfiles,dtype=np.int)
        xth=[]
        yth=[]
        xmin=np.zeros((nfiles,view.n))
        xmax=np.zeros((nfiles,view.n))
        for i in range(nfiles):
            Filei=self.parent_dataset.files[i]
            xthi, ythi, success = view.view_proc(self.tables[Filei.file_name_short], Filei.file_parameters)
            # We need to sort arrays
            for k in range(view.n):
                x = xthi[:,k]
                p = x.argsort()
                xthi[:,k] = xthi[p,k]
                ythi[:,k] = ythi[p,k]
            xth.append(xthi)
            yth.append(ythi)
            
            xmin[i,:]=np.amin(xthi,0)
            xmax[i,:]=np.amax(xthi,0)
      
        #Mwset, Mw, Tdict = self.get_cases()
        MwUnique={}
        for o in self.Mwset:
            MwUnique[o]=[0.0, 0]
            
        for i in range(nfiles):
            for j in range(i+1,nfiles):
                if (self.Mw[i] != self.Mw[j]): continue
                for k in range(view.n):
                    condition=(xth[j][:,k]>xmin[i,k])*(xth[j][:,k]<xmax[i,k])
                    x = np.extract(condition, xth[j][:,k])
                    y = np.extract(condition, yth[j][:,k])
                    yinterp=interp(x, xth[i][:,k], yth[i][:,k])
                    error=np.sum((yinterp-y)**2)
                    npt=len(y)
                    total_error+=error
                    npoints+=npt
                    MwUnique[self.Mw[i]][0]+=error
                    MwUnique[self.Mw[i]][1]+=npt
        
        if (line==""): 
            self.Qprint("%5s %5s %5s %5s %10s (%10s)"%("Mw","Mw2","phi","phi2","Error","# Points"))
            self.Qprint("=====================")
            p = list(MwUnique.keys())
            p.sort()
            for o in p:
                if (MwUnique[o][1]>0):
                    self.Qprint("%5gk %5gk %5g %5g %10.5g (%10d)"%(o[0], o[1], o[2], o[3],MwUnique[o][0]/MwUnique[o][1],MwUnique[o][1]))
                else:
                    self.Qprint("%5gk %5gk %5g %5g %10s (%10d)"%(o[0], o[1], o[2], o[3],"-",0))
        if (npoints>0):
            total_error/=npoints
        else:
            total_error=1e10;
        if (line==""): self.Qprint("%21s %10.5g (%10d)"%("TOTAL",total_error,npoints))
        return total_error
                
    def func_fitTTS(self, *param_in):
        """[summary]
        
        [description]
        
        Arguments:
            *param_in {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        ind=0
        for p in self.parameters.keys():
            par = self.parameters[p] 
            if par.opt_type == OptType.opt:
                par.value=param_in[0][ind]
                ind+=1
        self.do_calculate("")
        error=self.do_error("none")
        return error

    def func_fitTTS_one(self, *param_in):
        """[summary]
        
        [description]
        
        Arguments:
            *param_in {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        H = param_in[0][0]
        V = 0
        if self.parameters["vert"].value:
            V = param_in[0][1]
        tt = np.array(self.current_table, copy=True)
        tt[:,0] = tt[:,0]*np.power(10.0, H)
        tt[:,1] = tt[:,1]*np.power(10.0, V)
        tt[:,2] = tt[:,2]*np.power(10.0, V)
        xmin=self.current_master_curve[0,0]
        xmax=self.current_master_curve[-1,0]
        condition=(tt[:,0]>xmin)*(tt[:,0]<xmax)
        x0 = np.extract(condition, tt[:,0])
        x1 = np.extract(condition, tt[:,1])
        x2 = np.extract(condition, tt[:,2])
        tt = np.array([x0,x1,x2])
        tt = np.transpose(tt)
        
        yinterp1=interp(tt[:,0], self.current_master_curve[:,0], self.current_master_curve[:,1])
        #print(H)
        #print(tt[:,1]-yinterp1)
        yinterp2=interp(tt[:,0], self.current_master_curve[:,0], self.current_master_curve[:,2])
        error=np.sum((yinterp1-tt[:,1])**2)+np.sum((yinterp2-tt[:,2])**2)
        #error=np.sum((yinterp1-tt[:,1])**2)
        npt=len(yinterp1)*2
        #npt=len(yinterp1)
        #print(H, V, error/npt)
        #input("HELLO")
        return error/npt

    def do_fit(self, line):
        """Minimize the error
        
        [description]
        
        Arguments:
            line {[type]} -- [description]
        """
        self.fitting = True
        #view = self.parent_dataset.parent_application.current_view

        # Case by case, T by T, we optimize the overlap of all files with the 
        # corresponding cases at the selected temperature
        Tdesired = self.parameters["T"].value
        #print (self.Tdict)
        for case in self.Tdict.keys():
            self.Qprint('Mw=%g Mw2=%g phi=%g phi2=%g'%(case[0], case[1], case[2], case[3]))
            self.Qprint('===========================')
            Temps0=[x[0] for x in self.Tdict[case]]
            Temps=np.abs(np.array([x[0] for x in self.Tdict[case]])-Tdesired)
            Files=[x[2] for x in self.Tdict[case]]
            indices = np.argsort(Temps)
            #print(case, indices, Temps, Files)
            # first master curve is built from first file in indices list
            fname = Files[indices[0]]
            self.current_master_curve = self.tables[fname].data
            self.current_master_curve.view('i8,i8,i8').sort(order=['f1'], axis=0)
            self.shiftParameters[fname] = (0.0, 0.0)
            #print(self.current_master_curve) #DEBUG
            #print(Temps0[indices[0]], 0.0, 0.0)
            self.Qprint('%15s %15s %15s'%('T','log(Hshift)','log(Vshift)'))
            self.Qprint('%15.3g %15.3g %15.3g'%(Temps0[indices[0]], 0.0, 0.0))
            indices=np.delete(indices,0,None)

            for i in indices:
                XSHIFT = 0.0
                YSHIFT = 0.0
                if (Temps[i]==0):
                    # Add to current_master_curve
                    fname = Files[i]
                    tt = self.tables[fname].data
                    self.current_master_curve = np.concatenate((self.current_master_curve,tt),axis=0)
                    self.current_master_curve=self.current_master_curve[self.current_master_curve[:,0].argsort()]
                    self.shiftParameters[fname] = (XSHIFT, YSHIFT)

                else:
                    fname = Files[i]
                    tt = self.tables[fname].data
                    # Calculate preliminary shift factors (horizontal and vertical)
                    # Calculate mid-point of tt
                    #print(tt)
                    #print(len(tt[:,0]))
                    indmiddle = int(len(tt[:,0])/2)
                    #print(indmiddle, tt[indmiddle,:])
                    xmid = tt[indmiddle,0]
                    ymid = tt[indmiddle,1]
                    xmidinterp=interp(ymid, self.current_master_curve[:,1], self.current_master_curve[:,0])
                    xshift=np.log10(xmidinterp/xmid)
                    #print(xmid, ymid, xmidinterp, xshift)
                    # minimize shift factors so the overlap is maximum
                    initial_guess=[xshift]
                    if self.parameters["vert"].value:
                        initial_guess.append(0)
                    self.current_table=tt
                    self.current_file_min=fname    
                    #print(initial_guess)
                    res = minimize(self.func_fitTTS_one, initial_guess, method='Nelder-Mead')
                    if (not res['success']):
                        self.Qprint("Solution not found: ", res['message'])
                        return
                    XSHIFT=res.x[0]
                    if self.parameters["vert"].value:
                        YSHIFT=res.x[1]
                    else:
                        YSHIFT=0.0
                    #print(res.x)
                    # Add to current_master_curve
                    # Set the theory file for that particular file                    
                    ttcopy =np.array(tt, copy=True)
                    ttcopy[:,0] = ttcopy[:,0]*np.power(10.0, XSHIFT)
                    ttcopy[:,1] = ttcopy[:,1]*np.power(10.0, YSHIFT)
                    ttcopy[:,2] = ttcopy[:,2]*np.power(10.0, YSHIFT)
                    self.current_master_curve = np.concatenate((self.current_master_curve,ttcopy),axis=0)
                    self.current_master_curve=self.current_master_curve[self.current_master_curve[:,0].argsort()]
                    #self.shiftParameters[fname] = (xshift, 0)
                    self.shiftParameters[fname] = (XSHIFT, YSHIFT)

                #print(Temps0[i], XSHIFT, YSHIFT)
                self.Qprint('%15.3g %15.3g %15.3g'%(Temps0[i], XSHIFT, YSHIFT))

        self.fitting=False
        self.do_calculate(line)

    def do_print(self, line):
        """Print the theory table associated with the given file name
        
        [description]
        
        Arguments:
            line {[type]} -- [description]
        """
        if line in self.tables:
            print(self.tables[line].data)
        else:
            print("Theory table for \"%s\" not found"%line)

    def complete_print(self, text, line, begidx, endidx):
        """[summary]
        
        [description]
        
        Arguments:
            text {[type]} -- [description]
            line {[type]} -- [description]
            begidx {[type]} -- [description]
            endidx {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        file_names=list(self.tables.keys())
        if not text:
            completions = file_names[:]
        else:
            completions = [ f
                            for f in file_names
                            if f.startswith(text)
                            ]
        return completions
        
    def do_save(self, line):
        """Save the results from TTSShiftAutomatic theory predictions to a TTS file
        
        [description]
        
        Arguments:
            line {[type]} -- [description]
        """
        print('Saving prediction of '+self.thname+' theory')
        nfiles=len(self.parent_dataset.files)
        MwUnique = list(set(self.Mw))
        MwUnique.sort()

        for m in MwUnique:
            data=np.zeros(0)
            fparam={}
            for i in range(nfiles):
                if (self.Mw[i] == m): 
                    Filei=self.parent_dataset.files[i]
                    ttable=self.tables[Filei.file_name_short]
                    data = np.append(data, ttable.data)
                    data=np.reshape(data, (-1, ttable.num_columns))
                    fparam.update(Filei.file_parameters)
            data=data[data[:, 0].argsort()]
            fparam["T"]=self.parameters["T"].value

            if line=="":
                ofilename=os.path.dirname(self.parent_dataset.files[0].file_full_path)+os.sep+fparam["chem"]+'_Mw'+str(m[0])+'k'+'_Mw2'+str(m[1])+'_phi'+str(m[2])+'_phiB'+str(m[3])+str(fparam["T"])+'.tts'
            else:
                ofilename=line+os.sep+fparam["chem"]+'_Mw'+str(m[0])+'k'+'_Mw2'+str(m[1])+'_phi'+str(m[2])+'_phiB'+str(m[3])+str(fparam["T"])+'.tts'            
            print('File: '+ofilename)
            fout=open(ofilename, 'w')
            for i in sorted(fparam):
                fout.write(i + "=" + str(fparam[i])+ ";")
            k = list(self.parameters.keys())
            k.sort()
            for i in k:
                fout.write(i + '=' + str(self.parameters[i].value) + ';')
            fout.write('\n')
            fout.write('# Master curve predicted with WLF Theory\n')
            fout.write('# Date: '+ time.strftime("%Y-%m-%d %H:%M:%S") + ' - User: ' + getpass.getuser() + '\n')
            k = Filei.file_type.col_names
            for i in k: 
                fout.write(i+'\t')
            fout.write('\n')
            for i in range(data.shape[0]):
                for j in range(data.shape[1]):
                    fout.write(str(data[i, j])+'\t')
                fout.write('\n')
            fout.close()

class CLTheoryTTSShiftAutomatic(BaseTheoryTTSShiftAutomatic, Theory):
    """[summary]
    
    [description]
    """
    def __init__(self, name="ThTTSShiftAutomatic", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThTTSShiftAutomatic"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        
class GUITheoryTTSShiftAutomatic(BaseTheoryTTSShiftAutomatic, QTheory):
    """[summary]
    
    [description]
    """
    def __init__(self, name="ThTTSShiftAutomatic", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThTTSShiftAutomatic"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)

        # add widgets specific to the theory
        tb = QToolBar()
        tb.setIconSize(QSize(24,24))
        self.verticalshift = tb.addAction(self.style().standardIcon(getattr(QStyle, 'SP_ArrowUp')), 'Vertical shift')
        self.verticalshift.setCheckable(True)
        self.verticalshift.setChecked(True)
        self.savemaster = tb.addAction(self.style().standardIcon(getattr(QStyle, 'SP_DialogSaveButton')), 'Save Master Curve')
        self.cbTemp = QComboBox()
        self.populate_TempComboBox()
        self.cbTemp.setToolTip("Select a goal Temperature")
        tb.addWidget(self.cbTemp)
        self.refreshT = tb.addAction(self.style().standardIcon(getattr(QStyle, 'SP_BrowserReload')), 'Refresh T list')

        self.thToolsLayout.insertWidget(0, tb)
        connection_id = self.verticalshift.triggered.connect(self.do_vertical_shift)
        connection_id = self.savemaster.triggered.connect(self.do_save_dialog)
        connection_id = self.cbTemp.currentIndexChanged.connect(self.change_temperature)
        connection_id = self.refreshT.triggered.connect(self.refresh_temperatures)

    def populate_TempComboBox(self):
        k = list(self.Tdict.keys())
        a = sorted(list(set([x[0] for x in self.Tdict[k[0]]])))
        for i in range (1,len(k)):
            b = sorted([x[0] for x in self.Tdict[k[i]]])
            a = sorted(list(set(a) & set(b)))
        self.cbTemp.clear()
        for t in a:
            self.cbTemp.addItem(str(t))
        self.set_param_value("T", float(self.cbTemp.currentText()))
        self.update_parameter_table()

    def do_vertical_shift(self):
        self.set_param_value("vert", self.verticalshift.isChecked())

    def do_save_dialog(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory to save Master curves"))
        self.do_save(folder)

    def change_temperature(self):
        try:
            self.set_param_value("T", float(self.cbTemp.currentText()))
            self.update_parameter_table()
        except:
            pass

    def refresh_temperatures(self):
        self.Mwset, self.Mw, self.Tdict = self.get_cases()
        self.populate_TempComboBox()
