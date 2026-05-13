import time


def randomSequence(count):
    value = 306
    terms = []
    for _ in range(count):
        terms.append(value)
        value = value * value % 10_007
    return terms


def extinctionProbabilityValue(typeCount, choiceCount, tolerance=1e-13):
    randomValues = randomSequence(typeCount * choiceCount)
    choices = [
        [
            randomValues[typeIndex * choiceCount + choiceIndex] % 5
            for choiceIndex in range(choiceCount)
        ]
        for typeIndex in range(typeCount)
    ]

    probabilities = [0.0] * typeCount
    while True:
        nextProbabilities = [0.0] * typeCount
        for typeIndex in range(typeCount):
            probability = probabilities[typeIndex]
            total = 0.0
            for choice in choices[typeIndex]:
                if choice == 0:
                    total += 1.0
                elif choice == 1:
                    total += probability * probability
                elif choice == 2:
                    total += probabilities[(2 * typeIndex) % typeCount]
                elif choice == 3:
                    destination = (typeIndex * typeIndex + 1) % typeCount
                    total += probabilities[destination] ** 3
                else:
                    total += probability * probabilities[(typeIndex + 1) % typeCount]
            nextProbabilities[typeIndex] = total / choiceCount

        delta = max(
            abs(nextProbability - probability)
            for nextProbability, probability
            in zip(nextProbabilities, probabilities)
        )
        probabilities = nextProbabilities
        if delta < tolerance:
            return probabilities[0]


def extinctionProbability(typeCount, choiceCount):
    return format(
        extinctionProbabilityValue(typeCount, choiceCount),
        ".8f",
    )


def runTests():
    assert extinctionProbability(2, 2) == "0.07243802"
    assert extinctionProbability(4, 3) == "0.18554021"
    assert extinctionProbability(10, 5) == "0.53466253"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = extinctionProbability(500, 10)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
