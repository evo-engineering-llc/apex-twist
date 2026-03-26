import numpy as np

# ==========================================================
# Apex Twist Core Engine
# ==========================================================

def apex_field(width, height, phi=1.061, pi_=4.57):
    """
    Generate a deterministic field using Apex Twist formulation.

    Parameters:
        width (int): grid width
        height (int): grid height
        phi (float): horizontal modulation constant
        pi_ (float): vertical modulation constant

    Returns:
        np.ndarray: generated field (float64)
    """
    y, x = np.mgrid[0:height, 0:width]
    return np.sin(phi * x / width) * np.cos(pi_ * y / height)


def raster_field(width, height, phi=1.061, pi_=4.57):
    """
    Reference implementation using iterative raster computation.

    Used for comparison / benchmarking.
    """
    arr = np.zeros((height, width), dtype=np.float64)
    for y in range(height):
        for x in range(width):
            arr[y, x] = np.sin(phi * x / width) * np.cos(pi_ * y / height)
    return arr


def compare_fields(width, height, phi=1.061, pi_=4.57):
    """
    Generate both raster and Apex fields and return them.

    Returns:
        (raster, apex)
    """
    r = raster_field(width, height, phi, pi_)
    a = apex_field(width, height, phi, pi_)
    return r, a


def compute_error(a, b):
    """
    Compute absolute difference between two fields.
    """
    return np.abs(a - b)