import time


TARGET_SCORE = 20
SHOT_COUNT = 50
TARGET_PROBABILITY = 0.02


def scoreProbability(q, target_score=TARGET_SCORE):
    probabilities = [0.0] * (target_score + 1)
    probabilities[0] = 1.0

    for distance in range(1, SHOT_COUNT + 1):
        score_probability = 1 - distance / q
        miss_probability = 1 - score_probability

        for score in range(min(distance, target_score), 0, -1):
            probabilities[score] = (
                probabilities[score] * miss_probability
                + probabilities[score - 1] * score_probability
            )

        probabilities[0] *= miss_probability

    return probabilities[target_score]


def findQ():
    low = 50.0
    high = 100.0

    for _ in range(100):
        middle = (low + high) / 2

        if scoreProbability(middle) > TARGET_PROBABILITY:
            low = middle
        else:
            high = middle

    return (low + high) / 2


def runTests():
    q = findQ()
    assert abs(scoreProbability(q) - TARGET_PROBABILITY) < 1e-14


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = format(findQ(), ".10f")
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
