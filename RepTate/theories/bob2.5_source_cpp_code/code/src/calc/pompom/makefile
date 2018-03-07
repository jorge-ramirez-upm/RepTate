CC=g++
CFLAGS=
all_obj: calc_pompom.o odeint.o pm_shear.o pm_uext.o pompom.o rkck.o rkqs.o graceheadernlin.o
.c.o:
	$(CC) $(CFLAGS) -c $< -o $@
clean :
	rm *.o
