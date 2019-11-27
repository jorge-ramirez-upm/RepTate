gcc -o landscape_darwin.so -shared -fPIC -lm -I/usr/local//include  /usr/local/lib/libgsl.a  /usr/local/lib/libgslcblas.a  -O2 landscape.c
mv landscape_darwin.so ../
