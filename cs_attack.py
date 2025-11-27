import numpy as np
import math

def P2(x, q, k):
    """
    Implements P2(x in Z_q^n, q): outputs (2^0 * x, 2^1 * x, ..., 2^{k-1} * x) in Z_q^{n*k}.
    
    Parameters
    ----------
    x : array_like
        1D length-n integer vector, or 2D matrix of shape (m, n) for batch.
    q : int
        Modulus (must be positive).
    k : int
        Number of power-of-two scalings (k >= 1).
    
    Returns
    -------
    np.ndarray
        If x is 1D (shape (n,)), returns shape (n*k,).
        If x is 2D (shape (m, n)), returns shape (m, n*k),
        formed by concatenating blocks [2^0*x, 2^1*x, ..., 2^{k-1}*x] along the last axis,
        all reduced mod q.
    """
    if q <= 0:
        raise ValueError("q must be a positive modulus.")
    if k < 1:
        raise ValueError("k must be at least 1.")

    x = np.asarray(x)
    if x.ndim == 1:
        # Vector case
        x_mod = x % q
        blocks = []
        for i in range(k):
            coeff = pow(2, i, q)  # compute 2^i mod q safely
            blocks.append((coeff * x_mod) % q)
        return np.concatenate(blocks, axis=0)

    elif x.ndim == 2:
        # Batch matrix case: row-wise concatenation of scaled blocks
        x_mod = x % q
        blocks = []
        for i in range(k):
            coeff = pow(2, i, q)
            blocks.append((coeff * x_mod) % q)
        return np.concatenate(blocks, axis=1)

    else:
        raise ValueError("x must be a 1D vector or a 2D matrix.")

def recover_pth_secret(res, p, q):
    k = int(math.log2(q))
    bits = []
    for i in range(k):
        v = res[k - i - 1][p]
        for j in range(i):
            v -= bits[j] * (2 ** (k - i - 1 + j))
        v %= q
        rp = v % (2 ** (k - 1))
        r = rp if rp < 2 ** (k - 2) else rp - 2 ** (k - 1)
        if (v - r) % q == 0:
            bits.append(0)
        else:
            bits.append(1)
    value = sum(bits[i] * (2 ** i) for i in range(len(bits)))
    if value >= 2 ** (k - 1):
        value -= 2 ** k
    return bits, value

def recover_secret(res, q):
    secret = []
    for p in range(res.shape[1]):
        bits, value = recover_pth_secret(res, p, q)
        secret.append((bits, value))
    return secret