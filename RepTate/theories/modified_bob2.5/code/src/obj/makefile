cpp=g++ -Wall  -g -O3 -DNBETA 
include fl_UI
include fl_Util
include fl_polygen
include fl_calc
include fl_relax
all_obj=$(UI_obj) $(Util_obj) $(polygen_obj) $(calc_obj) $(relax_obj)

default : $(all_obj) ../main/bob.cpp
	$(cpp) ../main/bob.cpp ../main/end_code.cpp ../calc/FlowPriority/calcsnipprio.cpp \
 ../calc/FlowPriority/calc_flow_priority.cpp  \
 ../calc/FlowPriority/calc_snip_priority.cpp  \
../calc/FlowPriority/sample_alt_time.cpp \
 ../calc/FlowPriority/sample_alt_taus.cpp  $(all_obj) -o bob2p5
clean :
	rm -f *.o

include mk_UI
include mk_Util
include mk_polygen
include mk_calc
include mk_relax
