import math
import time


def isPalindrome(n):
    text = str(n)
    return text == text[::-1]


def palindromicSquareSumTotal(limit):
    squares = [n * n for n in range(1, math.isqrt(limit) + 1)]
    palindromes = set()

    for start in range(len(squares)):
        total = 0
        for end in range(start, len(squares)):
            total += squares[end]
            if total >= limit:
                break
            if end > start and isPalindrome(total):
                palindromes.add(total)

    return sum(palindromes)


def runTests():
    assert palindromicSquareSumTotal(1000) == 4164


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = palindromicSquareSumTotal(10 ** 8)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
