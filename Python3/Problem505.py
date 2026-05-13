import functools
import time


MODULUS = 2 ** 60
MASK = MODULUS - 1


def childValues(value, parent):
    leftValue = (3 * value + 2 * parent) & MASK
    rightValue = (2 * value + 3 * parent) & MASK
    return leftValue, rightValue


def x(k):
    if k == 0:
        return 0

    value = 1
    parent = 0

    for bit in bin(k)[3:]:
        leftValue, rightValue = childValues(value, parent)
        value, parent = (leftValue, value) if bit == "0" else (rightValue, value)

    return value


def bidirectionalA(n):
    mask = MASK
    modulus = MODULUS

    def evaluate(k, value, parent, isMaxNode, alpha, beta):
        if k >= n:
            return mask - value if isMaxNode else value

        leftValue = (3 * value + 2 * parent) & mask
        rightValue = (2 * value + 3 * parent) & mask
        leftChild = k << 1
        rightChild = leftChild + 1

        if isMaxNode:
            best = evaluate(rightChild, rightValue, value, False, alpha, beta)
            if best > alpha:
                alpha = best
            if alpha >= beta:
                return best

            other = evaluate(leftChild, leftValue, value, False, alpha, beta)
            return best if best >= other else other

        best = evaluate(rightChild, rightValue, value, True, alpha, beta)
        if best < beta:
            beta = best
        if alpha >= beta:
            return best

        other = evaluate(leftChild, leftValue, value, True, alpha, beta)
        return best if best <= other else other

    return evaluate(1, 1, 0, False, -1, modulus)


def _aSmall(n):
    @functools.lru_cache(None)
    def y(k):
        if k >= n:
            return x(k)
        return MASK - max(y(2 * k), y(2 * k + 1))

    return y(1)


def runTests():
    assert x(2) == 3
    assert x(3) == 2
    assert x(4) == 11
    assert bidirectionalA(4) == 8
    assert bidirectionalA(10) == MODULUS - 34
    assert bidirectionalA(10 ** 3) == 101_881
    assert bidirectionalA(100) == _aSmall(100)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = bidirectionalA(10 ** 12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
