from array import array
import time


MOD = 1_001_961_001
TARGET_N = 12_345_678


def qPrime(p):
    p2 = p * p % MOD
    p3 = p2 * p % MOD
    p4 = p3 * p % MOD
    p7 = p4 * p3 % MOD
    return (p7 + p4 - p3) % MOD


def Q(limit):
    smallestPrime = array("I", [0]) * (limit + 1)
    primePower = array("I", [0]) * (limit + 1)
    qPrimePower = array("I", [0]) * (limit + 1)
    fourthPower = array("I", [0]) * (limit + 1)
    qValue = array("I", [0]) * (limit + 1)

    primes = []
    qValue[1] = 1
    total = 1

    for n in range(2, limit + 1):
        if smallestPrime[n] == 0:
            smallestPrime[n] = n
            primes.append(n)

            primePower[n] = n
            fourthPower[n] = pow(n, 4, MOD)
            qPrimePower[n] = qPrime(n) if n != 2 else 128
            qValue[n] = qPrimePower[n]
        else:
            p = smallestPrime[n]
            m = n // p

            if m % p == 0:
                primePower[n] = primePower[m] * p
                fourthPower[n] = fourthPower[m] * pow(p, 4, MOD) % MOD

                if p == 2:
                    qPrimePower[n] = (
                        128 * qPrimePower[m]
                        + 128 * fourthPower[m]
                    ) % MOD
                else:
                    p2 = p * p % MOD
                    p3 = p2 * p % MOD
                    p7 = pow(p, 7, MOD)
                    term = fourthPower[m] * p3 % MOD * (p - 1) % MOD
                    qPrimePower[n] = (p7 * qPrimePower[m] + term) % MOD

                qValue[n] = qValue[m // primePower[m]] * qPrimePower[n] % MOD
            else:
                primePower[n] = p
                fourthPower[n] = pow(p, 4, MOD)
                qPrimePower[n] = qPrimePower[p]
                qValue[n] = qValue[m] * qPrimePower[n] % MOD

        total = (total + qValue[n]) % MOD

        for p in primes:
            composite = n * p
            if composite > limit:
                break
            smallestPrime[composite] = p
            if p == smallestPrime[n]:
                break

    return total


def runTests():
    assert qPrime(3) == 2241
    assert Q(4) == 20_802
    assert Q(10) == 18_573_381


def solve():
    return Q(TARGET_N)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
