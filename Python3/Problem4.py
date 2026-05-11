def isPalindrome(n):
    text = str(n)
    return text == text[::-1]


def largestPalindromeProduct(digits):
    high = 10 ** digits - 1
    low = 10 ** (digits - 1)
    largest = 0

    for first in range(high, low - 1, -1):
        if first * high < largest:
            break
        for second in range(first, low - 1, -1):
            product = first * second
            if product <= largest:
                break
            if isPalindrome(product):
                largest = product

    return largest


def runTests():
    assert isPalindrome(9009)
    assert not isPalindrome(9010)
    assert largestPalindromeProduct(2) == 9009


def solve():
    return largestPalindromeProduct(3)


if __name__ == "__main__":
    runTests()
    print(solve())
