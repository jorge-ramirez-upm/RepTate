To compile the C files:

MacOs
gcc -o ../dtd_lib_darwin.so -shared -fPIC -O2 dtd.c trapz.c qtrap.c

Windows 64-bit (using MINGW64)
gcc -o ../dtd_lib_win32.so -shared -fPIC -O2 dtd.c trapz.c qtrap.c

Windows 32-bit (using MINGW32)
gcc -o ../dtd_lib_win32_i686.so -shared -fPIC -O2 dtd.c trapz.c qtrap.c

Linux
gcc -o ../dtd_lib_linux.so -shared -fPIC -O2 dtd.c trapz.c qtrap.c
