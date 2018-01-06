To compile the C files:

MacOs
gcc -o ../react_lib_darwin.so -shared -fPIC -O2 binsandbob.c polybits.c polycleanup.c polymassrg.c ran3.c tobitabatch.c

Windows (using MINGW)
gcc -o ../react_lib_win32.so -shared -fPIC -O2 binsandbob.c polybits.c polycleanup.c polymassrg.c ran3.c tobitabatch.c

Linux
gcc -o ../react_lib_linux.so -shared -fPIC -O2 binsandbob.c polybits.c polycleanup.c polymassrg.c ran3.c tobitabatch.c
