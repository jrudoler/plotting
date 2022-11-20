import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')

def bordered_imshow(X, mask, line_kwargs={"linewidth":4, "color":'k'}, **kwargs):
    shape = X.shape
    im = plt.imshow(X, extent=[0, shape[0], 0, shape[1]], origin='lower', **kwargs)
    ax = plt.gca()
    extent = im.get_extent()
    masked_cells = [(i, j) for i, j in zip(*np.nonzero(mask))]
    for cell in masked_cells:
        # left
        if (cell[0], cell[1]-1) not in masked_cells:
            line = plt.Line2D([extent[0]+(extent[1]/shape[1])*cell[1], extent[0]+(extent[1]/shape[1])*cell[1]],
                              [extent[2]+(extent[3]/shape[0])*cell[0], extent[2]+(extent[1]/shape[0])*cell[0]+1],
                              **line_kwargs)
            ax.add_patch(line)
        # right
        if (cell[0], cell[1]+1) not in masked_cells:
            line = plt.Line2D([extent[0]+(extent[1]/shape[1])*cell[1]+1, extent[0]+(extent[1]/shape[1])*cell[1]+1],
                              [extent[2]+(extent[3]/shape[0])*cell[0], extent[2]+(extent[1]/shape[0])*cell[0]+1],
                              **line_kwargs)
            ax.add_patch(line)
        # above
        if (cell[0]+1, cell[1]) not in masked_cells:
            line = plt.Line2D([extent[0]+(extent[1]/shape[1])*cell[1], extent[0]+(extent[1]/shape[1])*cell[1]+1],
                              [extent[2]+(extent[3]/shape[0])*cell[0]+1, extent[2]+(extent[1]/shape[0])*cell[0]+1],
                              **line_kwargs)
            ax.add_patch(line)
        # below
        if (cell[0]-1, cell[1]) not in masked_cells:
            line = plt.Line2D([extent[0]+(extent[1]/shape[1])*cell[1], extent[0]+(extent[1]/shape[1])*cell[1]+1],
                              [extent[2]+(extent[3]/shape[0])*cell[0], extent[2]+(extent[1]/shape[0])*cell[0]],
                              **line_kwargs)
            ax.add_patch(line)
    return im, ax