#!/usr/bin/env python3
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt

#  Format text used in plots to match LaTeX
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


def confidence_interval(data, confidence_level, loc=None):
    """
    The frequentist confidence interval for a tests statistic t = (mean - theta)/std
    from data that are Normally distributed. This is modeled using a Student's
    t-distribution with n-1 degrees of freedom.

    Args:
        data (Array of Floats): Sampled observations of the Normally distributed data
        confidence_level (Float): The 100*(1-alpha)% confidence level of the confidence interval (e.g., 0.95)

    Returns:
        Array of Floats: The 100*(1-alpha)% confidence level confidence interval from the data
    """
    if loc is None:
        loc = np.mean(data)

    t_dist = st.t(len(data) - 1, loc=loc, scale=st.sem(data))
    return t_dist.interval(confidence_level)


def plot_confidence_belt(pdf, confidence_level, sample_size=100, fontsize=14):
    np.random.seed(0)
    fig, ax = plt.subplots(1, 1)

    true_mean = pdf.mean()
    true_std = pdf.std()
    data = pdf.rvs(size=sample_size)
    theta_range = np.linspace(true_mean - 2 * true_std, true_mean + 2 * true_std, 100)

    confidence_belt = np.array(
        [
            confidence_interval(data, confidence_level, loc=theta)
            for theta in theta_range
        ]
    )

    observation = pdf.rvs(size=int(sample_size / 2.0)).mean()
    paramter_confidence_interval = theta_range[
        np.where(
            np.logical_and(
                confidence_belt[:, 0] <= observation,
                confidence_belt[:, 1] >= observation,
            )
        )
    ]
    paramter_confidence_interval = np.array(
        [paramter_confidence_interval[0], paramter_confidence_interval[-1]]
    )

    # Plot confidence belt
    for theta, interval in zip(theta_range, confidence_belt):
        ax.hlines(theta, *interval)

    # Plot observation line and confidence interval lines
    ax.axvline(observation, color='red')

    obs_frac_distance = [
        np.linalg.norm(observation - a) / np.linalg.norm(a - b)
        for a, b in [ax.get_xlim()]
    ][0]

    for height in [
        paramter_confidence_interval.min(),
        paramter_confidence_interval.max(),
    ]:
        ax.axhline(y=height, xmax=obs_frac_distance, color='blue', linestyle='--')

    ax.set_xlabel(r'test statistic $t$', fontsize=fontsize)
    ax.set_ylabel(r'paramter value $\theta$', fontsize=fontsize)

    return fig


def plot_confidence_intervals(
    pdf, confidence_level, n_samples=25, sample_size=100, fontsize=14
):
    np.random.seed(0)
    figsize = (6.4, 4.8)
    if n_samples > 50:
        figsize = (figsize[0] * 2.5, figsize[1] * 1.4)

    fig, ax = plt.subplots(1, 1, figsize=figsize)

    true_mean = pdf.mean()

    samples = np.array([pdf.rvs(size=sample_size) for _ in range(n_samples)])
    means = [sample.mean() for sample in samples]
    confidence_intervals = np.array(
        [confidence_interval(sample, confidence_level) for sample in samples]
    )

    outside_intervals = np.where(
        np.logical_or(
            confidence_intervals[:, 0] > true_mean,
            confidence_intervals[:, 1] < true_mean,
        )
    )

    x = np.arange(1, n_samples + 1)
    colors = [
        'red' if sample in samples[outside_intervals] else 'black' for sample in samples
    ]
    # point estimates
    for index, mean, color in zip(x, means, colors):
        ax.scatter(index, mean, color=color, zorder=3)
    # interval estimates
    for index, interval, color in zip(x, confidence_intervals, colors):
        ax.vlines(index, *interval, color=color, zorder=2)
    # true value
    ax.axhline(
        y=true_mean,
        color='blue',
        linestyle='--',
        label=r'true value $\theta$',
        zorder=1,
    )

    ax.legend(loc='best', frameon=False, fontsize=fontsize)

    ax.set_xlabel(r'measurement number', fontsize=fontsize)
    ax.set_ylabel(r'measurement value', fontsize=fontsize)

    return fig


def main():
    np.random.seed(0)

    true_mean = 0.1
    true_std = 1.2
    normal_dist = st.norm(loc=true_mean, scale=true_std)

    confidence_belt_plot = plot_confidence_belt(normal_dist, 0.95, sample_size=100)
    confidence_interval_plot = plot_confidence_intervals(
        normal_dist, 0.95, n_samples=100, sample_size=45, fontsize=20
    )
    image_write_path = 'figures/preface/'
    extensions = ['pdf', 'png', 'eps']
    for ext in extensions:
        confidence_belt_plot.savefig(f'{image_write_path}confidence_belt.{ext}')
        confidence_interval_plot.savefig(
            f'{image_write_path}confidence_intervals.{ext}'
        )


if __name__ == '__main__':
    main()
