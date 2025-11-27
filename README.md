# Collusion attack to proxy re-encryption
This repository provides Python demo of attack explained in paper [Collusion-Safe Proxy Re-Encryption](https://eprint.iacr.org/2025/1423.pdf) .
This is a collusion attack to a lattice-based proxy re-encryption scheme:
Given Bob's secret key and re-encryption key, the adversary can compute Alice's secret key.

Key components:
- Toy **Discrete Gaussian Sampler**: Generates matrices with entries sampled from a discrete Gaussian distribution.
- Toy **Proxy Re-Encryption Algorithms**: Simulates setups, extraction, and re-encryption key generation.
- **Random Matrix Generator**: Creates uniform random matrices over Z_q.
- **P2 Gadget Function**: Expands a vector into its power-of-two scaled representation for gadget-based constructions.
- **Recovery Algorithm**: Recovers secret key bits from scaled noisy samples.

## Installation
Ensure you have Python 3 and NumPy installed:
```bash
pip install numpy
```

## Usage Example
```python
from simple_mp12 import discrete_gaussian_sampler_matrix, random_matrix
from cs_attack import P2, recover_secret


if __name__ == "__main__":
    # demo parameters
    k = 10
    n, m, q = 4, 8, 2**k
    sigma = 3.2

    # direct generate Bob's public key matrix
    Ab = random_matrix(n, m, q)
    
    # sample the desired secret key first
    ska = discrete_gaussian_sampler_matrix(m, 1, sigma).flatten()
    skb = discrete_gaussian_sampler_matrix(m, 1, sigma).flatten()
    
    
    print("\n------------------------------ Before Attack ------------------------------\n")
    print(f"Alice's secret key: {ska}\n")
    print(f"Bob's secret key: {skb}\n")
    
    # then generate another part of public key u (similar to some proof techniques)
    u = Ab @ skb % q
    
    # sample the randomness for re-encryption key generation
    R1 = discrete_gaussian_sampler_matrix(m * k, n, sigma)
    r_2 = discrete_gaussian_sampler_matrix(m * k, 1, sigma).flatten()
    
    # compute the P2 of the secret key
    skp2 = P2(ska, q, k)

    # compute the re-encryption key components
    rk1 = R1 @ Ab % q
    rk2 = (R1 @ u + r_2 - skp2) % q
    
    print(f"Re-encryption key rk1 shape: {rk1.shape}, rk2 shape: {rk2.shape}\n")

    print("------------------------------ After Attack ------------------------------\n")

    # compute the main result by applying ``decryption'' to the re-encryption key
    res = (rk1 @ skb - rk2) % q
    res = res.reshape(k, m)  # reshape to (k, m) for easier processing
    
    print(f"Result after applying ``decryption'' to (rk1, rk2) using Bob's secret key: \n{res}\n")
        
    recovered_secrets = recover_secret(res, q)
    print("Recovered secrets:")
    for i, (bits, value) in enumerate(recovered_secrets):
        print(f"Secret {i}: bits = {bits[::-1]}, value = {value}, ska{ i } = {ska[i]}")
    
    attack_success = all(value == ska[i] for i, (_, value) in enumerate(recovered_secrets))
    print(f"\nAttack success: {attack_success}")
    
    print("\n-------------------------------------------------------------------------\n")
```

## Example output
```
------------------------------ Before Attack ------------------------------

Alice's secret key: [ 5 -4  0  3  2  6  1  3]

Bob's secret key: [-1  6  5 -4  5  8 -2  6]

Re-encryption key rk1 shape: (80, 8), rk2 shape: (80,)

------------------------------ After Attack ------------------------------

Result after applying ``decryption'' to (rk1, rk2) using Bob's secret key: 
[[   1 1021    0    4    4    6    0    5]
 [   8 1017    0    9    0   10    2    5]
 [  18 1011    1    6   13   25    0   12]
 [  40  985 1022   27   13   51    7   23]
 [  78  959    3   51   31   97   18   52]
 [ 164  893 1023   96   61  195   38  102]
 [ 323  763    2  192  129  380   67  186]
 [ 640  514    2  387  251  768  132  386]
 [ 266    7    0  768  513  515  255  770]
 [ 510    3 1020  513    6 1021  516  511]]

Recovered secrets:
Secret 0: bits = [0, 0, 0, 0, 0, 0, 0, 1, 0, 1], value = 5, ska0 = 5
Secret 1: bits = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0], value = -4, ska1 = -4
Secret 2: bits = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], value = 0, ska2 = 0
Secret 3: bits = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1], value = 3, ska3 = 3
Secret 4: bits = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], value = 2, ska4 = 2
Secret 5: bits = [0, 0, 0, 0, 0, 0, 0, 1, 1, 0], value = 6, ska5 = 6
Secret 6: bits = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], value = 1, ska6 = 1
Secret 7: bits = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1], value = 3, ska7 = 3

Attack success: True

-------------------------------------------------------------------------
```
## Credits
This project was developed with assistance from **Microsoft Copilot**, which provided algorithmic guidance and code generation support.

## License
[MIT License](LICENSE)
