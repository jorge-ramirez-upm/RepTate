===============
Version History
===============

Release 0.9.2 - 20180503
========================
- New App: Dielectric spectroscopy
- New Dielectric Theories: Debye and Havriliak-Negami relaxation modes
- New Dielectric Theories: Kolhrauch-Williams-Watts (KWW) modes (BETA VERSION)
- Select xrange for iRheo G(t) view transformation
- alternate filled/empty symbols for views with n>1
- Read data from Excel file (only in CL version, LVE app)
- Zoom plot with mouse wheel (does not work if multiview > 1)
- Added all LVE views to TTS.
- LVE app can open osc files.
- Added missing views from old Reptate
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