#ifndef CUDACLAW_ALLOCATE_H
#define CUDACLAW_ALLOCATE_H

#ifdef __cplusplus
extern "C"
{
#endif

struct fclaw2d_patch;
struct fclaw2d_global;

/* This can breaks cuda if memory is not aligne dproperly; use -malign-double flag
   in gcc */
   
typedef struct  cudaclaw_fluxes
{
 #if 1   
    size_t num;
    size_t num_aux;
    size_t num_waves;
    size_t num_speeds;
#endif    

    size_t num_bytes;   /* All members have the same size */
    size_t num_bytes_aux;  
    size_t num_bytes_waves;  
    size_t num_bytes_speeds;  

    double* qold;
    double* aux;
    double *qold_dev;
    double *aux_dev;
    
    double *fp_dev;
    double *fm_dev;
    double *gp_dev;
    double *gm_dev;

    double *waves_dev;
    double *speeds_dev;

    double dx;
    double dy;

    double xlower;
    double ylower;
} cudaclaw_fluxes_t;

void cudaclaw_allocate_fluxes(struct fclaw2d_global *glob,
                               struct fclaw2d_patch *patch);

void cudaclaw_deallocate_fluxes(struct fclaw2d_global *glob,
                                 struct fclaw2d_patch *patch);


#ifdef __cplusplus
}
#endif
#endif