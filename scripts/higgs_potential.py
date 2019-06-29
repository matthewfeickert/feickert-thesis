#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

#  Format text used in plots to match LaTeX
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


def higgs_potential(phi, theta):
    """
    REVISE THIS TO MAKE IT BETTER
    """
    return -theta * np.power(phi, 2) + np.power(phi, 4)


def plot_potential(fontsize=14, elev=None, azim=None):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    n_points = 1000
    theta_scale = np.pi / 4
    phi, phase = np.meshgrid(
        np.linspace(0, theta_scale, n_points), np.linspace(0, 2 * np.pi, n_points)
    )
    phi_real, phi_imaginary = phi * np.cos(phase), phi * np.sin(phase)

    ax.plot_surface(
        phi_real,
        phi_imaginary,
        higgs_potential(phi, theta_scale),
        cmap=plt.cm.YlGnBu_r,
        label=r'Higgs',
    )

    # Follow formatting advice from
    # https://dawes.wordpress.com/2014/06/27/publication-ready-3d-figures-from-matplotlib/
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    # Manual hack to get placement right
    ax.text(0.75, -0.7, -0.22, r'$\phi$', color='black', fontsize=fontsize)
    ax.set_zlabel(r'$V(\phi)$', fontsize=fontsize, labelpad=-13)

    ax.view_init(elev, azim)

    return fig


def main():
    higgs_potential_figure = plot_potential(elev=50, azim=-60)

    image_write_path = 'figures/theory/'
    extensions = ['pdf', 'png']
    for ext in extensions:
        higgs_potential_figure.savefig(f'{image_write_path}higgs_potential.{ext}')


if __name__ == '__main__':
    main()
