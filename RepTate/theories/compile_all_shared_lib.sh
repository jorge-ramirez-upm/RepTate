#!/bin/bash
#####
# Compile all shared library for RepTate
#####
system="darwin" # "linux" "win32" "win32_i686"
flags="-shared -fPIC -O2"

cd dtd_source_c_code
gcc -o ../dtd_lib_${system}.so ${flags} dtd.c trapz.c qtrap.c

cd ../kww_source_c_code
gcc -o ../kww_lib_${system}.so ${flags} kww.c

cd ../react_source_c_code
gcc -o ../react_lib_${system}.so ${flags} binsandbob.c polybits.c polycleanup.c polymassrg.c ran3.c tobitabatch.c tobitaCSTR.c multimetCSTR.c dieneCSTR.c calc_architecture.c

cd ../rouse_source_c_code
gcc -o ../rouse_lib_${system}.so ${flags} rouse.c

cd ../rp_blend_source_c_code
gcc -o ../rp_blend_lib_${system}.so ${flags} derivs_rolie_poly_blend.c

cd ../sccr_source_c_code
gcc -o ../sccr_lib_${system}.so ${flags} sccr.c

cd ../schwarzl_source_c_code
gcc -o ../schwarzl_lib_${system}.so ${flags} schwarzl.c

cd ../modified_bob2.5/code/src/obj
rm -f *.o
rm -f *.so
make -f makefile_for_lib
cp bob2p5_lib.so ../../../../bob2p5_lib_${system}.so