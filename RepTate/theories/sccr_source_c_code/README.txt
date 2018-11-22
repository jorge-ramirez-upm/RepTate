To compile the C files:

MacOs
gcc -o ../sccr_lib_darwin.so -shared -fPIC -O2 sccr.c

Windows 64-bit (using MINGW64)
gcc -o ../sccr_lib_win32.so -shared -fPIC -O2 sccr.c

Windows 32-bit (using MINGW32)
gcc -o ../sccr_lib_win32_i686.so -shared -fPIC -O2 sccr.c

Linux
gcc -o ../sccr_lib_linux.so -shared -fPIC -O2 sccr.c
