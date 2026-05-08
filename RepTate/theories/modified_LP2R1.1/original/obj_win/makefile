### compile with mingw as static executable
cpp=g++ -std=c++11 -static -Wall -O3 -fPIC
obj_main=../main/parse_arg.cpp
obj_all=parse_arg.o ReadInput.o ReadRCFL.o safeGetLine.o  genPolyLin.o GenLinLogNormal.o \
  GenLinGPC.o GenLinWt.o assign_FNMs.o \
  GetPhiEq.o  frac_unrelaxed.o try_reptate.o arm_retraction.o time_step.o \
  add_spectra_headers.o kww.o GStarGlass.o GStarRouse.o GStarFastRouse.o \
GStarSlow.o CalcGstar.o CalcVisc.o add_goft_headers.o GoftRouse.o \
 GoftFast.o GoftTube.o  Calc_goft.o LinRheology.o
default: $(obj_all) ../include/LP2R.h ../include/LP2R_NS.h ../main/LinPoly2Rheo.cpp
	$(cpp) ../main/LinPoly2Rheo.cpp $(obj_all) -o LP2R
	
parse_arg.o : ../main/parse_arg.cpp 
	$(cpp) -c ../main/parse_arg.cpp
ReadInput.o : ../prep/ReadInput.cpp 
	$(cpp) -c ../prep/ReadInput.cpp
ReadRCFL.o : ../prep/ReadRCFL.cpp 
	$(cpp) -c ../prep/ReadRCFL.cpp
safeGetLine.o : ../util/safeGetLine.cpp 
	$(cpp) -c ../util/safeGetLine.cpp
genPolyLin.o : ../prep/genPolyLin.cpp
	$(cpp) -c ../prep/genPolyLin.cpp
GenLinLogNormal.o : ../prep/GenLinLogNormal.cpp
	$(cpp) -c ../prep/GenLinLogNormal.cpp
GenLinGPC.o : ../prep/GenLinGPC.cpp
	$(cpp) -c ../prep/GenLinGPC.cpp
GenLinWt.o : ../prep/GenLinWt.cpp
	$(cpp) -c ../prep/GenLinWt.cpp
assign_FNMs.o : ../prep/assign_FNMs.cpp
	$(cpp) -c ../prep/assign_FNMs.cpp


GetPhiEq.o : ../Relax/GetPhiEq.cpp
	$(cpp) -c ../Relax/GetPhiEq.cpp
frac_unrelaxed.o : ../Relax/frac_unrelaxed.cpp
	$(cpp) -c ../Relax/frac_unrelaxed.cpp
try_reptate.o : ../Relax/try_reptate.cpp
	$(cpp) -c ../Relax/try_reptate.cpp
arm_retraction.o : ../Relax/arm_retraction.cpp
	$(cpp) -c ../Relax/arm_retraction.cpp
time_step.o : ../Relax/time_step.cpp
	$(cpp) -c ../Relax/time_step.cpp


add_spectra_headers.o : ../Rheology/add_spectra_headers.cpp
	$(cpp) -c ../Rheology/add_spectra_headers.cpp
kww.o : ../Rheology/kww.c
	$(cpp) -c ../Rheology/kww.c
GStarGlass.o : ../Rheology/GStarGlass.cpp
	$(cpp) -c ../Rheology/GStarGlass.cpp
GStarRouse.o : ../Rheology/GStarRouse.cpp
	$(cpp) -c ../Rheology/GStarRouse.cpp
GStarFastRouse.o : ../Rheology/GStarFastRouse.cpp
	$(cpp) -c ../Rheology/GStarFastRouse.cpp
GStarSlow.o : ../Rheology/GStarSlow.cpp
	$(cpp) -c ../Rheology/GStarSlow.cpp
CalcGstar.o : ../Rheology/CalcGstar.cpp
	$(cpp) -c ../Rheology/CalcGstar.cpp

CalcVisc.o : ../Rheology/CalcVisc.cpp
	$(cpp) -c ../Rheology/CalcVisc.cpp
add_goft_headers.o : ../Rheology/add_goft_headers.cpp
	$(cpp) -c ../Rheology/add_goft_headers.cpp
GoftRouse.o : ../Rheology/GoftRouse.cpp
	$(cpp) -c ../Rheology/GoftRouse.cpp
GoftFast.o : ../Rheology/GoftFast.cpp
	$(cpp) -c ../Rheology/GoftFast.cpp
GoftTube.o : ../Rheology/GoftTube.cpp
	$(cpp) -c ../Rheology/GoftTube.cpp
Calc_goft.o : ../Rheology/Calc_goft.cpp
	$(cpp) -c ../Rheology/Calc_goft.cpp
LinRheology.o : ../Rheology/LinRheology.cpp
	$(cpp) -c ../Rheology/LinRheology.cpp

