import numpy as np
from numba import njit, prange


@njit()
def get_idx_periodic(i, ii, shape):
    return (i + ii) % shape


@njit()
def get_idx(i, ii, shape):
    return i + ii


@njit(parallel=True)
def update_grid2d(grid_in, periodic_bc=True):
    nb_struct = np.array([[-1, -1], [-1,  0], [-1,  1], [0, -1], [0,  1], [1, -1], [1,  0], [1,  1]])
    grid_out = np.zeros_like(grid_in)
    shapex, shapey = grid_out.shape
    
    offset = 0 if periodic_bc else 1
    for i in prange(offset, shapex - offset):
        for j in prange(offset, shapey - offset):
            # accumulate over the nb structure
            _sum, current_state = 0, grid_in[i, j]
            for ii, jj in nb_struct:
                
                if periodic_bc:
                    _sum += grid_in[get_idx_periodic(i, ii, shapex), 
                                    get_idx_periodic(j, jj, shapey)]
                else:
                    _sum += grid_in[get_idx(i, ii, shapex), 
                                    get_idx(j, jj, shapey)]
            
            # compact game of life rules
            if _sum == 3:
                grid_out[i, j] = 1
            elif current_state == 1 and _sum == 2:
                grid_out[i, j] = 1
                    
    return grid_out
