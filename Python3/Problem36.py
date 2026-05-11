def isPalindrome(text):
    return text == text[::-1]


def isDoubleBasePalindrome(n):
    return isPalindrome(str(n)) and isPalindrome(bin(n)[2:])


def sumDoubleBasePalindromes(limit):
    return sum(value for value in range(1, limit) if isDoubleBasePalindrome(value))


def runTests():
    assert isDoubleBasePalindrome(585)
    assert sumDoubleBasePalindromes(1000) == 1772


def solve():
    return sumDoubleBasePalindromes(1000000)


if __name__ == "__main__":
    runTests()
    print(solve())
