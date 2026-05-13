import math
import time


LIMIT = 110000000


def cardanoTripletCount(limit):
    result = 0
    max_q = math.isqrt(((limit + 1) * 8 // 3 - 3) // 5) + 5
    max_p = math.isqrt((limit + 1) // 5) + 5

    for q in range(1, max_q + 1, 2):
        q2 = q * q
        q3 = q2 * q

        for p in range(1, max_p + 1):
            if 3 * q2 + 8 * p * p + 8 * q > 8 * limit - 1:
                break
            if math.gcd(p, q) != 1:
                continue

            modulus = 8 * p
            m = (-3 * pow(q2 % modulus, -1, modulus)) % modulus
            g = (q2 * m + 3) // modulus

            base_sum = g * q + m * p * p + 3 * g * p
            if base_sum <= limit + 1:
                period_sum = q3 + 3 * p * q2 + 8 * p * p * p
                result += (limit + 1 - base_sum) // period_sum + 1

    return result


def bruteCardanoTripletCount(limit):
    result = 0

    for k in range((limit - 2) // 3 + 1):
        a = 3 * k + 2
        value = (k + 1) * (k + 1) * (8 * k + 5)

        for b in range(1, limit - a):
            square = b * b
            if value % square == 0:
                c = value // square
                if a + b + c <= limit:
                    result += 1

    return result


def runTests():
    assert cardanoTripletCount(100) == bruteCardanoTripletCount(100)
    assert cardanoTripletCount(1000) == 149


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = cardanoTripletCount(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
