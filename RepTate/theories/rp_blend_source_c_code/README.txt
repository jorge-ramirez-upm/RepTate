To compile the C files:

MacOs
gcc -o ../rp_blend_lib_darwin.so -shared -fPIC -O2 derivs_rolie_poly_blend.c

Windows (using MINGW)
gcc -o ../rp_blend_lib_win32.so -shared -fPIC -O2 derivs_rolie_poly_blend.c

Linux
gcc -o ../rp_blend_lib_linux.so -shared -fPIC -O2 derivs_rolie_poly_blend.c
