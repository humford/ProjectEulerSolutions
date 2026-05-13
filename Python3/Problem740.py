import collections
import time


def secretSantaFailureProbability(people):
    if people < 2:
        raise ValueError("people must be at least 2")
    if people == 2:
        return 1.0

    # State is (u1, u2, last, processed):
    # u1/u2 count unprocessed non-last people with 1 or 2 slips left,
    # last is the number of last-person slips left, and processed is the
    # indistinguishable pool of slips belonging to people who already drew.
    distribution = {(0, people - 1, 2, 0): 1.0}

    for step in range(people - 1):
        unprocessed = people - 1 - step
        totalSlips = 2 * people - 2 * step
        nextDistribution = collections.defaultdict(float)

        for (oneSlip, twoSlips, lastSlips, processedSlips), probability in distribution.items():
            zeroSlips = unprocessed - oneSlip - twoSlips

            for actorSlips, actorCount in ((0, zeroSlips), (1, oneSlip), (2, twoSlips)):
                if actorCount == 0:
                    continue

                actorProbability = probability * actorCount / unprocessed
                remainingOneSlip = oneSlip
                remainingTwoSlips = twoSlips
                if actorSlips == 1:
                    remainingOneSlip -= 1
                elif actorSlips == 2:
                    remainingTwoSlips -= 1

                firstDenominator = totalSlips - actorSlips
                firstOutcomes = []
                if lastSlips:
                    firstOutcomes.append(
                        (lastSlips / firstDenominator, remainingOneSlip, remainingTwoSlips, lastSlips - 1, processedSlips)
                    )
                if remainingOneSlip:
                    firstOutcomes.append(
                        (remainingOneSlip / firstDenominator, remainingOneSlip - 1, remainingTwoSlips, lastSlips, processedSlips)
                    )
                if remainingTwoSlips:
                    firstOutcomes.append(
                        (
                            2 * remainingTwoSlips / firstDenominator,
                            remainingOneSlip + 1,
                            remainingTwoSlips - 1,
                            lastSlips,
                            processedSlips,
                        )
                    )
                if processedSlips:
                    firstOutcomes.append(
                        (processedSlips / firstDenominator, remainingOneSlip, remainingTwoSlips, lastSlips, processedSlips - 1)
                    )

                secondDenominator = totalSlips - 1 - actorSlips
                for firstProbability, oneAfterFirst, twoAfterFirst, lastAfterFirst, processedAfterFirst in firstOutcomes:
                    transitionProbability = actorProbability * firstProbability
                    processedAfterActor = processedAfterFirst + actorSlips

                    if lastAfterFirst:
                        nextDistribution[(oneAfterFirst, twoAfterFirst, lastAfterFirst - 1, processedAfterActor)] += (
                            transitionProbability * lastAfterFirst / secondDenominator
                        )
                    if oneAfterFirst:
                        nextDistribution[(oneAfterFirst - 1, twoAfterFirst, lastAfterFirst, processedAfterActor)] += (
                            transitionProbability * oneAfterFirst / secondDenominator
                        )
                    if twoAfterFirst:
                        nextDistribution[(oneAfterFirst + 1, twoAfterFirst - 1, lastAfterFirst, processedAfterActor)] += (
                            transitionProbability * 2 * twoAfterFirst / secondDenominator
                        )
                    if processedAfterFirst:
                        nextDistribution[(oneAfterFirst, twoAfterFirst, lastAfterFirst, processedAfterActor - 1)] += (
                            transitionProbability * processedAfterFirst / secondDenominator
                        )

        distribution = nextDistribution

    return sum(probability for (_, _, lastSlips, _), probability in distribution.items() if lastSlips > 0)


def formattedFailureProbability(people):
    return format(secretSantaFailureProbability(people), ".10f")


def runTests():
    assert formattedFailureProbability(3) == "0.3611111111"
    assert formattedFailureProbability(5) == "0.2476095994"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = formattedFailureProbability(100)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
