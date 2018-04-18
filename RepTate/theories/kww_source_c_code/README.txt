To compile the C files:

MacOs
gcc -o ../kww_lib_darwin.so -shared -fPIC -O2 kww.c

Windows (using MINGW)
gcc -o ../kww_lib_win32.so -shared -fPIC -O2 kww.c

Linux
gcc -o ../kww_lib_linux.so -shared -fPIC -O2 kww.c
