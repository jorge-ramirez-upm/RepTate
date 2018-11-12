To compile the C files:

MacOs
gcc -o ../react_lib_darwin.so -shared -fPIC -O2 binsandbob.c polybits.c polycleanup.c polymassrg.c ran3.c tobitabatch.c tobitaCSTR.c multimetCSTR.c dieneCSTR.c calc_architecture.c

Windows 64-bit (using MINGW64)
gcc -o ../react_lib_win32.so -shared -fPIC -O2 binsandbob.c polybits.c polycleanup.c polymassrg.c ran3.c tobitabatch.c tobitaCSTR.c multimetCSTR.c dieneCSTR.c calc_architecture.c

Windows 32-bit (using MINGW32)
gcc -o ../react_lib_win32_i686.so -shared -fPIC -O2 binsandbob.c polybits.c polycleanup.c polymassrg.c ran3.c tobitabatch.c tobitaCSTR.c multimetCSTR.c dieneCSTR.c calc_architecture.c

Linux
gcc -o ../react_lib_linux.so -shared -fPIC -O2 binsandbob.c polybits.c polycleanup.c polymassrg.c ran3.c tobitabatch.c tobitaCSTR.c multimetCSTR.c dieneCSTR.c calc_architecture.c
