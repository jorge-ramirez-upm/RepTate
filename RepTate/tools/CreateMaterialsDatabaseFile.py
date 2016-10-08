import numpy as np
from polymer_data import polymer

polymerdict={}        
polymerdict['PEP'] = polymer(C1=6.0767, C2=125.96, Rho0=0.95, C3=2.5721, T0=25, CTg=0, short='PEP',long='Polyethylene-propylene',chem='',M0=0,tau_e=3.9636E-6, Ge=1.5503E6, Me=1.4306, c_nu=0.1, author='Alexei Likhtman', date='17/03/2006', description='Recommended')
polymerdict['PS'] = polymer(C1=5.5354, C2=-52.237, Rho0=0.95, C3=0.69, T0=170, CTg=0, short='PS',long='Polystyrene',chem='C8H8',M0=104, tau_e=0.0010423, Ge=3.0555E5, Me=16.518, c_nu=0.1, author='Alexei Likhtman', date='17/03/2006', description='Recommended')
polymerdict['PI'] = polymer(C1=4.9864, C2=114.03, Rho0=0.928, C3=0.61, T0=25, CTg=14.65, short='PI',long='Polyisoprene',chem='C5H8',M0=68,tau_e=1.3213E-5, Ge=5.9535E5, Me=4.8158, c_nu=0.1, author='Alexei Likhtman', date='17/03/2006', description='Recommended')
polymerdict['PBd'] = polymer(C1=3.6301, C2=142.11, Rho0=0.95, C3=0.69, T0=25, CTg=13.0, short='PBd',long='Polybutadiene',chem='CH2CH=CHCH2',M0=54,tau_e=3.3965E-7, Ge=1.6154E6, Me=1.8136, c_nu=0.1, author='Alexei Likhtman', date='17/03/2006', description='Recommended')
polymerdict['hPBd'] = polymer(C1=1.8, C2=70, Rho0=0.95, C3=0.69, T0=170, CTg=0.01, short='hPBd',long='Hydrogenated Polybutadiene',chem='CH2CH2-CH2CH2',M0=56,tau_e=1.1885E-8, Ge=2.81E6, Me=1.26, c_nu=1, author='Richard Graham', date='21/06/2006', description='Parameters for linear hydrogentated polybutadiene')

np.save('materials_database.npy', polymerdict) 


