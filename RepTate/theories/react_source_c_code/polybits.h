#ifndef POLYBITS_H
#define POLYBITS_H

#include <stdbool.h>
#include "react_structs.h"

typedef struct
{
    int maxbobbins;
    int maxmwdbins;
    int maxarm; //  maxarm=10000000;
    int maxpol;
    int maxreact;
} polybits_global_const;

typedef struct
{
 int first_in_pool;
 int first_poly_in_pool;
 int first_dist_in_pool;
 int mmax;
 int num_react;
 int arms_left;
 bool react_pool_initialised;
 bool react_pool_declared;
 bool arms_avail;  // these flags simply record
 bool polys_avail; // availability of arms
 bool dists_avail;
} polybits_global;

extern polybits_global_const pb_global_const;
extern polybits_global pb_global;


extern arm *arm_pool;
extern polymer *br_poly;
extern reactresults *react_dist;

extern void react_pool_init(void);
extern void pool_reinit(void);
extern bool request_arm(int *); // returns false if no arms left
extern void return_arm(int);
extern bool request_poly(int *); // returns false if no polymers left
extern void return_poly_arms(int);
extern void return_poly(int);
extern bool request_dist(int *); // returns false if no distributions left
extern void return_dist(int);
extern void return_dist_polys(int);
extern void armupdown(int, int);

#endif
