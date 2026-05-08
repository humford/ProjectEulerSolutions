import time


def properDivisorSums(limit):
    sums = [0] * limit

    for divisor in range(1, limit // 2 + 1):
        for multiple in range(2 * divisor, limit, divisor):
            sums[multiple] += divisor

    return sums


def smallestMemberLongestAmicableChain(limit):
    divisor_sums = properDivisorSums(limit)
    processed = [False] * limit
    best_chain = []

    for start in range(2, limit):
        if processed[start]:
            continue

        seen = {}
        sequence = []
        current = start

        while 0 < current < limit and current not in seen and not processed[current]:
            seen[current] = len(sequence)
            sequence.append(current)
            current = divisor_sums[current]

        if current in seen:
            chain = sequence[seen[current] :]
            if len(chain) > len(best_chain):
                best_chain = chain

        for value in sequence:
            processed[value] = True

    return min(best_chain)


def runTests():
    divisor_sums = properDivisorSums(300)
    assert divisor_sums[220] == 284
    assert divisor_sums[284] == 220
    assert smallestMemberLongestAmicableChain(300) == 220


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = smallestMemberLongestAmicableChain(1000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
