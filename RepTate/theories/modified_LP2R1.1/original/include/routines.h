int parse_arg(int argc, char* argv[]);
void ReadRCFL(void);
int ReadInput(void);

int genPolyLin(std::fstream&);
double aaerfcc(const double x);
void GenLinLogNormal(const int n, const double mw, const double pdi, const double wtcomp);
int GenLinGPC(std::string &fname, const double wtcomp);
int GenLinWt(std::string &fname, const double wtcomp);
void assign_FNMs(void);

std::istream& safeGetline(std::istream& is, std::string& t);
std::istream& readEquality(std::istream& is, std::string& sL, std::string& sR);

// relaxation
double GetPhiEq(void);
void frac_unrelaxed(void);
void try_reptate(const int np);
void arm_retraction(const int np, const int indx);
int time_step(const int indx);

// Calculation of responses
void add_spectra_headers(std::fstream &fRh, std::fstream &fDi);
void GStarGlass(const double w, double &gp, double &g2p);
void GStarRouse(double freq, double &gRs, double &g2Rs, double &eRs, double &e2Rs);
void GStarFastRouse(const double w, double &gpf, double &g2pf);
void GStarSlow(const double w, double &gp, double &g2p, double &ep, double &e2p);
void CalcGstar(std::fstream &fRh, std::fstream &fDi);

double CalcVisc(void);
void add_goft_headers(std::fstream &fRh);
double GoftRouse(const double t);
double GoftFast(const double t);
double GoftTube(const double t, double &muoft, double &Roft);
void Calc_goft(std::fstream &fRh);

void LinRheology(void);
