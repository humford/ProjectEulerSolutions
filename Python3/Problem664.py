import math
import time


PHI = (1 + math.sqrt(5)) / 2
LOG_PHI = math.log(PHI)


def logWeightedColumnSum(power, cutoff):
    peak = max(1, round(power / LOG_PHI))

    def logTerm(column):
        return power * math.log(column) - column * LOG_PHI

    peakLog = max(logTerm(peak - 1), logTerm(peak), logTerm(peak + 1))

    total = 0
    column = peak
    while column >= 1:
        term = logTerm(column) - peakLog
        if term < -cutoff:
            break
        total += math.exp(term)
        column -= 1

    column = peak + 1
    while True:
        term = logTerm(column) - peakLog
        if term < -cutoff:
            break
        total += math.exp(term)
        column += 1

    return peakLog + math.log(total)


def infiniteGameDistance(power):
    if power == 0:
        return 4

    distances = []
    for cutoff in [70, 90, 110]:
        resourceLog = logWeightedColumnSum(power, cutoff)
        distances.append(math.ceil(3 + resourceLog / LOG_PHI))

    if len(set(distances)) != 1:
        raise ArithmeticError("unstable pagoda-bound computation")
    return distances[0]


def runTests():
    assert infiniteGameDistance(0) == 4
    assert infiniteGameDistance(1) == 6
    assert infiniteGameDistance(2) == 9
    assert infiniteGameDistance(3) == 13
    assert infiniteGameDistance(11) == 58
    assert infiniteGameDistance(123) == 1_173


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = infiniteGameDistance(1_234_567)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
