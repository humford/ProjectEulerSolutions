import time


A = (
    "14159265358979323846264338327950288419716939937510"
    "58209749445923078164062862089986280348253421170679"
)
B = (
    "82148086513282306647093844609550582231725359408128"
    "48111745028410270193852110555964462294895493038196"
)


def fibonacciLengths(block_size, limit):
    lengths = [block_size, block_size]
    while lengths[-1] < limit:
        lengths.append(lengths[-2] + lengths[-1])
    return lengths


def digit(index, first, second):
    lengths = fibonacciLengths(len(first), index)
    word = len(lengths) - 1
    index -= 1

    while word >= 2:
        left_length = lengths[word - 2]
        if index < left_length:
            word -= 2
        else:
            index -= left_length
            word -= 1

    source = first if word == 0 else second
    return int(source[index])


def fibonacciWordSum():
    total = 0
    for n in range(18):
        total += (10 ** n) * digit((127 + 19 * n) * (7 ** n), A, B)
    return total


def runTests():
    assert digit(35, "1415926535", "8979323846") == 9


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = fibonacciWordSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
