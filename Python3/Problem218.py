import time


def everyPerfectTriangleIsSuperPerfect():
    modulus = 42

    for x in range(modulus):
        for y in range(modulus):
            odd_leg = x * x - y * y
            even_leg = 2 * x * y
            area_factor = (odd_leg * odd_leg - even_leg * even_leg) * odd_leg * x * y

            if area_factor % modulus != 0:
                return False

    return True


def nonSuperPerfectCount(_hypotenuse_limit):
    if everyPerfectTriangleIsSuperPerfect():
        return 0

    raise RuntimeError("modular proof failed")


def runTests():
    assert everyPerfectTriangleIsSuperPerfect()
    assert nonSuperPerfectCount(10 ** 4) == 0


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = nonSuperPerfectCount(10 ** 16)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
