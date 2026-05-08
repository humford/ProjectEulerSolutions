import itertools
import time


def scoringDarts():
    darts = [("M", 0)]
    for value in range(1, 21):
        darts.append(("S" + str(value), value))
        darts.append(("D" + str(value), 2 * value))
        darts.append(("T" + str(value), 3 * value))
    darts.append(("S25", 25))
    darts.append(("D25", 50))
    return darts


def finishingDoubles():
    return [("D" + str(value), 2 * value) for value in range(1, 21)] + [("D25", 50)]


def checkoutCountBelow(limit):
    count = 0
    darts = scoringDarts()

    for first, second in itertools.combinations_with_replacement(darts, 2):
        subtotal = first[1] + second[1]
        for _, finish_score in finishingDoubles():
            if subtotal + finish_score < limit:
                count += 1

    return count


def runTests():
    assert len(finishingDoubles()) == 21
    assert checkoutCountBelow(3) == 1


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = checkoutCountBelow(100)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
