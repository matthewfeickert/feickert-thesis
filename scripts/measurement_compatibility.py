#!/usr/bin/env python3
import numpy as np


def total_uncertainty(stat_uncert, syst_uncert, theory_uncert):
    """
    The total quadratic uncertainty
    """

    def up_and_down(uncert):
        if not isinstance(uncert, (list, np.ndarray)):
            uncert = np.tile(uncert, 2)
        return uncert

    total_uncert = np.sqrt(
        np.square(up_and_down(stat_uncert))
        + np.square(up_and_down(syst_uncert))
        + np.square(up_and_down(theory_uncert))
    )
    return total_uncert


def z_score(point_estimate, accepted_value, uncertainty):
    """
    The z-score of how far a point estimate is from an accepted value
    z = (estimate - accepted)/uncertainty

    Args:
        point_estimate (Float): The point estimator of the parameter (best-fit value)
        accepted_value (Float): The accepted value of the parameter (SM prediction)
        uncertainty (Float or Array): The associated 1sigma totat uncertainty

    Returns:
        Float: The number of Normal standard deviations the point estimate differs from the accepted
    """
    if not isinstance(uncertainty, (list, np.ndarray)):
        uncert = uncertainty
    else:
        if point_estimate > accepted_value:
            uncert = uncertainty[0]
        else:
            uncert = uncertainty[1]
    return (point_estimate - accepted_value) / uncert


def main():
    Vjets_best_fit = 1.5
    Vjets_uncertainty = total_uncertainty(0.22, [0.25, 0.29], 0.18)
    Higgs_best_fit = 5.8
    Higgs_uncertainty = total_uncertainty(3.1, 1.9, 1.7)

    print(
        f'V+jets best-fit value compatibility with SM: {z_score(Vjets_best_fit, 1, Vjets_uncertainty):.2f} sigma'
    )
    print(
        f'Higgs best-fit value compatibility with SM: {z_score(Higgs_best_fit, 1, Higgs_uncertainty):.2f} sigma'
    )


if __name__ == '__main__':
    main()
