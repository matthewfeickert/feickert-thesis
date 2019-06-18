#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#  Format text used in plots to match LaTeX
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


def pseudorapidity(polar_angle):
    return -np.log(np.tan(polar_angle / 2.0))


def invert_eta(eta):
    return 2 * np.arctan(np.exp(-eta))


def generate_table(polar_angles):
    eta = pseudorapidity(polar_angles)
    df = pd.DataFrame({'Polar Angle': polar_angles, 'Pseudorapidity': eta})
    # Display with drecresing polar angle
    df = df[::-1]
    return df


def plot_pseudorapidity(polar_angles, eta, fontsize=14):
    fig, ax = plt.subplots(1, 1)

    x = np.linspace(0, np.pi / 2.0, 10000)
    ax.plot(
        x,
        pseudorapidity(x),
        color='black',
        label=r'$\eta=-\ln(\tan \,\theta/2)$',
        zorder=1,
    )
    ax.scatter(
        polar_angles,
        eta,
        label=r'$\eta(\theta)$ for $\theta \in \{\pi/2, \pi/4, \pi/8, \pi/16, \pi/32\}$',
        zorder=2,
    )

    fiducial_region = np.linspace(invert_eta(2.5), np.pi / 2.0, 10000)
    fiducial_eta = pseudorapidity(fiducial_region)
    ax.fill_between(
        fiducial_region,
        0,
        fiducial_eta,
        facecolor='blue',
        alpha=0.2,
        label='ATLAS fiducial region coverage',
    )

    ax.invert_xaxis()

    x_ticks = np.pi * np.arange(0, 0.6, 1 / 8.0)
    x_tick_labels = [r'$0$', r'$\pi/8$', r'$\pi/4$', r'$3\pi/8$', r'$\pi/2$']
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_tick_labels)

    ax.set_xlim(left=1.6, right=0.0)
    ax.set_ylim(bottom=-0.05, top=5)

    ax.set_xlabel(r'$\theta$', fontsize=fontsize)
    ax.set_ylabel(r'$\eta$', fontsize=fontsize)

    ax.legend(loc='best', frameon=False)
    return fig


def main():
    n_angles = 5
    polar_angles = np.array([np.pi / np.power(2, n) for n in range(1, n_angles + 1)])
    table = generate_table(polar_angles)
    print(table.to_string(index=False))
    pseudorapidity_figure = plot_pseudorapidity(
        table['Polar Angle'], table['Pseudorapidity']
    )

    image_write_path = 'figures/preface/'
    extensions = ['pdf', 'png']
    for ext in extensions:
        pseudorapidity_figure.savefig(f'{image_write_path}pseudorapidity.{ext}')


if __name__ == '__main__':
    main()
