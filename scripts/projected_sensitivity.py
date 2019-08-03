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

    uncertainties = [stat_uncert, syst_uncert, theory_uncert]

    if syst_uncert is None:
        uncertainties = [stat_uncert, theory_uncert]
    if theory_uncert is None:
        uncertainties = uncertainties[:-1]

    total_uncert = np.sqrt(
        np.sum([np.square(up_and_down(uncert)) for uncert in uncertainties], axis=0)
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


def weighted_signal_strength(signal_strength, luminosity):
    fractional_weights = np.array(luminosity) / np.sum(luminosity)
    return np.sum(np.prod([fractional_weights, signal_strength], axis=0))


def weighted_uncertainty(uncertainty, luminosity):
    fractional_weights = np.array(luminosity) / np.sum(luminosity)
    return np.sqrt(
        np.sum(np.square(np.prod([fractional_weights, uncertainty], axis=0)))
    )


def lumi_weighted_uncertainty(observations, luminosity_scale_factor):
    total_uncertainty_ATLAS = total_uncertainty(
        3.1 / np.sqrt(luminosity_scale_factor), 1.9, 1.7
    )
    total_uncertainty_down_CMS = total_uncertainty(
        1.5 / np.sqrt(luminosity_scale_factor), 0.4, None
    )
    total_uncertainty_up_CMS = total_uncertainty(
        1.5 / np.sqrt(luminosity_scale_factor), 1.0, None
    )
    weighted_uncert = [
        weighted_uncertainty(
            [total_uncertainty_ATLAS[0], total_uncertainty_down_CMS[0]],
            [observations["ATLAS"]["luminosity"], observations["CMS"]["luminosity"]],
        ),
        weighted_uncertainty(
            [total_uncertainty_ATLAS[1], total_uncertainty_up_CMS[0]],
            [observations["ATLAS"]["luminosity"], observations["CMS"]["luminosity"]],
        ),
    ]
    return weighted_uncert


def lumi_weighted_stat_uncertainty(observations, luminosity_scale_factor):
    total_uncertainty_ATLAS = total_uncertainty(
        3.1 / np.sqrt(luminosity_scale_factor), None, None
    )
    total_uncertainty_down_CMS = total_uncertainty(
        1.5 / np.sqrt(luminosity_scale_factor), None, None
    )
    total_uncertainty_up_CMS = total_uncertainty(
        1.5 / np.sqrt(luminosity_scale_factor), None, None
    )
    weighted_uncert = [
        weighted_uncertainty(
            [total_uncertainty_ATLAS[0], total_uncertainty_down_CMS[0]],
            [observations["ATLAS"]["luminosity"], observations["CMS"]["luminosity"]],
        ),
        weighted_uncertainty(
            [total_uncertainty_ATLAS[1], total_uncertainty_up_CMS[0]],
            [observations["ATLAS"]["luminosity"], observations["CMS"]["luminosity"]],
        ),
    ]
    return weighted_uncert


def main():
    ATLAS = {
        "mu": 5.8,
        "uncert_down": total_uncertainty(3.1, 1.9, 1.7)[0],
        "uncert_up": total_uncertainty(3.1, 1.9, 1.7)[1],
        # Units of inverse femotbarns
        "luminosity": 80.5,
    }
    CMS = {
        "mu": 2.3,
        "uncert_down": total_uncertainty(1.5, 0.4, None)[0],
        "uncert_up": total_uncertainty(1.5, 1.0, None)[1],
        # Units of inverse femotbarns
        "luminosity": 35.9,
    }
    observations = {"ATLAS": ATLAS, "CMS": CMS}
    mean_lumi = np.average([ATLAS["luminosity"], CMS["luminosity"]])

    weighted_mu = weighted_signal_strength(
        [ATLAS["mu"], CMS["mu"]], [ATLAS["luminosity"], CMS["luminosity"]]
    )
    weighted_uncert = [
        weighted_uncertainty(
            [ATLAS["uncert_down"], CMS["uncert_down"]],
            [ATLAS["luminosity"], CMS["luminosity"]],
        ),
        weighted_uncertainty(
            [ATLAS["uncert_up"], CMS["uncert_up"]],
            [ATLAS["luminosity"], CMS["luminosity"]],
        ),
    ]
    luminosity = [mean_lumi, 140, 440, 3300]

    print(
        f"ATLAS Higgs best-fit value compatibility with SM: {z_score(ATLAS['mu'], 1, ATLAS['uncert_down']):.2f} sigma"
    )
    print('Improvements to statistical uncertainty only:\n')
    for lumi in luminosity:
        print(
            f"Combined Higgs best-fit value compatibility with SM (mu=1) at {lumi} ifb: {z_score(weighted_mu, 1, lumi_weighted_uncertainty(observations, lumi / mean_lumi)):.2f} sigma"
        )
        print(
            f"       Total Uncertainties: -{lumi_weighted_uncertainty(observations, lumi / mean_lumi)[0]:.2f}, +{lumi_weighted_uncertainty(observations, lumi / mean_lumi)[1]:.2f}"
        )
    print('\nUsing only statistical uncertainty:\n')
    for lumi in luminosity:
        print(
            f"Combined Higgs best-fit value compatibility with SM (mu=1) at {lumi} ifb: {z_score(weighted_mu, 1, lumi_weighted_stat_uncertainty(observations, lumi / mean_lumi)):.2f} sigma"
        )
        print(
            f"       Total Uncertainties: -{lumi_weighted_stat_uncertainty(observations, lumi / mean_lumi)[0]:.2f}, +{lumi_weighted_stat_uncertainty(observations, lumi / mean_lumi)[1]:.2f}"
        )


if __name__ == "__main__":
    main()
