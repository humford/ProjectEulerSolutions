import time


MOD = 998_244_353
DIGITS = 10
NONZERO_DIGITS = 9


def triplicateWordsByBlocks(blocks, modulus=MOD):
    sideBranches = DIGITS - 1
    firstReturn = [0] * (blocks + 1)
    sideLoop = [0] * (blocks + 1)
    sideLoop[0] = 1

    for n in range(1, blocks + 1):
        total = 0
        for i in range(n):
            total += sideLoop[i] * sideLoop[n - 1 - i]
        firstReturn[n] = total % modulus

        total = 0
        for i in range(1, n + 1):
            total += firstReturn[i] * sideLoop[n - i]
        sideLoop[n] = sideBranches * total % modulus

    f = [0] * (blocks + 1)
    f[0] = 1
    for n in range(1, blocks + 1):
        total = 0
        for i in range(1, n + 1):
            total += firstReturn[i] * f[n - i]
        f[n] = DIGITS * total % modulus

    return f


def T(n, modulus=MOD):
    blocks = n // 3
    identityWords = triplicateWordsByBlocks(blocks, modulus)
    allTriplicateStrings = sum(identityWords[1:]) % modulus
    return allTriplicateStrings * NONZERO_DIGITS * pow(DIGITS, -1, modulus) % modulus


def reducesToEmpty(digits):
    stack = []
    for digit in digits:
        if len(stack) >= 2 and stack[-1] == digit and stack[-2] == digit:
            stack.pop()
            stack.pop()
        else:
            stack.append(digit)
    return not stack


def bruteT(n):
    total = 0

    def search(length, prefix):
        nonlocal total
        if len(prefix) == length:
            if reducesToEmpty(prefix):
                total += 1
            return

        start = 1 if not prefix else 0
        for digit in range(start, 10):
            search(length, prefix + [digit])

    for length in range(1, n + 1):
        search(length, [])

    return total


def runTests():
    assert reducesToEmpty([1, 2, 2, 5, 5, 5, 2, 1, 1])
    assert not reducesToEmpty([6, 6, 3, 6, 3, 3])
    assert not reducesToEmpty([9, 9, 9, 0])
    assert bruteT(6) == 261
    assert T(6) == 261
    assert T(30) == 5_576_195_181_577_716 % MOD


def solve():
    return T(10**4)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
