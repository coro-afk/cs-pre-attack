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