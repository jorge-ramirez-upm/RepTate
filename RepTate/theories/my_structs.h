#ifndef MY_STRUCTS_H
#define MY_STRUCTS_H

#include <stdbool.h>

typedef struct
{
    int nrows, ncols, nnz, L1;
    double **rows;
} double_matrix_struct;

typedef struct
{
    double arm_len, arm_conv, arm_time, arm_tm, arm_tdb;
    int L1, L2, R1, R2, up, down, armnum, armcat;
    bool ended, endfin, scission;
} arm;

typedef struct
{
    int first_end, num_br, bin, num_sat, num_unsat, armnum, nextpoly;
    double tot_len, gfactor;
    bool saved;
} polymer;

typedef struct
{
    double *wt, *avbr, *wmass, *avg, *lgmid; //array[1..maxmwdbins] of ;
    int *numinbin;                           // array[1..maxbobbins] of integer;
    double monmass, M_e, N_e, boblgmin, boblgmax, m_w, m_n, brav;
    int first_poly, next, nummwdbins, numbobbins, bobbinmax, nsaved, npoly, simnumber;
    bool polysaved;
    char name[];
} reactresults;

extern int this_int;
#endif