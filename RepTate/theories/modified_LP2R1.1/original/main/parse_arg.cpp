#include "../include/LP2R.h"
#include "../include/tclap/CmdLine.h"

/**
  * \file
  * \brief
  * parse command line arguments
  *
  * options [-i input_file] [-r resource_file] [-d] [-L] [-v] [-h] [--version] [--help] \n
  * -i input_file : Read material and polymer information from this file (default: inp.dat) \n\n
  * -r resource_file : Model parameters (default: LP2R.rc).\n
  *  Will use default values if the file does not exist. \n\n
  * -d : Switch on output of dielectric response. \n\n
  * -L : Output steps in LP2Rlog.txt, useful for debugging. \n\n
  * -v / --version : version information \n
  * -h / --help : help page. \n
  */

/**
  * parse command line arguments
  * \param[in] argc number of arguments passed to main.
  * \param[in] argv character array containing the arguments.
  * \return zero if parsed properly and non-zero in case of error.
  */

int parse_arg(int argc, char* argv[])
{
using LP2R_NS::inpFNM;
using LP2R_NS::rcFNM;
using LP2R_NS::CalcDielectric;
using LP2R_NS::GenLogFL;
using LP2R_NS::f_Log;
int rtval=0;
try{
 TCLAP::CmdLine cmd("Linear Polydisperse Polymer (linear) Rheology\n (c) 2022,2023 Chinmay Das and Daniel J. Read \n GNU GPLv3 (or at your option any later version)", ' ', "1.1");
 TCLAP::ValueArg<std::string> inpFLarg("i", "Input_File", "Input file name", false, "inp.dat","input file");
 cmd.add(inpFLarg);
 TCLAP::ValueArg<std::string> rcFLarg("r", "Resource_File", "Resource file name", false, "LP2R.rc","resource file");
 cmd.add(rcFLarg);
 TCLAP::SwitchArg DielectricSwitch("d","dielectric","Calculate Dielectric loss",cmd,false);
 TCLAP::SwitchArg LogSwitch("L","LogFile","Create a log file of everything",cmd,false);
 
 cmd.parse(argc,argv);
 inpFNM=inpFLarg.getValue();
 rcFNM=rcFLarg.getValue();
 CalcDielectric=DielectricSwitch.getValue();
 GenLogFL=LogSwitch.getValue();
   }catch (TCLAP::ArgException &e)  // catch exceptions
        { rtval=1; std::cerr << "error: " << e.error() << " for arg " << e.argId() << std::endl; }
if(GenLogFL){
f_Log.open("LP2Rlog.txt", std::ios_base::out);
f_Log << "Parsed command line:" << std::endl;
f_Log << "   Will look for input in file: " << inpFNM << std::endl;
f_Log << "   Will look for additional resources in file (if present): "<< rcFNM << std::endl;
if(CalcDielectric){
f_Log << "   Will calculate dielectric relaxation (assuming type A dipoles) " << std::endl;
                  }
f_Log << std::endl;
            }

return rtval;
}
