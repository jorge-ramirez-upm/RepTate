To compile the C files:

MacOs
gcc -o ../dtd_lib_darwin.so -shared -fPIC -O2 dtd.c trapz.c qtrap.c

Windows (using MINGW)
gcc -o ../dtd_lib_win32.so -shared -fPIC -O2 dtd.c trapz.c qtrap.c

Linux
gcc -o ../dtd_lib_linux.so -shared -fPIC -O2 dtd.c trapz.c qtrap.c
