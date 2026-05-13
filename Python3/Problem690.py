import time


MODULUS = 1_000_000_007
TARGET = 2_019


def partitionsUpTo(limit):
    partitions = [0] * (limit + 1)
    partitions[0] = 1
    for part in range(1, limit + 1):
        for total in range(part, limit + 1):
            partitions[total] += partitions[total - part]
            if partitions[total] >= MODULUS:
                partitions[total] -= MODULUS
    return partitions


def multiplySeries(first, second, limit):
    result = [0] * (limit + 1)
    cutoff = MODULUS * MODULUS
    for i, firstCoefficient in enumerate(first):
        if firstCoefficient == 0:
            continue
        maxJ = limit - i
        for j in range(maxJ + 1):
            result[i + j] += firstCoefficient * second[j]
            if result[i + j] >= cutoff:
                result[i + j] %= MODULUS
    for i in range(limit + 1):
        result[i] %= MODULUS
    return result


def invertSeries(series, limit):
    inverse = [0] * (limit + 1)
    inverseZero = pow(series[0], MODULUS - 2, MODULUS)
    inverse[0] = inverseZero
    cutoff = MODULUS * MODULUS

    for index in range(1, limit + 1):
        total = 0
        for k in range(1, index + 1):
            total += series[k] * inverse[index - k]
            if total >= cutoff:
                total %= MODULUS
        inverse[index] = (-total * inverseZero) % MODULUS

    return inverse


def lobsterTreeCounts(limit):
    partitions = partitionsUpTo(limit)
    inverseTwo = (MODULUS + 1) // 2

    partitionMinusGeometric = [
        (partitions[index] - 1) % MODULUS
        for index in range(limit + 1)
    ]

    numeratorOne = multiplySeries(
        partitionMinusGeometric,
        partitionMinusGeometric,
        limit,
    )
    denominatorOne = [0] * (limit + 1)
    denominatorOne[0] = 1
    for index in range(1, limit + 1):
        denominatorOne[index] = (-partitions[index - 1]) % MODULUS
    termOne = multiplySeries(numeratorOne, invertSeries(denominatorOne, limit), limit)

    partitionEven = [0] * (limit + 1)
    partitionEvenMinusGeometric = [0] * (limit + 1)
    for index in range(limit // 2 + 1):
        partitionEven[2 * index] = partitions[index]
        partitionEvenMinusGeometric[2 * index] = (partitions[index] - 1) % MODULUS

    onePlusXPartitions = [0] * (limit + 1)
    onePlusXPartitions[0] = 1
    for index in range(1, limit + 1):
        onePlusXPartitions[index] = partitions[index - 1]

    numeratorTwo = multiplySeries(
        partitionEvenMinusGeometric,
        onePlusXPartitions,
        limit,
    )
    denominatorTwo = [0] * (limit + 1)
    denominatorTwo[0] = 1
    for index in range(2, limit + 1):
        denominatorTwo[index] = (-partitionEven[index - 2]) % MODULUS
    termTwo = multiplySeries(numeratorTwo, invertSeries(denominatorTwo, limit), limit)

    combined = [
        (termOne[index] + termTwo[index]) % MODULUS
        for index in range(limit + 1)
    ]

    main = [0] * (limit + 1)
    for index in range(limit - 1):
        main[index + 2] = combined[index] * inverseTwo % MODULUS

    xPartitions = [0] * (limit + 1)
    for index in range(1, limit + 1):
        xPartitions[index] = partitions[index - 1]

    inverseOneMinusSquared = [(index + 1) % MODULUS for index in range(limit + 1)]
    inverseOnePlus = [
        1 if index % 2 == 0 else MODULUS - 1
        for index in range(limit + 1)
    ]
    rationalTail = multiplySeries(
        inverseOneMinusSquared,
        inverseOnePlus,
        limit,
    )
    shiftedTail = [0] * (limit + 1)
    for index in range(limit - 2):
        shiftedTail[index + 3] = rationalTail[index]

    return [
        (main[index] + xPartitions[index] - shiftedTail[index]) % MODULUS
        for index in range(limit + 1)
    ]


def eulerTransform(componentCounts, limit):
    exponents = [0] * (limit + 1)
    for divisor in range(1, limit + 1):
        count = componentCounts[divisor]
        if count == 0:
            continue
        contribution = divisor * count % MODULUS
        for multiple in range(divisor, limit + 1, divisor):
            exponents[multiple] += contribution
            if exponents[multiple] >= MODULUS:
                exponents[multiple] -= MODULUS

    inverses = [0] * (limit + 1)
    for index in range(1, limit + 1):
        inverses[index] = pow(index, MODULUS - 2, MODULUS)

    transformed = [0] * (limit + 1)
    transformed[0] = 1
    cutoff = MODULUS * MODULUS
    for size in range(1, limit + 1):
        total = 0
        for k in range(1, size + 1):
            total += exponents[k] * transformed[size - k]
            if total >= cutoff:
                total %= MODULUS
        transformed[size] = total % MODULUS * inverses[size] % MODULUS

    return transformed


def tomGraphCountsUpTo(limit):
    return eulerTransform(lobsterTreeCounts(limit), limit)


def tomGraphCount(vertices):
    return tomGraphCountsUpTo(vertices)[vertices]


def runTests(counts):
    assert counts[3] == 3
    assert counts[7] == 37
    assert counts[10] == 328
    assert counts[20] == 1_416_269


if __name__ == "__main__":
    start = time.time()
    counts = tomGraphCountsUpTo(TARGET)
    runTests(counts)
    answer = counts[TARGET]
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
