import time
from array import array
from math import comb, fsum


class Model:
    def __init__(self, n):
        self.n = n
        self.total = comb(n + 4, 4)
        self.maxRemaining = 4 * n
        self.buckets = [[[] for _ in range(n + 1)] for __ in range(self.maxRemaining + 1)]

        self.inverseRemaining = array("d", [0.0]) * self.total

        self.next0 = array("I", [0]) * self.total
        self.next1 = array("I", [0]) * self.total
        self.next2 = array("I", [0]) * self.total
        self.next3 = array("I", [0]) * self.total

        self.count0 = array("H", [0]) * self.total
        self.count1 = array("H", [0]) * self.total
        self.count2 = array("H", [0]) * self.total
        self.count3 = array("H", [0]) * self.total

        prefixByTotal = [0] * (n + 2)
        for totalCategories in range(n + 1):
            prefixByTotal[totalCategories + 1] = (
                prefixByTotal[totalCategories] + comb(totalCategories + 3, 3)
            )

        prefixByX0 = []
        for totalCategories in range(n + 1):
            prefixes = [0] * (totalCategories + 2)
            running = 0
            for x0 in range(totalCategories + 1):
                prefixes[x0] = running
                rest = totalCategories - x0
                running += comb(rest + 2, 2)
            prefixes[totalCategories + 1] = running
            prefixByX0.append(prefixes)

        def index(x0, x1, x2, x3):
            totalCategories = x0 + x1 + x2 + x3
            rest = totalCategories - x0
            result = prefixByTotal[totalCategories] + prefixByX0[totalCategories][x0]
            result += x1 * (rest + 1) - x1 * (x1 - 1) // 2
            result += x2
            return result

        stateIndex = 0
        for totalCategories in range(n + 1):
            for x0 in range(totalCategories + 1):
                rest = totalCategories - x0
                for x1 in range(rest + 1):
                    remainingAfterX1 = rest - x1
                    for x2 in range(remainingAfterX1 + 1):
                        x3 = remainingAfterX1 - x2

                        remainingCards = 4 * x0 + 3 * x1 + 2 * x2 + x3
                        activePiles = x1 + x2 + x3

                        if remainingCards:
                            self.inverseRemaining[stateIndex] = 1.0 / remainingCards
                        self.buckets[remainingCards][activePiles].append(stateIndex)

                        if x0:
                            self.next0[stateIndex] = index(x0 - 1, x1 + 1, x2, x3)
                            self.count0[stateIndex] = 4 * x0
                        if x1:
                            self.next1[stateIndex] = index(x0, x1 - 1, x2 + 1, x3)
                            self.count1[stateIndex] = 3 * x1
                        if x2:
                            self.next2[stateIndex] = index(x0, x1, x2 - 1, x3 + 1)
                            self.count2[stateIndex] = 2 * x2
                        if x3:
                            self.next3[stateIndex] = index(x0, x1, x2, x3 - 1)
                            self.count3[stateIndex] = x3

                        stateIndex += 1

        self.start = index(n, 0, 0, 0)


def probabilityMaximumBelow(model, threshold):
    total = model.total
    maxActive = min(threshold - 1, model.n)
    dp = [0.0] * total
    dp[0] = 1.0

    for remainingCards in range(1, model.maxRemaining + 1):
        for activePiles in range(maxActive + 1):
            for state in model.buckets[remainingCards][activePiles]:
                dp[state] = (
                    model.count0[state] * dp[model.next0[state]]
                    + model.count1[state] * dp[model.next1[state]]
                    + model.count2[state] * dp[model.next2[state]]
                    + model.count3[state] * dp[model.next3[state]]
                ) * model.inverseRemaining[state]

    return dp[model.start]


def expectedMaximumPiles(n):
    model = Model(n)
    probabilities = [probabilityMaximumBelow(model, threshold) for threshold in range(1, n + 1)]
    return fsum(1.0 - probability for probability in probabilities)


def formattedExpectedMaximumPiles(n):
    return f"{expectedMaximumPiles(n):.8f}"


def runTests():
    assert formattedExpectedMaximumPiles(2) == "1.97142857"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = formattedExpectedMaximumPiles(60)
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
