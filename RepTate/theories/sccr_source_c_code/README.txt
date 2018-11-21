To compile the C files:

MacOs
gcc -o ../sccr_lib_darwin.so -shared -fPIC -O2 sccr.c

Windows (using MINGW)
gcc -o ../sccr_lib_win32.so -shared -fPIC -O2 sccr.c

Linux
gcc -o ../sccr_lib_linux.so -shared -fPIC -O2 sccr.c
