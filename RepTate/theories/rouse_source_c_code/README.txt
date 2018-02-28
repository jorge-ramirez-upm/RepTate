To compile the C files:

MacOs
gcc -o ../rouse_lib_darwin.so -shared -fPIC -O2 rouse.c

Windows (using MINGW)
gcc -o ../rouse_lib_win32.so -shared -fPIC -O2 rouse.c

Linux
gcc -o ../rouse_lib_linux.so -shared -fPIC -O2 rouse.c
