import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from scipy.stats import chi2

def scatter_ellipse(x, y, ax, kind = 'sd', percentile=0.95, subset=None, corrcoef=False, **kwargs):
    # Eigenvectors of symmetric covariance matrix are orthogonal principal components
    cov = np.cov(np.stack([x, y]))
    evals, evecs = np.linalg.eigh(cov)
    # Eigenvalues give variance along principal components
    if kind == 'sd':
        width, height = 2 * np.sqrt(evals)
    elif kind == 'sem':
        width, height = 2 * np.sqrt(evals) / np.sqrt(len(x))
    elif kind == 'percentile':
        width, height = 2 * np.sqrt(evals) * np.sqrt(chi2.ppf((1+percentile)/2, df=2))
    else:
        raise Exception('Must define error method: "sd", "sme", or "percentile".')
    # Eigenvectors give direction of greatest variance
    v1, v2 = evecs[:, 0]
    angle = np.degrees(np.arctan(v2/v1))
    # Obtain correlation coefficient
    r2 = np.corrcoef(np.stack([x, y]))[0, 1]**2
    
    if subset is None:
        subset = np.arange(len(x))
    ax.scatter(x[subset], y[subset], **kwargs)
    ax.scatter(x[~subset], y[~subset], **kwargs)
    err = Ellipse((np.mean(x), np.mean(y)), 
                  width=width, height=height, ec='k', facecolor='none',
                  angle=angle, label=r'$\pm \sigma$')
    if corrcoef:
        ax.annotate(s='$R^2$: {:.3f}'.format(r2),xy=(.1, .2), xycoords='axes fraction', fontsize=12)
    ax.scatter(np.mean(x), np.mean(y), marker='o', color='r', label=r'$\mu$')
    ax.add_patch(err)