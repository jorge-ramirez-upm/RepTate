import numpy as np
from scipy import interp
from scipy.optimize import minimize
from Theory import *

class TheoryWLFShift(Theory, CmdBase):
    """Basic theory for Time-Temperature Superposition, based on the WLF equation"""
    thname="WLFShift"
    description="Basic theory for Time-Temperature Superposition, based on the WLF equation"
    cite="TODO: Cite Dietmar Auhl paper?"

    def __init__(self, name="ThWLFShift", parent_dataset=None, ax=None):
        super(TheoryWLFShift, self).__init__(name, parent_dataset, ax)
        self.function = self.TheoryWLFShift
        self.parameters["C1"]=Parameter("C1", 6.85, "Material parameter C1 for WLF Shift", ParameterType.real, True)
        self.parameters["C2"]=Parameter("C2", 150, "Material parameter C2 for WLF Shift", ParameterType.real, True)
        self.parameters["rho0"]=Parameter("rho0", 0.928, "Density of polymer at 0 °C", ParameterType.real, False)
        self.parameters["C3"]=Parameter("C3", 0.61, "Density parameter TODO: Meaning of this?", ParameterType.real, False)
        self.parameters["T0"]=Parameter("T0", 25, "Temperature to shift WLF to, in °C", ParameterType.real, False)
        self.parameters["CTg"]=Parameter("CTg", 14.65, "Molecular weight dependence of Tg", ParameterType.real, False)
        self.parameters["dx12"]=Parameter("dx12", 0, "For PBd", ParameterType.real, False)

    def bT(self, T, T0, rho0, c3):
        return 

    def TheoryWLFShift(self, f=None):
        ft=f.data_table
        tt=self.tables[f.file_name_short]
        tt.num_columns=ft.num_columns
        tt.num_rows=ft.num_rows
        tt.data=np.zeros((tt.num_rows, tt.num_columns))

        T0=self.parameters["T0"].value
        C1=self.parameters["C1"].value
        C2=self.parameters["C2"].value
        C3=self.parameters["C3"].value
        rho0=self.parameters["rho0"].value
        CTg=self.parameters["CTg"].value
        dx12=self.parameters["dx12"].value

        T=f.file_parameters["T"]
        Mw=f.file_parameters["Mw"]

        C2 += CTg / Mw - 68.7 * dx12
        T0corrected = T0 - CTg / Mw + 68.7 * dx12
        tt.data[:,0] = ft.data[:,0]*np.power(10.0, -(T - T0corrected) * (C1 / (T + C2)))

        bT = (rho0 - T * C3 * 1E-3) * (T + 273.15) / ((rho0 - T0 * C3 * 1E-3) * (T0 + 273.15));
        tt.data[:,1] = ft.data[:,1] / bT;
        tt.data[:,2] = ft.data[:,2] / bT;

    def do_error(self, line):
        """Override the error calculation for TTS. \
The error is calculated as the vertical distance between theory points, in the current view,\
calculated over all possible pairs of theory tables, when the theories overlap in the horizontal direction and\
they correspond to files with the same Mw. 1/2 of the error is added to each file.
Report the error of the current theory on all the files.\n\
File error is calculated as the mean square of the residual, averaged over all calculated points in the shifted tables.\n\
Total error is the mean square of the residual, averaged over all points considered in all files.
        """
        total_error=0
        npoints=0
        view = self.parent_dataset.parent_application.current_view
        nfiles=len(self.parent_dataset.files)
        file_error=np.zeros(nfiles)
        file_points=np.zeros(nfiles,dtype=np.int)
        xth=[]
        yth=[]
        Mw=[]
        xmin=np.zeros((nfiles,view.n))
        xmax=np.zeros((nfiles,view.n))
        for i in range(nfiles):
            Filei=self.parent_dataset.files[i]
            Mwi=Filei.file_parameters["Mw"]
            xthi, ythi, success = view.view_proc(self.tables[Filei.file_name_short], Filei.file_parameters)
            # We need to sort arrays
            for k in range(view.n):
                x = xthi[:,k]
                p = x.argsort()
                xthi[:,k] = xthi[p,k]
                ythi[:,k] = ythi[p,k]
            xth.append(xthi)
            yth.append(ythi)
            Mw.append(Mwi)
            
            xmin[i,:]=np.amin(xthi,0)
            xmax[i,:]=np.amax(xthi,0)

        MwUnique={}
        p = list(set(Mw))
        for o in p:
            MwUnique[o]=[0.0, 0]

        for i in range(nfiles):
            for j in range(i+1,nfiles):
                if (Mw[i] != Mw[j]): continue
                for k in range(view.n):
                    condition=(xth[j][:,k]>xmin[i,k])*(xth[j][:,k]<xmax[i,k])
                    x = np.extract(condition, xth[j][:,k])
                    y = np.extract(condition, yth[j][:,k])
                    yinterp=interp(x, xth[i][:,k], yth[i][:,k])
                    error=np.sum((yinterp-y)**2)
                    npt=len(y)
                    total_error+=error
                    npoints+=npt
                    MwUnique[Mw[i]][0]+=error
                    MwUnique[Mw[i]][1]+=npt
        
        if (line==""): 
            print("%20s %10s (%10s)"%("Mw","Error","# Points"))
            print("=============================================")
            p = list(MwUnique.keys())
            p.sort()
            for o in p:
                if (MwUnique[o][1]>0):
                    print("%20.5gk %10.5g (%10d)"%(o,MwUnique[o][0]/MwUnique[o][1],MwUnique[o][1]))
                else:
                    print("%20.5gk %10s (%10d)"%(o,"-",0))
        if (npoints>0):
            total_error/=npoints
        else:
            total_error=1e10;
        if (line==""): print("%21s %10.5g (%10d)"%("TOTAL",total_error,npoints))
        return total_error
                
    def func_fitTTS(self, *param_in):
        ind=0
        for p in self.parameters.keys():
            par = self.parameters[p] 
            if par.min_flag:
                par.value=param_in[0][ind]
                ind+=1
        self.do_calculate("")
        error=self.do_error("none")
        return error

    def do_fit(self, line):
        """Minimize the error"""
        self.fitting = True
        view = self.parent_dataset.parent_application.current_view

        # Mount the vector of parameters (Active ones only)
        initial_guess=[]
        for p in self.parameters.keys():
            par = self.parameters[p] 
            if par.min_flag: 
                initial_guess.append(par.value)

        res = minimize(self.func_fitTTS, initial_guess, method='Nelder-Mead')
        
        if (not res['success']):
            print("Solution not found: ", res['message'])
            return

        print("Solution found with %d function evaluations and error %g"%(res['nfev'],res.fun))

        ind=0
        k=list(self.parameters.keys())
        k.sort()
        print("%10s   %10s"%("Parameter","Value"))
        print("===========================")
        for p in k:
            par = self.parameters[p] 
            if par.min_flag:
                ind+=1
                print('*%9s = %10.5g'%(par.name, par.value))
            else:
                print('%10s = %10.5g'%(par.name, par.value))
        self.fitting=False
        self.do_calculate(line)

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
        
    def do_save(self, line):
        """Save the results from WLFShift theory predictions to a TTS file"""
        print('Saving prediction of '+self.thname+' theory')
        Mw=[]
        for f in self.parent_dataset.files:
            Mwi=f.file_parameters["Mw"]
            Mw.append(Mwi)            
        MwUnique = list(set(Mw))
        MwUnique.sort()

        for m in MwUnique:
            data=np.zeros(0)
            fparam={}
            for f in self.parent_dataset.files:
                if (f.file_parameters["Mw"]==m):
                    ttable=self.tables[f.file_name_short]
                    data = np.append(data, ttable.data)
                    data=np.reshape(data, (-1, ttable.num_columns))
                    fparam.update(f.file_parameters)
            data=data[data[:, 0].argsort()]
            fparam["T"]=self.parameters["T0"].value

            ofilename=os.path.dirname(self.parent_dataset.files[0].file_full_path)+os.sep+fparam["chem"]+'_'+str(fparam["Mw"])+'k'+'_'+str(fparam["T"])+'.tts'
            print('File: '+ofilename)
            fout=open(ofilename, 'w')
            k = list(f.file_parameters.keys())
            k.sort()
            for i in k:            
                fout.write(i + "=" + str(f.file_parameters[i])+ ";")
            fout.write('\n')
            fout.write('# Master curve predicted with '+self.thname+' Theory\n')
            fout.write('# ')
            k = list(self.parameters.keys())
            k.sort()
            for i in k:
                fout.write(i + '=' + str(self.parameters[i].value) + '; ')
            fout.write('\n')
            fout.write('# Date: '+ time.strftime("%Y-%m-%d %H:%M:%S") + ' - User: ' + getpass.getuser() + '\n')
            k = f.file_type.col_names
            for i in k: 
                fout.write(i+'\t')
            fout.write('\n')
            for i in range(data.shape[0]):
                for j in range(data.shape[1]):
                    fout.write(str(data[i, j])+'\t')
                fout.write('\n')
            fout.close()
