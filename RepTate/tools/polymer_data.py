class polymer:
    def __init__ (self, **kwargs):
        self.data = {
            'short'       : '',     # Short name
            'long'        : '',     # Full name
            'chem'        : '',     # Short hand Chemistry
            'M0'          : 0,      # Monomer molecular weight
            'description' : '',     # Description of parameters
            'author'      : '',     # Who added/Modified the parameters
            'date'        : '',     # Date of parameter modification
            # Likhtman-McLeish parameters
            'tau_e'       : 0,      # Rouse time of one entanglement
            'Ge'          : 0,      # Entanglement modulus
            'Me'          : 0,      # Entanglemnet molecular while
            'c_nu'        : 0,      # Constraint release parameter
            # WLF Parameters
            'C1'          : 0,      # Material parameter C1 for WLF Shift
            'C2'          : 0,      # Material parameter C2 for WLF Shift
            'Rho0'        : 0,      # Density of polymer at 0 °C
            'C3'          : 0,      # Density parameter TODO: Meaning of this?
            'T0'          : 0,      # Reference temperature?
            'CTg'         : 0,      # Molecular weight dependence of Tg
        }
        
        self.data.update(kwargs)
