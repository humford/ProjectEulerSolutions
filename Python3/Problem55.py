def isPalindrome(n):
    text = str(n)
    return text == text[::-1]


def reverseAndAdd(n):
    return n + int(str(n)[::-1])


def isLychrel(n, iterations=50):
    for _ in range(iterations):
        n = reverseAndAdd(n)
        if isPalindrome(n):
            return False
    return True


def lychrelCountBelow(limit):
    return sum(1 for value in range(1, limit) if isLychrel(value))


def runTests():
    assert reverseAndAdd(47) == 121
    assert not isLychrel(47)
    assert not isLychrel(349)


def solve():
    return lychrelCountBelow(10000)


if __name__ == "__main__":
    runTests()
    print(solve())
