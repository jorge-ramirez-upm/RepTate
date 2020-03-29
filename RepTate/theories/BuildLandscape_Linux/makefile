# more advanced makefile
# June 2005

VPATH = ./


SOURCES= main.c landscape.c brent.c c_math.c error.c infnan.c fdiv.c pow_int.c fdfsolver.c newton.c fsolver.c convergence.c stream.c

OBJECTS=main.o landscape.c brent.o c_math.o error.o infnan.o fdiv.o pow_int.c fdfsolver.o newton.o fsolver.o convergence.o stream.o

PRODUCT=landscape

#CC=icpc
CC=gcc


#CFLAGS=	 -O3  -DHAVE_INLINE -L$(GSL)/lib
#L$(GSL)/lib -O2 -m32 -Wall -DHAVE_INLINE  #-fast -B CARE!!! m32 ignores 64bit functionality
CFLAGS= -lm -I/Users/pmzrsg/Dropbox/BuildLandscape/ 




all: $(PRODUCT)
$(PRODUCT): $(OBJECTS)
	$(CC) $(CFLAGS) -o $(PRODUCT) $(OBJECTS) -lm #-lgsl -lgslcblas
#-lgsl -lgslcblas 

.c.o:	
	$(CC) $(CFLAGS) -c $< 

clean:
	rm -f *.o
