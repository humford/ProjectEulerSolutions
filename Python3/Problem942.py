import time


TARGET_Q = 74_207_281
MODULUS = 1_000_000_007


def quadraticResiduePowerSum(q, modulus):
    residues = bytearray(q)
    residue = 1
    increment = 3

    for _ in range((q - 1) // 2):
        residues[residue] = 1
        residue += increment
        if residue >= q:
            residue -= q
        increment += 2

    total = 0
    power = 2 % modulus
    for exponent in range(1, q):
        if residues[exponent]:
            total += power
        power += power
        if power >= modulus:
            power -= modulus

    return total % modulus


def gaussRootMod(q, modulus):
    residuePowerSum = quadraticResiduePowerSum(q, modulus)
    allPowerSum = (pow(2, q, modulus) - 2) % modulus
    return (2 * residuePowerSum - allPowerSum) % modulus


def R(q, modulus):
    """Return the minimal square root of q modulo 2**q - 1, reduced by modulus."""
    if q % 4 != 1:
        raise ValueError("This Gauss-sum square root is real only for q == 1 mod 4.")

    root = gaussRootMod(q, modulus)
    if q % 8 == 1:
        mersenne = (pow(2, q, modulus) - 1) % modulus
        return (mersenne - root) % modulus

    return root


def solve():
    return R(TARGET_Q, MODULUS)


def runTests():
    assert R(5, 2**5 - 1) == 6
    assert R(17, 2**17 - 1) == 47_569


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
