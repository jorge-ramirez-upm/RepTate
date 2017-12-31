#ifndef POLYBITS_H
#define POLYBITS_H
#define MIN(a, b) ({ __typeof__ (a) _a = (a); __typeof__ (b) _b = (b); _a < _b ? _a : _b; })
#define MAX(a, b) ({ __typeof__ (a) _a = (a); __typeof__ (b) _b = (b); _a < _b ? _b : _a; })

#include <stdbool.h>
#include "my_structs.h"

extern int maxbobbins;
extern int maxmwdbins;
extern int maxarm; //  maxarm=10000000;
extern int maxpol;
extern int maxreact;

extern arm *arm_pool;
extern polymer *br_poly;
extern reactresults *react_dist;

extern int first_in_pool;
extern int first_poly_in_pool;
extern int first_dist_in_pool;
extern int mmax;
extern int num_react;
extern int arms_left;
extern bool react_pool_initialised;
extern bool react_pool_declared;
extern bool arms_avail;  // these flags simply record
extern bool polys_avail; // availability of arms
extern bool dists_avail;

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