import functools
import time


def playerTwoWinProbability(target):
    @functools.cache
    def playerTwoTurn(player_one_needed, player_two_needed):
        if player_two_needed <= 0:
            return 1.0
        if player_one_needed <= 0:
            return 0.0

        best = 0.0
        points = 1
        probability_two_scores = 0.5

        while True:
            next_two_needed = player_two_needed - points
            current = (
                0.5 * probability_two_scores * playerTwoTurn(player_one_needed - 1, next_two_needed)
                + 0.5 * probability_two_scores * playerTwoTurn(player_one_needed, next_two_needed)
                + 0.5 * (1 - probability_two_scores) * playerTwoTurn(player_one_needed - 1, player_two_needed)
            )
            current /= 1 - 0.5 * (1 - probability_two_scores)
            best = max(best, current)

            if next_two_needed <= 0:
                break

            points *= 2
            probability_two_scores /= 2

        return best

    return 0.5 * playerTwoTurn(target - 1, target) + 0.5 * playerTwoTurn(target, target)


def runTests():
    assert f"{playerTwoWinProbability(1):.8f}" == "0.33333333"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = f"{playerTwoWinProbability(100):.8f}"
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
