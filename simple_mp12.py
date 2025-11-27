import numpy as np
import math

def discrete_gaussian_sampler_matrix(rows, cols, sigma, center=None, tailcut=13):
    """
    Generate a `rows` x `cols` matrix where each entry follows the discrete Gaussian distribution D_{Z, sigma}.

    Parameters:
        rows (int): Number of rows
        cols (int): Number of columns
        sigma (float): Standard deviation
        center (ndarray): Optional center matrix (default is zero matrix)
        tailcut (int): Truncation multiplier for sigma (default = 13)

    Returns:
        ndarray: rows x cols matrix of sampled integers
    """
    if center is None:
        center = np.zeros((rows, cols))

    # Precompute 1D CDF table
    bound = int(math.ceil(tailcut * sigma))
    x_vals = np.arange(-bound, bound + 1)
    probs = np.exp(-((x_vals) ** 2) / (2 * sigma ** 2))
    probs /= probs.sum()  # Normalize
    cdf = np.cumsum(probs)

    # Generate rows x cols matrix
    samples = np.zeros((rows, cols), dtype=int)
    random_matrix = np.random.rand(rows, cols)

    # Map random values to discrete Gaussian samples
    for i in range(rows):
        for j in range(cols):
            u = random_matrix[i, j]
            idx = np.searchsorted(cdf, u)
            samples[i, j] = x_vals[idx] + int(center[i, j])

    return samples

def random_matrix(rows, cols, q):
    """
    Generate a `rows` x `cols` matrix with entries uniformly sampled from Z_q.

    Parameters:
        rows (int): Number of rows
        cols (int): Number of columns
        q (int): Modulus
    Returns:
        ndarray: rows x cols matrix with entries in Z_q
    """
    return np.random.randint(0, q, size=(rows, cols))