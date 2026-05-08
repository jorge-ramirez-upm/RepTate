/** \mainpage Linear rheology of linear polydisperse polymers
  * \tableofcontents
&nbsp; &nbsp; &nbsp; &nbsp; &copy; Chinmay Das and Daniel J. Read <br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 28/09/2022 <br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <a href="https://www.gnu.org/licenses/gpl-3.0.en.html"> GNU GPLv3 </a> (or at your option any later version) <br>

<HR> 
  * \section sec_intro Introduction 
The code in this depository accompanies our paper <A HREF="https://chinmaydaslds.github.io/LP2R/manuscript/Das_Read_LP2R.pdf"> <em>"A tube model for predicting the stress and dielectric
relaxations of polydisperse linear polymers"</em> </A> submitted to <em>Journal of Rheology</em> (2022). 
This implements modern ideas about how constraint release and tube escape modes in linear polymer melts affect each other
in a numerical code to predict linear respose in arbitrarily polydisperse linear polymers. The information about the
polymers can be supplied as moments of a distribution, or as data files containing gel permeation chromatography measurements (GPC), or a set of discrete molar masses and associated weight fractions. Arbitrarily complex blends can be designed by adding several such components. Besides the mechanical relaxation moduli, the code also can calculate dielectric
relaxation for type-A polymers (polymers with monomer dipole moments aligned along the chain backbone). With appropriate
instructions, the code outputs evolutions of model constructs like different dynamic tube diameters or how a specific 
molar mass chain will undergo the terminal relaxation. 

The code is available for download from <A HREF="https://github.com/chinmaydaslds/LP2R"> github</A>. On UNIX/Linux
systems, you can use <em> make</em> command from <em> LP2R/src/obj </em> subdirectory to create the executable. 
A precompiled windows executable is available from <A HREF="https://drive.google.com/file/d/1gO2Z3UWPi1zeLnvmpjs5II3OA2hJrPla/view?usp=sharing"> google drive</A>.  A snapshot of the code
at the time of submission of this paper including the submitted preprint is available 
at <A HREF="https://zenodo.org/record/7276482#.Y2OTKnbP1PZ"> zenodo. </A>

The rest of this page documents the command line options, input file syntax, and output file formats.

<div style="background: lavender; padding: 0px; border: 1px solid lightblue; margin: 1px;">
<SMALL>
Go to  <strong> <A HREF="sec_intro"> Table of Contents </A> </strong> <br>
&rArr; \ref sec_intro &nbsp; &nbsp;
&rArr; \ref sec_usage &nbsp; &nbsp;
&rArr; \ref sec_input &nbsp; 
&bull; <span style="color: #9096a3;"> <A HREF="sec_inp"> Material input file </A> &nbsp; </span> 
&bull; <span style="color: #9096a3;"> <A HREF="sec_rc"> Resource file </A> </span> &nbsp; &nbsp;
&rArr;  \ref sec_output  &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_gtp"> Relaxation spectra </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_gt"> Time relaxation </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_phi"> Tube diameters </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_pathway"> Relaxation pathways </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_pathway"> Relaxation pathways </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_log"> Log file </A> </span> &nbsp;
</SMALL>
</div>
\section sec_usage Usage
<CODE>
LP2R  [-L] [-d] [-i inputfile] [-r resourcefile] [-h] [-</CODE><CODE>-version]
</CODE>
<br/>

<h4><strong>Optional command line arguments:</strong></h4>

<ul>
<li><strong>-L</strong> : Output debugging and extra information in a file named <strong><em>LP2Rlog.txt<br /><br /></em></strong></li>
<li><strong>-i</strong> inputfile : material and output frequency information supplied via a named file. Default inputfile name is <em><strong>inp.dat<br /><br /></strong></em></li>
<li><strong>-r</strong> resourcefile : Presumably chemistry independent parameters, and output options can be set via a resource file. Default resourcefile name is <em><strong>LP2R.rc<br /><br /></strong></em></li>
<li><strong>-h</strong> : help (this usage information)<br /><br /></li>
<li><strong>- -version</strong> : version information</li>
</ul>
<p>&nbsp;</p>

<div style="background: lavender; padding: 0px; border: 1px solid lightblue; margin: 1px;">
<SMALL>
Go to  <strong> <A HREF="sec_intro"> Table of Contents </A> </strong> <br>
&rArr; \ref sec_intro &nbsp; &nbsp;
&rArr; \ref sec_usage &nbsp; &nbsp;
&rArr; \ref sec_input &nbsp; 
&bull; <span style="color: #9096a3;"> <A HREF="sec_inp"> Material input file </A> &nbsp; </span> 
&bull; <span style="color: #9096a3;"> <A HREF="sec_rc"> Resource file </A> </span> &nbsp; &nbsp;
&rArr;  \ref sec_output  &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_gtp"> Relaxation spectra </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_gt"> Time relaxation </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_phi"> Tube diameters </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_pathway"> Relaxation pathways </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_pathway"> Relaxation pathways </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_log"> Log file </A> </span> &nbsp;
</SMALL>
</div>

\section sec_input Input files
The code expects input to be supplied from plain text files. The percentage (%) character is  used
as a comment character in the files. If the first non-space character in a line is %, the entire line is
ignored. Similarly a % sign can be used beyond the intended input in the same line to add comments. The
files are read one line at a time - so, if multiple entries are supposed to be in the same line, a line break 
between entries will lead to input error. The input file itself may contain names of some other file containing
detailed molecular weight information. In such cases, names containing space or percentage sign will not be
processed correctly. Avoid names like <strong> "Molecular Weight.txt" </strong> or <strong> "PI100k(2%)_PI50k(98%).txt"</strong>: The first name will be truncated to <strong> <em> "Molecular" </em> </strong> and the second will be truncated
to <strong> <em> "PI100k(2" </em></strong> and the code will fail to find the intended data file.

Two different files are used for input: The first should supply the material parameters and the frequency range
over which relaxation spectra is desired. The default file name for this file is <strong> <em> inp.dat </em></strong>. A different file can be supplied with the command line option <strong> <em> -i filename </em></strong>. Details of the information required in this file are described in \ref sec_inp .

The second optional file supplies model parameters that are thought to be insensitive to the chemistry, and can be used
to choose the results that the code should generate. The default file name for this resource file is <strong> <em> LP2R.rc  </em></strong>. A different file can be supplied with the command line option <strong> <em> -r filename </em></strong>. Details of the information required in this file are described in \ref sec_rc . 


<div style="background: lavender;
  padding: 0px;
  border: 1px solid lightblue;
  margin: 1px;">
<SMALL>
Go to  <strong> <A HREF="sec_intro"> Table of Contents </A> </strong> <br>
&rArr; \ref sec_intro &nbsp; &nbsp;
&rArr; \ref sec_usage &nbsp; &nbsp;
&rArr; \ref sec_input &nbsp; 
&bull; <span style="color: #9096a3;"> <A HREF="sec_inp"> Material input file </A> &nbsp; </span> 
&bull; <span style="color: #9096a3;"> <A HREF="sec_rc"> Resource file </A> </span> &nbsp; &nbsp;
&rArr;  \ref sec_output  &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_gtp"> Relaxation spectra </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_gt"> Time relaxation </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_phi"> Tube diameters </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_pathway"> Relaxation pathways </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_pathway"> Relaxation pathways </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_log"> Log file </A> </span> &nbsp;
</SMALL>
</div>

\subsection sec_inp Material input file
The information about the polymers is supplied via a plain-text file called <strong> inp.dat </strong> 
(a different file can be used by using the command line option <strong> <em> -i filename </em> </strong>). 
The input
can be imagined as having three distinct parts: the
first part gives the frequency range and discretization for the relaxation spectra output, the second part inputs
the material parameters (chemistry dependent but architucture independent parameters), and finally the third part
inputs the information about the molar mass distribution(s) of the molecules of interest. 

The first valid line (the code will ignore comment lines or empty lines) needs the minimum angular frequency
(&omega;<sub>min</sub>), the maximum angular frequency (&omega;<sub>max</sub>) and the ratio of successive 
angular frequencies (&omega;<sub>ratio</sub>) for the desired relaxation spectra output. 

The second valid line
requires the Kuhn molar mass (M<sub>Kuhn</sub>) in g/mole, entanglement molar mass (M<sub>e</sub>) in g/mole, plateau modulus 
(G<sub>N</sub><sup>0</sup>) in Pa, and the entanglement time (&tau;<sub>e</sub>) in seconds. The third line gives the
glassy modulus (G<sub>&infin;</sub>) in Pa, glassy relaxation time (&tau;<sub>g</sub>) in seconds and the exponent for the 
stretched exponential glassy relaxation (&beta;<sub>g</sub>). 

The fourth line contains a single integer specifying the number of components (n<sub>comp</sub>) forming the blend. 
(In the special case of single component polymer, this number is one). A <em> component </em> is understood to be
a set of <em> molecules </em> having a easily described distribution. For each of these components, additional two input-lines are
given to characterize the components. The first of thse lines contain an integer parameter (p<sub>type</sub>) and 
the weight fraction of this component (w<sub>comp</sub>) in the blend. If <strong> p<sub>type</sub>=0</strong>, the component is 
assumed to be represented
by a log-normal distribution. The following line in that case needs number of discrete molar masses to be used to
represent the distribution (n<sub>poly</sub>), the weight-averaged molar mass (M<sub>W</sub>) in g/mole and the polydispersity
index (PDI). Instead if, <strong> p<sub>type</sub>=1</strong>, the molar mass distribution is assumed to exist as
a GPC measurement and the second line of component specification in that case gives the file name of the GPC data. 
The GPC file should have usual {M, dW/dlog<sub>10</sub>M } values with the molar mass in g/mole.
Finally, <strong> p<sub>type</sub>=2</strong>, assumes that the molar mass is specified by a set of weights associated
with discrete sets of molar mass. Again, the second line of component specification is a file name and the file
should contain two columns: molar mass in g/mole and the associated weights {M<sub>i</sub>, w<sub>i</sub> }. 


The following is an input file for 1,4-PI at 25&deg;C for a 1131000 g/mole polymer assumed to be described by
a log-normal distribution:<br>
<div style="background: ghostwhite;
  padding: 10px;
  border: 1px solid lightgray;
  margin: 10px;">
1.0e-4 1.0e6 1.2 &nbsp; &nbsp; % &nbsp; &nbsp; &omega;<sub>min</sub>, &omega;<sub>max</sub>, &omega;<sub>ratio</sub> <br>
113.0 4350.0 476000.0 1.30e-5 &nbsp; &nbsp; % &nbsp; &nbsp; M<sub>Kuhn</sub>, M<sub>e</sub>, G<sub>N</sub><sup>0</sup>, &tau;<sub>e</sub> <br>
1.0e9 7.0e-11 0.370 &nbsp; &nbsp; % &nbsp; &nbsp; G<sub>&infin;</sub>, &tau;<sub>g</sub>, &beta;<sub>g</sub> <br>
1 &nbsp; &nbsp;  % &nbsp; &nbsp; Single component: n<sub>comp</sub>=1 <br>
0 1.0 &nbsp; &nbsp;  % &nbsp; &nbsp; p<sub>type</sub>=0 (log-normal distribution), w<sub>comp</sub>=1 <br>
50 1131000 1.05  &nbsp; &nbsp;  % &nbsp; &nbsp; n<sub>poly</sub>=50, M<sub>W</sub>, PDI <br>
</div>

Blending 30-wt% 226kg/mole polymer would require an input file like the following<br>
<div style="background: ghostwhite;
  padding: 10px;
  border: 1px solid lightgray;
  margin: 10px;">
1.0e-4 1.0e6 1.2 &nbsp; &nbsp; % &nbsp; &nbsp; &omega;<sub>min</sub>, &omega;<sub>max</sub>, &omega;<sub>ratio</sub> <br>
113.0 4350.0 476000.0 1.30e-5 &nbsp; &nbsp; % &nbsp; &nbsp; M<sub>Kuhn</sub>, M<sub>e</sub>, G<sub>N</sub><sup>0</sup>, &tau;<sub>e</sub> <br>
1.0e9 7.0e-11 0.370 &nbsp; &nbsp; % &nbsp; &nbsp; G<sub>&infin;</sub>, &tau;<sub>g</sub>, &beta;<sub>g</sub> <br>
2 &nbsp; &nbsp;  % &nbsp; &nbsp; <strong> Two components :</strong> &nbsp; &nbsp;  n<sub>comp</sub>=2 <br>
0 0.70 &nbsp; &nbsp;  % &nbsp; &nbsp; <strong> <em> First component: </em> </strong>  &nbsp; &nbsp; p<sub>type</sub>=0 (log-normal distribution), w<sub>comp</sub>=0.70 <br>
50 1131000 1.05  &nbsp; &nbsp;  % &nbsp; &nbsp; n<sub>poly</sub>=50, M<sub>W</sub>, PDI <br>
0 0.30 &nbsp; &nbsp;  % &nbsp; &nbsp;  <strong> <em> Second component: </em> </strong> &nbsp; &nbsp; p<sub>type</sub>=0 (log-normal distribution), w<sub>comp</sub>=0.30 <br>
50 225900 1.03 &nbsp; &nbsp;  % &nbsp; &nbsp; n<sub>poly</sub>=50, M<sub>W</sub>, PDI <br>
</div>

Some more examples of input files can be found in the examples subdirectory in the code distribution.

<em> Some pointers about the input: </em> <br>

&bull;&nbsp; A strictly monodisperse polymer can be specified by choosing a log-normal distribution
(p<sub>type</sub>=0) and PDI=1, or n<sub>poly</sub>=1 in the specification of the distribution. <br>

&bull;&nbsp; If the glassy parameters are not be available for the chemistry of interest, a good starting
point may be G<sub>&infin;</sub>=1.0e9, &tau;<sub>g</sub>=1.0e5 &times; &tau;<sub>e</sub>, and
&beta;<sub>g</sub>=0.35.


<div style="background: lavender; padding: 0px; border: 1px solid lightblue; margin: 1px;">
<SMALL>
Go to  <strong> <A HREF="sec_intro"> Table of Contents </A> </strong> <br>
&rArr; \ref sec_intro &nbsp; &nbsp;
&rArr; \ref sec_usage &nbsp; &nbsp;
&rArr; \ref sec_input &nbsp; 
&bull; <span style="color: #9096a3;"> <A HREF="sec_inp"> Material input file </A> &nbsp; </span> 
&bull; <span style="color: #9096a3;"> <A HREF="sec_rc"> Resource file </A> </span> &nbsp; &nbsp;
&rArr;  \ref sec_output  &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_gtp"> Relaxation spectra </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_gt"> Time relaxation </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_phi"> Tube diameters </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_pathway"> Relaxation pathways </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_pathway"> Relaxation pathways </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_log"> Log file </A> </span> &nbsp;
</SMALL>
</div>
\subsection sec_rc Resource file
The code searches for a file named <strong> <em> LP2R.rc </em></strong> in the current directory to input 
additional parameters besides the material parameters. 
A different file can be specified with command line option <strong> <em> -r filename </em> </strong>. 
In the absence of this file, the code will continue with default parameters and options detailed below. Similarly
any entry in the file that is not understood by the code is silenty ignored. If you use 
the command line option <strong> <em> -L </em></strong> to generate a log file, such unresolved entries will be
written in the log file as warning messages. Each entry in the resource file is a property-value pair separated by
a equal (=) sign. Each line can contain only one such property-value pair. Unlike the material input file, the
ordering of the different entries in the file does not have any consequence. 

A sample file with all options set to default values is available in the examples/01rcdefault subdirectory.


<p> <span style="color: #ff0000;"><strong>% Model parameters</strong></span> </p>

<div style="background: ghostwhite;
  padding: 10px;
  border: 1px solid lightgray;
  margin: 10px;">
Alpha=1.0 &nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; Dilution exponent <span style="color: #0000ff;">&alpha;</span> <br>
t_CR_START=1.0 &nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; Constraint release starts after this time (in units of &tau;<sub>e</sub>) <br>
deltaCR=0.30 &nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; Fractional drop in &phi;<sub>ST</sub> for &tau;<sub>CR </sub>&raquo; &tau;<sub>e</sub> <span style="color: #0000ff;">(&delta;<sub>CR</sub><sup>&infin;</sup>)</span> <br>
B_zeta=2.0 &nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; Proportionality constant relating friction coefficient to supertube fraction <span style="color: #0000ff;">(B<sub>&zeta;</sub>)</span><br>
A_eq=2.0 &nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; Proportionality constant connecting "effective equilibrium time" and time to locally equiilbiate in a certain supertube <span style="color: #0000ff;">(A<sub>eq</sub>)</span> <br>
B_eq=10.0 &nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; Constant delaying equilibrium for fast CR events <span style="color: #0000ff;">(B<sub>eq</sub>)</span> <br>
ret_pref=0.189 &nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; Constant in arm retraction formula <span style="color: #0000ff;">(C<sub>a,&infin;</sub>)</span> <br>
ret_pref_0=0.020 &nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; Short-time prefactor for CLF&nbsp;<span style="color: #0000ff;">(C<sub>a,0</sub>)</span> <br>
ret_switch_exponent=0.42 &nbsp; &nbsp; &nbsp; % &nbsp; &nbsp;  Exponent&nbsp;<span style="color: #0000ff;">&epsilon;<sub>a </sub></span>determining how steeply CLF switches to long-time strength <br>
Rept_Switch_Factor=1.664 &nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; Constant deciding transition from CLF to reptation <span style="color: #0000ff;">(K<sub><em>R</em></sub>)</span> <br>
Rouse_Switch_Factor=1.5 &nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; Minimum number of bare entanglements to be considered entangled <span style="color: #0000ff;">(Z<sub>U</sub>)</span> <br>
Disentanglement_Switch=1.0 &nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; Number of surviving entanglements in the supertube below which chains relax by "disentanglement" <br>
</div>

<p> <span style="color: #ff0000;"><strong>% Time discretization</strong></span> </p>
<div style="background: ghostwhite;
  padding: 10px;
  border: 1px solid lightgray;
  margin: 10px;">
Start_time=1.0e-3 &nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; Start of integration (in units of &tau;<sub>e</sub>) <br>
Time_ratio=1.02 &nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; Ratio of successive discrete times <br>
</div>

<p> <span style="color: #ff0000;"><strong>% Options for results </strong></span> </p>
<div style="background: ghostwhite;
  padding: 10px;
  border: 1px solid lightgray;
  margin: 10px;">
CalcDielectric=no &nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; "yes" asks for dielectric relaxation spectra. <br>
OutTermRelaxPathways=no &nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; "yes" outputs individual chain relaxation modes. <br>
OutPhiPhiST=no &nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; "yes" outputs evolution of different tube diameters <br>
Output_G_of_t=no &nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; "yes" asks for time relaxation of modulus <br>
</div>

<p> <span style="color: #ff0000;"><strong>% Control of output  </strong></span> </p> 
<div style="background: ghostwhite;
  padding: 10px;
  border: 1px solid lightgray;
  margin: 10px;">
OutputFormat=Default &nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; Other options are "Text", "CSV" and "RepTate" <br>
CSVdelimiter=, &nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; For <em> OutputFormat=CSV </em> you can specify a different delimiter than usual comma (,) <br>
Add_header=yes &nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; "no" does not add header line in the output files <br>
label=&nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; You can specify a string as a label (default is an empty string). The label will be used in output file names. <br>
chem=&nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; You can specify a string as chemistry (default is an empty string). If specifed and <em> OutputFormat=RepTate  </em>, this will be added in the output headers. <br>
origin=&nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; You can specify a string as origin (default is an empty string). If specifed and <em> OutputFormat=RepTate  </em>, this will be added in the output headers. <br>
Temp=0.0&nbsp; &nbsp; &nbsp; % &nbsp; &nbsp; You can specify the temperature (in degree centigrades). If <em> OutputFormat=RepTate  </em>, this will be added in the output headers. <br>
</div>

<div style="background: lavender; padding: 0px; border: 1px solid lightblue; margin: 1px;">
<SMALL>
Go to  <strong> <A HREF="sec_intro"> Table of Contents </A> </strong> <br>
&rArr; \ref sec_intro &nbsp; &nbsp;
&rArr; \ref sec_usage &nbsp; &nbsp;
&rArr; \ref sec_input &nbsp; 
&bull; <span style="color: #9096a3;"> <A HREF="sec_inp"> Material input file </A> &nbsp; </span> 
&bull; <span style="color: #9096a3;"> <A HREF="sec_rc"> Resource file </A> </span> &nbsp; &nbsp;
&rArr;  \ref sec_output  &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_gtp"> Relaxation spectra </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_gt"> Time relaxation </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_phi"> Tube diameters </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_pathway"> Relaxation pathways </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_pathway"> Relaxation pathways </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_log"> Log file </A> </span> &nbsp;
</SMALL>
</div>

\section sec_output Output files
By default the code only outputs the mechanical relaxation spectra G&prime;(&omega;) and G&Prime; (&omega;). 
In addition, you can
ask it to output the dielectric relaxation spectra &epsilon;&prime;(&omega;) and
&epsilon;&Prime;(&omega;) (assuming that the dipoles are aligned along the chain backbone), 
time domain mechanical relaxation G(t), 
evolution of different relevant tube constraints after an instantaneous small shear deformation, and assignment of 
the terminal relaxation pathway for each chain in the ensemble. These additional outputs are initiated by setting the
appropriate flags in the resource file to <em> yes </em>. The different outputs are directed to different files with
the contents somewhat dependent on the <em> OutputFormat </em> variable set from the resource file. If the
<em> label </em> option is set in the resource file, the files include the label as part of their names. 

If <em> OutputFormat=Default</em>, 
the output file names have  <strong><em> .dat </em></strong>
extensions. 
Unless the option <em> Add_header </em> is not set to <em> no </em> in the resource file (the default behaviour
is <em> Add_header=yes </em>), the first line will be a header line
starting with a hash (\#) character (default comment option for many UNIX plotting softwares).
The choice  <em> OutputFormat=Text</em> behaves similarly as the <em> OutputFormat=Default</em> option, except that
the filenames end with <strong><em> .txt </em></strong> extensions and the header line, if not switched off
with <em> Add_header=no </em> in the resource file,  start without a \# character. <em> OutputFormat=CSV </em> behaves like <em> OutputFormat=Text</em> except the entries are separated by a comma (,) (or, any other character
chosen via <em> CSVdelimiter </em> in the resource file) and the file names end with <strong><em> .csv </em></strong>
extensions.
<em> OutputFormat=RepTate</em> uses 
<A HREF="https://reptate.readthedocs.io/"> RepTate </A> specific extensions and data formats for the relaxation spectra and
the time relaxation function. For other outputs, it uses the same outputs as the <em> OutputFormat=Text</em> choice. 
The headers for the relaxation spectra and
the time relaxation function in this case contain temperature that can be set via the variable <em> Temp</em> in
the resource file. In absence of a supplied value, a default temperature of 0&deg;C will be added to the headers. 
Additional options <em>chem</em>, <em>label</em>, and <em>origin</em> can be set via the resource file and they will be
added in the RepTate format output headers.

The subsections below document the different outputs separately.

<div style="background: lavender; padding: 0px; border: 1px solid lightblue; margin: 1px;">
<SMALL>
Go to  <strong> <A HREF="sec_intro"> Table of Contents </A> </strong> <br>
&rArr; \ref sec_intro &nbsp; &nbsp;
&rArr; \ref sec_usage &nbsp; &nbsp;
&rArr; \ref sec_input &nbsp; 
&bull; <span style="color: #9096a3;"> <A HREF="sec_inp"> Material input file </A> &nbsp; </span> 
&bull; <span style="color: #9096a3;"> <A HREF="sec_rc"> Resource file </A> </span> &nbsp; &nbsp;
&rArr;  \ref sec_output  &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_gtp"> Relaxation spectra </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_gt"> Time relaxation </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_phi"> Tube diameters </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_pathway"> Relaxation pathways </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_pathway"> Relaxation pathways </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_log"> Log file </A> </span> &nbsp;
</SMALL>
</div>

\subsection sec_gtp Relaxation spectra outputs

By default, the code always outputs G&prime;(&omega;) and G&Prime;(&omega;) in an range of
angular frequencies &omega;<sub>min</sub> and &omega;<sub> max</sub>
with the ratio of subsequent frequencies being &omega; <sub>ratio</sub>. These frequency
information is set in the first line of the <A HREF="sec_inp">material input file</A>. 
In addition, dielectric relaxation
output is given if either <strong> <em> -d </em> </strong> option is used at the command line or
there is an entry <em> CalcDielectric=yes </em> in the resource file. 

Except for <em> OutputFormat=RepTate</em>, if the varialbe <em> label</em> is not set, the releaxation spectra output 
is written in a file <strong> RelSpec.extn </strong> with 
<em> extn</em> is either <em> dat </em>, <em> txt</em>, or <em> csv </em> depending on the setting for
the <em> OutputFormat</em>. If the <em> label</em> variable is set, for example <em> label=PS112k </em>, the
file name instead will be set to <strong>RS_PS112k.extn</strong> with appropriate choices of <em> extn</em>.
The entries in the file are <strong> 1. </strong> frequency &omega;, <strong> 2. </strong> dynamic storage modulus
G&prime;(&omega;), <strong> 3. </strong> dynamic loss modulus G&Prime;(&omega;), <strong> 4. </strong> dynamic viscosity
&eta;&Prime; (&omega;),  <strong> 5. </strong> dielectric storage modulus &epsilon;&prime;(&omega;), <strong> 6. </strong>
dielectric loss modulus &epsilon;&Prime;(&omega;). The dielectric information (columns 5 and 6) are only present if
appropriate instruction is given either via the command line flag or via the resource file.


If <em> OutputFormat=RepTate </em> is chosen, the mechanical output is written in <strong> MechSpec.tts </strong> 
in the absence of <em> label </em> variable in the resource file, and, if asked for, dielectric response in file
<strong> DiSpec.dls </strong>. If <em> label </em> is set, for example as <em> PS112k </em>, the file names will be
<strong> PS112k.tts </strong> and <strong> PS112k.dls </strong> respectively. 
The contents of the mechanical relaxation file
are the  <strong> 1. </strong> frequency &omega;, <strong> 2. </strong> dynamic storage modulus
G&prime;(&omega;), <strong> 3. </strong> dynamic loss modulus G&Prime;(&omega;) and those of the dielectric file
are the  <strong> 1. </strong> frequency &omega;, <strong> 2. </strong> dielectric storage modulus &epsilon;&prime;(&omega;), <strong> 3. </strong>
dielectric loss modulus &epsilon;&Prime;(&omega;).

<div style="background: lavender; padding: 0px; border: 1px solid lightblue; margin: 1px;">
<SMALL>
Go to  <strong> <A HREF="sec_intro"> Table of Contents </A> </strong> <br>
&rArr; \ref sec_intro &nbsp; &nbsp;
&rArr; \ref sec_usage &nbsp; &nbsp;
&rArr; \ref sec_input &nbsp; 
&bull; <span style="color: #9096a3;"> <A HREF="sec_inp"> Material input file </A> &nbsp; </span> 
&bull; <span style="color: #9096a3;"> <A HREF="sec_rc"> Resource file </A> </span> &nbsp; &nbsp;
&rArr;  \ref sec_output  &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_gtp"> Relaxation spectra </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_gt"> Time relaxation </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_phi"> Tube diameters </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_pathway"> Relaxation pathways </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_pathway"> Relaxation pathways </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_log"> Log file </A> </span> &nbsp;
</SMALL>
</div>

\subsection sec_gt  Time relaxation
Time domain decay of modulus after a step strain is calculated if <em> Output_G_of_t=yes </em> option is
set via the <A HREF="sec_rc"> resource file </A> (the default is <em> Output_G_of_t=no</em>). As with relaxation
spectra, file name extensions for <em>OutputFormat=Default</em>, <em> Text</em> and <em> CSV </em> are
respectively .dat, .txt, and .csv. In the absence of <em>label</em> in the <A HREF="sec_rc"> resource file </A>,
the data is written in a file named <strong> MechRel </strong> with appropriate file extension. The data
are set of time t, modulus G(t), tube survival probability &mu;(t), and the constraint release contribution
R(t). With <em>OutputFormat=RepTate</em>, time t and modulus G(t) is written in file <strong> MechRel.gt</strong>.
With the <em>label</em> variable set, for example as <em>label=PS100k</em>, the file name for <em>OutputFormat=RepTate</em> choice will be <strong> PS100k.gt</strong>. With the same label, <em>OutputFormat=Default</em> will use
a file <strong> MR_PS100k.dat </strong>. Other choices will change the file extension appropriately. 

The range of time for the time relaxation output is chosen to be between 
10<sup>-4</sup> &tau;<sub>e</sub> and 10<sup>4</sup> &tau;<sub>d</sub>, with &tau;<sub>d</sub> being the longest
relaxation time. These times can only be changed by editing <em> src/Rheology/Calc_goft.cpp </em> in the source code.


<div style="background: lavender; padding: 0px; border: 1px solid lightblue; margin: 1px;">
<SMALL>
Go to  <strong> <A HREF="sec_intro"> Table of Contents </A> </strong> <br>
&rArr; \ref sec_intro &nbsp; &nbsp;
&rArr; \ref sec_usage &nbsp; &nbsp;
&rArr; \ref sec_input &nbsp; 
&bull; <span style="color: #9096a3;"> <A HREF="sec_inp"> Material input file </A> &nbsp; </span> 
&bull; <span style="color: #9096a3;"> <A HREF="sec_rc"> Resource file </A> </span> &nbsp; &nbsp;
&rArr;  \ref sec_output  &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_gtp"> Relaxation spectra </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_gt"> Time relaxation </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_phi"> Tube diameters </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_pathway"> Relaxation pathways </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_pathway"> Relaxation pathways </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_log"> Log file </A> </span> &nbsp;
</SMALL>
</div>
\subsection sec_phi Tube diameters
If <em> OutPhiPhiST=yes </em> option is
set via the <A HREF="sec_rc"> resource file </A> (the default is <em> OutPhiPhiST=no</em>), different
dynamic tube diameters (<strong> a<sub>X</sub></strong>) are output in terms of associated 
fractions of unrelaxed tube constraints (<strong> &phi;<sub>X</sub> </strong>):
<strong> a<sub>X</sub> = a<sub>0</sub> &phi;<sub>X</sub><sup>-&alpha;/2</sup></strong> with <strong>a<sub>0</sub></strong> being the <em>equilibrium</em> tube diameter or the bare tube diameter. The output is written in a file named
<strong>STube</strong> with appropriate extension in the absence of the <em> label</em> string. If the <em>label</em> 
variable is set, for example as <em>label=PI645k</em>, the file name will be <strong>STube_PI645k</strong> with appropriate extension. The output contains <strong> 1.</strong> time after step deformation t, 
<strong> 2.</strong> fraction of unrelaxed tube contraints &phi;(t), 
<strong> 3.</strong> supertube fraction &phi;<sub>ST</sub>(t),
<strong> 4. </strong> <em> equilibriated </em> constraint fraction &phi;<sub>eq</sub>(t),
<strong> 5. </strong> constraint fraction allowing reptation &phi;<sub>rept</sub>(t), and
<strong> 6. </strong> enhancement of reptation due to contour length fluctuation along fat tube &Psi;<sub>min</sub>(t).

<div style="background: lavender; padding: 0px; border: 1px solid lightblue; margin: 1px;">
<SMALL>
Go to  <strong> <A HREF="sec_intro"> Table of Contents </A> </strong> <br>
&rArr; \ref sec_intro &nbsp; &nbsp;
&rArr; \ref sec_usage &nbsp; &nbsp;
&rArr; \ref sec_input &nbsp; 
&bull; <span style="color: #9096a3;"> <A HREF="sec_inp"> Material input file </A> &nbsp; </span> 
&bull; <span style="color: #9096a3;"> <A HREF="sec_rc"> Resource file </A> </span> &nbsp; &nbsp;
&rArr;  \ref sec_output  &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_gtp"> Relaxation spectra </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_gt"> Time relaxation </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_phi"> Tube diameters </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_pathway"> Relaxation pathways </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_pathway"> Relaxation pathways </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_log"> Log file </A> </span> &nbsp;
</SMALL>
</div>
 \subsection sec_pathway Terminal relaxation pathways
<p>If the variable <em><strong>OutTermRelaxPathways</strong></em> is set to <em><strong>yes</strong></em> via the resource file, information about terminal relaxation pathways of each chain is written in an output file named  <em>TermRelax.dat</em> (or <em>.txt</em>, or <em> .csv</em>) in the absence of the <em> label </em> variable. With <em> label </em> set to some string,
that string is appended to <em>TermR_</em> along with an appropriate extension.

The output contains <strong>1.</strong> Index <em><strong>i</strong></em> (index of the polymer in the ensemble),
<strong>2.</strong> Weight fraction <strong><em>w<sub>i</sub></em></strong>,
<strong>3.</strong>  Molar mass <strong><em>M<sub>i</sub></em></strong>,
<strong>4.</strong> Relaxation time <strong><em>&tau;<sub>relax</sub> </em> </strong>,
<strong>5.</strong> Integer code for relaxation pathway,
<strong>6.</strong> Relevant constraint fraction,
<strong>7.</strong> Speed up factor from fat tube CLF.

The integer code in the fifth column is set to 0 for unentangled chains. For those chains,
<strong><em>&tau;<sub>relax</sub> </em></strong> is set to the Rouse time of the chains  <strong><em>&tau;<sub>R</sub> </em> </strong>. The entries in both the sixth and seventh columns in this case are 1 signifying irrelevance of tube dilation for
the relaxation of these chains. 

When the chain of concern relaxes by reptation, the fifth column is set to 1 and 
the &nbsp;<strong><em>&tau;<sub>relax</sub></em></strong>
is set to the reptation time&nbsp;<strong><em>&tau;<sub>d</sub> </em> </strong>. The sixth column
in this case gives $&phi;<sub>T</sub>$ associated with the optimal tube diameter for 
reptation at the time the chain switches from relaxing by contour length fluctuation to reptation.
The seventh column in this case is the speed up due to fat tube CLF &Psi;<sub>min</sub>, evaluated
at the time the chain commits to relax remaining stress via reptation.

When a chain effectively becomes unentangled in the <em> supertube</em>, the remaining 
stress associated with the chain relaxes with this time scale via <em> disentanglement</em>. In such cases,
the fifth column is set to 2 and the &nbsp;<strong><em>&tau;<sub>relax</sub></em></strong>
is set to the time at which the chain first becomes disentangled. The sixth column in this case report &phi;<sub>ST</sub>
and the seventh column reports the speed up factor &Psi;<sub>min</sub> evaluated at the time of disentanglement.

<div style="background: lavender; padding: 0px; border: 1px solid lightblue; margin: 1px;">
<SMALL>
Go to  <strong> <A HREF="sec_intro"> Table of Contents </A> </strong> <br>
&rArr; \ref sec_intro &nbsp; &nbsp;
&rArr; \ref sec_usage &nbsp; &nbsp;
&rArr; \ref sec_input &nbsp; 
&bull; <span style="color: #9096a3;"> <A HREF="sec_inp"> Material input file </A> &nbsp; </span> 
&bull; <span style="color: #9096a3;"> <A HREF="sec_rc"> Resource file </A> </span> &nbsp; &nbsp;
&rArr;  \ref sec_output  &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_gtp"> Relaxation spectra </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_gt"> Time relaxation </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_phi"> Tube diameters </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_pathway"> Relaxation pathways </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_pathway"> Relaxation pathways </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_log"> Log file </A> </span> &nbsp;
</SMALL>
</div>
    \subsection sec_log Log file 
Command line argument <strong> -L </strong> directs the code to write information in a file named
<strong> LP2Rlog.txt </strong>. If something goes wrong during processing the input files, the 
log file can be helpful in resolving the place where the code failed. The log file also reports
molar mass moments (M<sub>N</sub>, M<sub>W</sub>, and M<sub>Z</sub>) and the zero-shear viscosity.

<div style="background: lavender; padding: 0px; border: 1px solid lightblue; margin: 1px;">
<SMALL>
Go to  <strong> <A HREF="sec_intro"> Table of Contents </A> </strong> <br>
&rArr; \ref sec_intro &nbsp; &nbsp;
&rArr; \ref sec_usage &nbsp; &nbsp;
&rArr; \ref sec_input &nbsp; 
&bull; <span style="color: #9096a3;"> <A HREF="sec_inp"> Material input file </A> &nbsp; </span> 
&bull; <span style="color: #9096a3;"> <A HREF="sec_rc"> Resource file </A> </span> &nbsp; &nbsp;
&rArr;  \ref sec_output  &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_gtp"> Relaxation spectra </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_gt"> Time relaxation </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_phi"> Tube diameters </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_pathway"> Relaxation pathways </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_pathway"> Relaxation pathways </A> </span> &nbsp;
&bull; <span style="color: #9096a3;"> <A HREF="sec_log"> Log file </A> </span> &nbsp;
</SMALL>
</div>
<HR>
  */

