#!/usr/bin/env python3
import numpy as np


def lorentz_factor(p, m):
    """
    Calculate the Lorentz factor for the proton beam given its kinetic energy
    (the beam energy) and the proton mass.

    p^2 = (gamma^2 - 1) m^2

    so

    gamma = sqrt(1 + (p/m)^2)

    Args:
        p (Float): The beam energy
        m (Float): The mass of the particle

    Returns:
        Float: The Lorentz factor (gamma)
    """
    return np.sqrt(1.0 + np.square(p / m))


def geometric_reduction_factor(theta_c, sigma_z, sigma_star):
    """
    Calculate the geometric luminosity reduction factor at the interaction point

    Args:
        theta_c (Float): The Full crossing angle (radians)
        sigma_z (Float): The RMS bunch length (meters)
        sigma_star (Float): The Transverse RMS beams size (meters)

    Returns:
        Float: The geometric luminosity reduction factor
    """
    return 1.0 / np.sqrt(1 + (theta_c * sigma_z / (2 * sigma_star)))


def machine_luminosity(N_b, n_b, frequency, gamma, epsilon, beta_star, F):
    ratio = np.prod([np.square(N_b), n_b, frequency, gamma]) / np.prod(
        [4, np.pi, epsilon, beta_star]
    )
    SI_luminosity = ratio * F
    return SI_luminosity * 1e-4  # cm^-2


def main():
    # Using design LHC values
    beam_energy = 7 * 1e3  # GeV
    proton_mass = 0.938  # GeV
    N_b = 1.15 * 1e11
    n_b = 2808
    frequency = 11.245 * 1e3  # Hz
    epsilon = 3.75 * 1e-6  # meters
    beta_star = 0.55  # meters
    theta_c = 285 * 1e-6  # radians
    sigma_z = 7.55 * 1e-2  # meters
    sigma_star = 16.6 * 1e-6  # meters

    F = geometric_reduction_factor(theta_c, sigma_z, sigma_star)
    gamma = lorentz_factor(beam_energy, proton_mass)

    accelerator_lumi = machine_luminosity(
        N_b, n_b, frequency, gamma, epsilon, beta_star, F
    )
    barns_lumi = accelerator_lumi * 1e-33  # nb^-1
    print('\nDesign machine luminosity:')
    print(f'{accelerator_lumi:.3e} cm^-2*s^-1')
    print(f'{barns_lumi:.3f} nb^-1*s^-1')


if __name__ == '__main__':
    main()
