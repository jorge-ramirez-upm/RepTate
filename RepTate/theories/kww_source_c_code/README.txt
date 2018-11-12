To compile the C files:

MacOs
gcc -o ../kww_lib_darwin.so -shared -fPIC -O2 kww.c

Windows 64-bit (using MINGW64)
gcc -o ../kww_lib_win32.so -shared -fPIC -O2 kww.c

Windows 32-bit (using MINGW32)
gcc -o ../kww_lib_win32_i686.so -shared -fPIC -O2 kww.c

Linux
gcc -o ../kww_lib_linux.so -shared -fPIC -O2 kww.c
