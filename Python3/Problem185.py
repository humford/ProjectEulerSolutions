import time
from itertools import combinations


def parseClues(raw_clues):
    return [(tuple(int(digit) for digit in guess), matches) for guess, matches in raw_clues]


def digitMask(digit):
    return 1 << digit


def onlyDigit(mask):
    return mask.bit_length() - 1


def solveNumberMind(raw_clues):
    clues = parseClues(raw_clues)
    length = len(clues[0][0])
    all_digits = (1 << 10) - 1
    starting_domains = tuple([all_digits] * length)
    solutions = []

    def clueChoices(domains, clue):
        guess, target = clue
        required = []
        optional = []

        for position, digit in enumerate(guess):
            mask = digitMask(digit)
            if domains[position] == mask:
                required.append(position)
            elif domains[position] & mask:
                optional.append(position)

        needed = target - len(required)
        if needed < 0 or needed > len(optional):
            return None

        return required, optional, needed

    def applyChoice(domains, clue, matching_positions):
        guess, _ = clue
        next_domains = list(domains)
        matching_positions = set(matching_positions)

        for position, digit in enumerate(guess):
            mask = digitMask(digit)
            if position in matching_positions:
                next_domains[position] &= mask
            else:
                next_domains[position] &= ~mask

            if next_domains[position] == 0:
                return None

        return tuple(next_domains)

    def search(domains, remaining_clues):
        if len(solutions) > 1:
            return

        if not remaining_clues:
            if all(mask.bit_count() == 1 for mask in domains):
                solutions.append("".join(str(onlyDigit(mask)) for mask in domains))
            return

        best_index = None
        best_choice_data = None
        best_choice_count = None

        for clue_index, clue in enumerate(remaining_clues):
            choice_data = clueChoices(domains, clue)
            if choice_data is None:
                return

            _, optional, needed = choice_data
            choice_count = mathComb(len(optional), needed)
            if best_choice_count is None or choice_count < best_choice_count:
                best_index = clue_index
                best_choice_data = choice_data
                best_choice_count = choice_count
                if choice_count == 1:
                    break

        clue = remaining_clues[best_index]
        next_clues = remaining_clues[:best_index] + remaining_clues[best_index + 1 :]
        required, optional, needed = best_choice_data

        for chosen_optional in combinations(optional, needed):
            next_domains = applyChoice(domains, clue, required + list(chosen_optional))
            if next_domains is None:
                continue
            search(next_domains, next_clues)

    search(starting_domains, tuple(clues))
    assert len(solutions) == 1
    return solutions[0]


def mathComb(n, r):
    if r < 0 or r > n:
        return 0
    if r == 0 or r == n:
        return 1

    r = min(r, n - r)
    result = 1
    for offset in range(1, r + 1):
        result = result * (n - r + offset) // offset

    return result


def runTests():
    assert (
        solveNumberMind(
            [
                ("90342", 2),
                ("70794", 0),
                ("39458", 2),
                ("34109", 1),
                ("51545", 2),
                ("12531", 1),
            ]
        )
        == "39542"
    )


if __name__ == "__main__":
    runTests()
    clues = [
        ("5616185650518293", 2),
        ("3847439647293047", 1),
        ("5855462940810587", 3),
        ("9742855507068353", 3),
        ("4296849643607543", 3),
        ("3174248439465858", 1),
        ("4513559094146117", 2),
        ("7890971548908067", 3),
        ("8157356344118483", 1),
        ("2615250744386899", 2),
        ("8690095851526254", 3),
        ("6375711915077050", 1),
        ("6913859173121360", 1),
        ("6442889055042768", 2),
        ("2321386104303845", 0),
        ("2326509471271448", 2),
        ("5251583379644322", 2),
        ("1748270476758276", 3),
        ("4895722652190306", 1),
        ("3041631117224635", 3),
        ("1841236454324589", 3),
        ("2659862637316867", 2),
    ]
    start = time.time()
    answer = solveNumberMind(clues)
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
