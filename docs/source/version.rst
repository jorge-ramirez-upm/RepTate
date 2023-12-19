===============
Version History
===============

Release 1.3.1 - 20231219
========================
- Optimization with integer parameters (Pom-Pom)
- Expanded shear and uext file to contain gammadot and epsdot
- Some theories can handle time dependent flow rate
- Fit simultaneously Creep and Creep Recovery experiments of the same sample.
- Better import from Excel; Data imported from Excel can be fitted with theories
- Allow to save current DataSet
- Show several theories with different linestyles
- Changes to the code to make it compatible with modern versions of Python, Numpy and Matplotlib
- Removed CLI (Command Line Interface). 
- Removed high DPI option (automatically handled)
- Removed spinbox to increase/decrease number of views (giving problems)
- Removed mplcursors (data can be tracked by showing the Figure Toolbar)
- Changed PyQt5 --> PySide6. Solved the High DPI problem on Windows
- Removed bug that erased figures when switching tabs in multi plot view

Release 1.1.0 - 20200527
========================
- NEW DSM theory in the LVE App (thanks to J. Ethier & J. Schieber)
- NEW Tool Powerlaw
- NEW TTS Shift any data from the Materials Database tool
- NEW Basic Theory (Algebraic Expression). It can use file parameters
- NEW Stand-alone applications (Materials Database and Universal Viewer)
- NEW logging functionality
- Corrected small bugs, simplified code structure and documentation
- Open files, theories, tools and projects from the command line
- Created pypi package
- Some tools can now use file parameters
- Materials Database shows info about current files
- Added colors and simplified the command line notation
- Added better version control

Release 1.0.0 - 20200330
========================
- NEW Crystal application for flow induced crystallization
- NEW LAOS application for the analysis of large amplitude oscillatory shear data (based on MITlaos)
- NEW Sticky Reptation theory in the LVE module
- NEW ReSpect theory to extract the continuous and discrete relaxation spectra in the LVE and Gt Apps
- NEW GO-polySTRAND theory for flow induced nucleation in the Crystal App
- NEW Smooth-polySTRAND theory for flow induced nucleation in the Crystal App
- NEW theories Rolie-Poly, UCM, Giesekus and Pom-Pom in the LAOS App
- NEW Installation package for Windows with file associations
- NEW Global and local optimization methods

Release 0.9.7 - 20200117
========================
- NEW right-click to save chart
- New Windows installation package with association of common RepTate files
- New functionality for Materials Database (new/edit/duplicate materials)


Release 0.9.6 - 20191111
========================
- NEW axes and label setting options
- NEW Arrhenius theory in TTSFactor app
- NEW enable delete data points
- NEW: import excel files dialog
- Correction to Carreau-Yasuda theory

Release 0.9.5 - 20181205
========================
- New React theory "Diene CSTR"
- New Rolie-Double-Poly-LVE theory for polydisperse entangled linear polymers
- New BoB NLVE theory
- New NLVE theory: PETS model
- New NLVE theory: GLaMM
- Changed BoB so it doesn´t generate auxiliary files
- View all theories applied to current dataset simultaneously
- Added cursor to check data values with the mouse
- Corrections to bugs

Release 0.9.3 - 20180719
========================
- New App: to handle and fit TTS shift factors
- New Tools for manipulating how data is represented (draggable to set the order of application)
- New Tools: Integral, Find Peaks, Gradient, Smooth data, set bounds to data, Evaluate Expression, Interpolate/Extrapolate
- New Materials Database (implemented as a Tool); theory parameters are read from the database if the chemistry is available
- New View: i-Rheo for J(t), with oversampling
- Handling of citations
- Bayesian information criterion printed in theory output
- Save to Flowsolve button in RP and BlendRP theories
- Save Maxwell modes in all theories
- Copy/Paste parameters between theories
- Legend settings and autoupdate legend
- Better bug handling (send email to developers)
- Save all views data to a text file
- Shifting of files; handling and saving shift parameters
- Nicer HTML output in Theory and Tools
- Allow calculations and fits to be stopped
- Developer docs: Callback functions
- Zoom (right button and wheel; zoom in and zoom out) and Pan (middle button)
- Dummyfiles to check theory predictions without experimental data
- New NLVE test data
- Allow many plots in the same application

Release 0.9.2 - 20180503
========================
- Save theory predictions to a file
- Save/Load RepTate project
- New App: Dielectric spectroscopy
- New Dielectric Theories: Debye and Havriliak-Negami relaxation modes
- New Dielectric Theories: Kolhrauch-Williams-Watts (KWW) modes (BETA VERSION)
- Select xrange for iRheo G(t) view transformation
- alternate filled/empty symbols for views with n>1
- Read data from Excel file (only in CL version, LVE app)
- Zoom plot with mouse wheel (does not work if multiview > 1)
- Added all LVE views to TTS.
- LVE app can open osc files.
- Added missing views from old RepTate
- i-Rheo is the default view for panel 2 (Gt)
- Calculate integrals and find peaks of data (Experimental, only in CL version)
- "get modes" for Blend RP theory

Release 0.9.1 - 20180416
========================
- New MWD Theories: Generalized Exponential (GEX) & LogNormal distributions
- New Gt View: i-Rheo transformation with tunable oversampling

Release 0.9 - 20180327
======================
- New App: SANS for Neutran Scattering experiments
- New App: Creep
- New TTS Theory: WLF with temperature independent parameters
- New LVE Theory: Branch-on-Branch linear rheology from polyconf file
- New LVE and Gt Theories: dynamic dilution of star polymers in freq and time domain
- New LVE and Gt Theories: Rouse model in freq and time domain
- New NLVE Theory: Blend of Rolie-Poly equations for polydisperse melts
- New NLVE Theory: Pom-pom model
- New NLVE Theory: Giesekus constitutive equation
- New NLVE Theory: Upper-Convected Maxwell constitutive equation
- New Creep Theory: Retardation Modes
- New SANS Theory: Debye function for neutron scattering of ideal polymer chains
- New React Theory: generate polymer configuration with BoB
- New View i-Rheo in Application Gt
- Double click on theory parameter to change its attributes
- Auto fit when dragging x/y-limits 
- Select format of theory lines
- New basic theories (exponential, polynomial, etc), available to all Apps

Release 0.8 - 20180215
======================
- New App: React
- New Gt View: Schwarzl tranform
- New LVE View: all views from old RepTate
- New NLVE File type: elong for startup of extensional flow
- New React theory: Tobita Batch 
- New React theory: Tobita CSTR
- New React theory: MultiMetallocen
- New React theory: Mixture
- New LVE theory: Carreau-Yasuda equation
- New NLVE theory: Rolie-Poly with finite extensibility
- New color palettes
- Fixed bug: add file when theory exists
- Fixed small bugs in MWD theory
- Fixed bug: ticking files to visible shows the old view
- Views sorted
- Delete datafile with Supr
- Theory applies to active files only
- New automatic TTS shift
- Can use parallel threads for calculation and minimization
- Save BoB configuration to file
- Improved output from TTS theories
- Added Multiplots capability
- Double-click on file allows to view/edit file parameters
- Copy chart to clipboard
- Right-click on a series allows to copy/save the data
- Open files when passed as command line arguments
- New button to prevent autoscale
- Added buttons to read online documentation
- MW Discr theory with draggable modes

Release 0.7.1 - 20171209
========================
- New App: Gt
- Shift Maxwell modes by hand
- Interpolate Maxwell modes when the number of modes is changed
- Symbol settings dialog
- Basic handling of units
- Redesign the theory tab widget
- Zooming with mouse wheel (only in CL version)
- Button to add annotations to the plot (beta)
- Button for xy range selection for fit
- Copy data from inspector to clipboard
- View/move Maxwell modes in plot
- New icons from icons8
- View LVE envelope in RoliePoly
- Added stretching modes to RoliePoly


Release 0.5 - 20171105
======================
- New GUI with same functionality as the command line
- New App: MWD
- New MWD theory: MW Discretize
- Fixed Bug: view all when changing tab
- Copy Maxwell modes from other App
- Use parameter bounds in fitting
- Drag and drop files to the RepTate window
- Double-click on tabs to change name
- Button to Reload data
- Highlight currently selected file
- Data inspector shows file raw data 
- Draggable lines

Release 0.1 - 20161209
========================
- Basic structure of RepTate
- Basic command line application
- New App: TTS
- New App: LVE
- New App: NLVE
- New LVE Theory: Maxwell modes fitting
- New LVE theory: Likhtman-McLeish
- New NLVE theory: Rolie-Poly
- Run in batch mode
- Basic Read the docs documentation