#!/usr/bin/env python3
import numpy as np
import scipy.special as special
import matplotlib.pyplot as plt

#  Format text used in plots to match LaTeX
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


def pvalue_from_zscore(z_score):
    return 0.5 * (1 - special.erf(z_score / np.sqrt(2)))


def zscore_from_pvalue(p_value):
    return np.sqrt(2) * special.erfinv(1 - 2 * p_value)


def plot_pvalue(z_range, fontsize=14):
    fig, ax = plt.subplots(1, 1)
    ax.set_yscale('log')

    x = np.linspace(min(z_range), max(z_range), 10000)
    ax.plot(x, pvalue_from_zscore(x), color='black')

    ax.set_xlim(left=-0.1)

    ax.set_xlabel(r'$z$-score', fontsize=fontsize)
    ax.set_ylabel(r'$p$\,-value', fontsize=fontsize)

    return fig


def plot_zscore(p_range, fontsize=14):
    fig, ax = plt.subplots(1, 1)

    x = np.linspace(min(p_range), max(p_range), 10000)
    ax.plot(x, zscore_from_pvalue(x), color='black')

    ax.invert_xaxis()
    ax.set_xscale('log')

    ax.set_xlabel(r'$p$\,-value', fontsize=fontsize)
    ax.set_ylabel(r'$z$-score', fontsize=fontsize)

    return fig


def main():
    pvalues_plot = plot_pvalue([0, 5])

    image_write_path = 'figures/results/'
    extensions = ['pdf', 'png', 'eps']
    for ext in extensions:
        pvalues_plot.savefig(f'{image_write_path}pvalues_from_zscores.{ext}')


if __name__ == '__main__':
    main()
