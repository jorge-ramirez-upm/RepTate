import numpy as np
from scipy import interp
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
        self.parameters["rho0"]=Parameter("rho0", 0.95, "Density of polymer at 0 °C", ParameterType.real, False)
        self.parameters["C3"]=Parameter("C3", 0.69, "Density parameter TODO: Meaning of this?", ParameterType.real, False)
        self.parameters["T0"]=Parameter("T0", -50, "Temperature to shift WLF to, in °C", ParameterType.real, False)
        self.parameters["CTg"]=Parameter("CTg", 13, "Molecular weight dependence of Tg", ParameterType.real, False)
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
            xth.append(xthi)
            yth.append(ythi)
            Mw.append(Mwi)
            
            xmin[i,:]=np.amin(xthi,0)
            xmax[i,:]=np.amax(xthi,0)

        for i in range(nfiles):
            for j in range(i+1,nfiles):
                if (Mw[i] != Mw[j]): continue
                for k in range(view.n):
                    condition=(xth[j][:,k]>xmin[i,k])*(xth[j][:,k]<xmax[i,k])
                    x = np.extract(condition, xth[j][:,k])
                    y = np.extract(condition, yth[j][:,k])
                    yinterp=interp(x, xth[i][:,k], yth[i][:,k])
                    error=np.sum((yinterp-y)**2)
                    total_error+=error
                    npoints+=len(y)
                    file_error[i]+=error/2
                    file_error[j]+=error/2
                    file_points[i]+=len(y)/2
                    file_points[j]+=len(y)/2

        for i in range(nfiles):
            f=self.parent_dataset.files[i]
            print("%20s\t%10.5g"%(f.file_name_short,file_error[i]/file_points[i]))
        print("%20s\t%10.5g"%("TOTAL",total_error/npoints))
                
                
                

        #for f in self.parent_dataset.files:
        #    xexp, yexp, success = view.view_proc(f.data_table, f.file_parameters)
        #    xth, yth, success = view.view_proc(self.tables[f.file_name_short], f.file_parameters)
        #    if (self.xrange.get_visible()):
        #        conditionx=(xexp>self.xmin)*(xexp<self.xmax)
        #    else:
        #        conditionx=np.ones_like(xexp, dtype=np.bool)
        #    if (self.yrange.get_visible()):
        #        conditiony=(yexp>self.ymin)*(yexp<self.ymax)
        #    else:
        #        conditiony=np.ones_like(yexp, dtype=np.bool)
        #    yexp=np.extract(conditionx*conditiony, yexp)
        #    yth=np.extract(conditionx*conditiony, yth)
        #    f_error=np.mean((yth-yexp)**2)
        #    npt=len(yth)
        #    total_error+=f_error*npt
        #    npoints+=npt
        #    print("%20s\t%10.5g"%(f.file_name_short,f_error))
        #print("%20s\t%10.5g"%("TOTAL",total_error/npoints))
