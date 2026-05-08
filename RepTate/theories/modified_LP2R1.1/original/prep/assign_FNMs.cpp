#include "../include/LP2R.h"
/**
  * \file
  * \brief
  * Depending on the output format and presence of "reptate_label", select file names for output 
  */
void assign_FNMs(void)
{
using namespace LP2R_NS;
// Relaxation pathways or tube diameter evolution is not understood by RepTate. 
// treat RepTate output as text file for these two files

if (has_label){
 if(OutputFormat == "RepTate"){
  MechRelSpecFNM=reptate_label+".tts";
  DiRelSpecFNM=reptate_label+".dls";
  MechRelFNM=reptate_label+".gt";
  OutTermRelaxFNM=std::string("TermR_")+reptate_label+".txt";
  OutPhiPhiSTFNM=std::string("STube_")+reptate_label+".txt";
                            }
 else if(OutputFormat == "CSV"){
   RelSpecFNM=std::string("RS_")+reptate_label+".csv";
   MechRelSpecFNM=std::string("RS_")+reptate_label+".csv";
   MechRelFNM=std::string("MR_")+reptate_label+".csv";
   OutTermRelaxFNM=std::string("TermR_")+reptate_label+".csv";
   OutPhiPhiSTFNM=std::string("STube_")+reptate_label+".csv";
                             }
 else if(OutputFormat == "Text"){
   RelSpecFNM=std::string("RS_")+reptate_label+".txt";
   MechRelSpecFNM=std::string("RS_")+reptate_label+".txt";
   MechRelFNM=std::string("MR_")+reptate_label+".txt";
   OutTermRelaxFNM=std::string("TermR_")+reptate_label+".txt";
   OutPhiPhiSTFNM=std::string("STube_")+reptate_label+".txt";
                                }
 else{
  RelSpecFNM=std::string("RS_")+reptate_label+".dat";
  MechRelSpecFNM=std::string("RS_")+reptate_label+".dat";
  MechRelFNM=std::string("MR_")+reptate_label+".dat";
  OutTermRelaxFNM=std::string("TermR_")+reptate_label+".dat";
  OutPhiPhiSTFNM=std::string("STube_")+reptate_label+".dat";
     }
              }
else{ // no label to add
 if(OutputFormat == "RepTate"){
    MechRelSpecFNM="MechSpec.tts";
    DiRelSpecFNM="DiSpec.tts";
    MechRelFNM="MechRel.gt";
   OutTermRelaxFNM=std::string("TermRelax")+".txt";
   OutPhiPhiSTFNM=std::string("STube")+".txt";
                            }
 else if(OutputFormat == "CSV"){
   RelSpecFNM="RelSpec.csv";
   MechRelSpecFNM="RelSpec.csv";
   MechRelFNM="MechRel.csv";
   OutTermRelaxFNM=std::string("TermRelax")+".csv";
   OutPhiPhiSTFNM=std::string("STube")+".csv";
                             }
 else if(OutputFormat == "Text"){
   RelSpecFNM="RelSpec.txt";
   MechRelSpecFNM="RelSpec.txt";
   MechRelFNM="MechRel.txt";
   OutTermRelaxFNM=std::string("TermRelax")+".txt";
   OutPhiPhiSTFNM=std::string("STube")+".txt";
                                }
 else{
   RelSpecFNM=std::string("RelSpec")+".dat";
   MechRelSpecFNM=std::string("RelSpec")+".dat";
   MechRelFNM=std::string("MechRel")+".dat";
   OutTermRelaxFNM=std::string("TermRelax")+".dat";
   OutPhiPhiSTFNM=std::string("STube")+".dat";
     }
    }
if(OutTermRelaxPathways){ // This file will have output as the relaxation progresses
  f_trelax.open(OutTermRelaxFNM, std::ios_base::out);
if(Add_header){
 if(OutputFormat=="CSV"){
  f_trelax << "index" << CSVdelimiter << "wt" << CSVdelimiter << "M" << CSVdelimiter  
           << "t_relax" <<CSVdelimiter << "relax_pathway"<< CSVdelimiter 
           << "phi_X" <<CSVdelimiter << "SpeedupFactor" << std::endl;
                        } 
 else if(OutputFormat == "Default"){
  f_trelax << "# index wt M  t_relax  relax_pathway  phi_X  SpeedupFactor" << std::endl;
                                   }
 else{
  f_trelax << "index wt M  t_relax  relax_pathway  phi_X  SpeedupFactor" << std::endl;
     }
              }
                        }
if(OutPhiPhiST){
 f_phi.open(OutPhiPhiSTFNM, std::ios_base::out);
 if(Add_header){
 if(OutputFormat=="CSV"){
   f_phi << "t" << CSVdelimiter << "phi" << CSVdelimiter 
         << "phi_ST" << CSVdelimiter << "phi_eq" << CSVdelimiter 
         << "phi_rept" << CSVdelimiter  << "Psi_min" << std::endl;
                        }
 else if(OutputFormat == "Default"){
  f_phi << "# t  phi  phi_ST  phi_eq  phi_rept  Psi_min" << std::endl; 
                                   }
 else{
  f_phi << "t  phi  phi_ST  phi_eq  phi_rept  Psi_min" << std::endl; 
     }
               }
if(OutputFormat=="CSV"){
   f_phi << "0.0" << CSVdelimiter << "1.0" << CSVdelimiter 
         << "1.0" << CSVdelimiter << "1.0" << CSVdelimiter 
         << "1.0" << CSVdelimiter << "1.0" << std::endl;
                       }
else{ f_phi << "0.0, 1.0, 1.0, 1.0, 1.0, 1.0" << std::endl;}

               }
}
