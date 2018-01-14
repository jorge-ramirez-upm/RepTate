To compile the C files:

MacOs
gcc -o ../schwarzl_lib_darwin.so -shared -fPIC -O2 schwarzl.c

Windows (using MINGW)
gcc -o ../schwarzl_lib_win32.so -shared -fPIC -O2 schwarzl.c

Linux
gcc -o ../schwarzl_lib_linux.so -shared -fPIC -O2 schwarzl.c
