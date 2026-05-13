import bisect
import time


LIMIT = 10**17


def fibonacciNumbers(limit):
    numbers = [1, 2]

    while numbers[-1] <= limit:
        numbers.append(numbers[-1] + numbers[-2])

    return numbers


def zeckendorfPrefixSums(fibonacci):
    prefix = [0] * len(fibonacci)
    prefix[1] = 1

    for index in range(2, len(fibonacci)):
        prefix[index] = prefix[index - 1] + prefix[index - 2] + fibonacci[index - 2]

    return prefix


def zeckendorfSum(limit):
    fibonacci = fibonacciNumbers(limit)
    prefix = zeckendorfPrefixSums(fibonacci)

    def search(bound):
        if bound <= 1:
            return 0

        index = bisect.bisect_right(fibonacci, bound - 1) - 1
        remainder = bound - fibonacci[index]

        return prefix[index] + remainder + search(remainder)

    return search(limit)


def runTests():
    assert zeckendorfSum(10**6) == 7894453


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = zeckendorfSum(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
