To compile the BoB files:

From here go to:
code/src/obj/

and run the makefile "makefile_for_lib":
make -f makefile_for_lib

This will produce a file "bob2p5_lib.so"
Copy that file to RepTate's "theories/" folder and change its name according to your OS

MacOs
cp bob2p5_lib.so ../../../../bob2p5_lib_darwin.so

Windows 64-bit
cp bob2p5_lib.so ../../../../bob2p5_lib_win32.so

Windows 32-bit 
cp bob2p5_lib.so ../../../../bob2p5_lib_win32_i686.so

Linux
cp bob2p5_lib.so ../../../../bob2p5_lib_linux.so
 
