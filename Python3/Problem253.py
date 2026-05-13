import bisect
import collections
import decimal
import math
import time


PIECES = 40


def canonicalEdges(first, second):
    if first <= second:
        return first, second
    return second, first


def insertGap(gaps, gap):
    index = bisect.bisect_left(gaps, gap)
    return gaps[:index] + (gap,) + gaps[index:]


def removeGap(gaps, gap):
    index = bisect.bisect_left(gaps, gap)
    return gaps[:index] + gaps[index + 1 :]


def segmentCount(state):
    if state is None:
        return 0
    return len(state[2]) + 1


def initialTransitions(piece_count):
    transitions = collections.defaultdict(int)

    for position in range(piece_count):
        left = position
        right = piece_count - 1 - position
        transitions[canonicalEdges(left, right) + ((),)] += 1

    return tuple(transitions.items())


TRANSITION_CACHE = {}


def transitions(state):
    if state in TRANSITION_CACHE:
        return TRANSITION_CACHE[state]

    edge_1, edge_2, internal_gaps = state
    result = collections.defaultdict(int)
    index = 0

    while index < len(internal_gaps):
        gap = internal_gaps[index]
        end = index
        while end < len(internal_gaps) and internal_gaps[end] == gap:
            end += 1

        multiplicity = end - index
        without_gap = removeGap(internal_gaps, gap)

        if gap == 1:
            result[(edge_1, edge_2, without_gap)] += multiplicity
        else:
            result[(edge_1, edge_2, insertGap(without_gap, gap - 1))] += (
                2 * multiplicity
            )

            for left in range(1, gap - 1):
                right = gap - 1 - left
                if left > right:
                    break

                ways = multiplicity
                if left != right:
                    ways *= 2
                result[
                    (
                        edge_1,
                        edge_2,
                        insertGap(insertGap(without_gap, left), right),
                    )
                ] += ways

        index = end

    if edge_1 == edge_2:
        edge_groups = ((edge_1, 2, edge_2),)
    else:
        edge_groups = ((edge_1, 1, edge_2), (edge_2, 1, edge_1))

    for gap, multiplicity, other_edge in edge_groups:
        if gap == 0:
            continue

        result[canonicalEdges(gap - 1, other_edge) + (internal_gaps,)] += multiplicity

        for new_edge in range(gap - 1):
            new_internal = gap - new_edge - 1
            result[
                canonicalEdges(new_edge, other_edge)
                + (insertGap(internal_gaps, new_internal),)
            ] += multiplicity

    TRANSITION_CACHE[state] = tuple(result.items())
    return TRANSITION_CACHE[state]


def maximumSegmentDistribution(piece_count):
    current = {None: {0: 1}}
    first_transitions = initialTransitions(piece_count)

    for _ in range(piece_count):
        next_states = collections.defaultdict(lambda: collections.defaultdict(int))

        for state, maximum_counts in current.items():
            state_transitions = first_transitions if state is None else transitions(state)

            for maximum, count in maximum_counts.items():
                for next_state, multiplicity in state_transitions:
                    next_maximum = max(maximum, segmentCount(next_state))
                    next_states[next_state][next_maximum] += count * multiplicity

        current = {state: dict(maximums) for state, maximums in next_states.items()}

    final_state = (0, 0, ())
    distribution = current[final_state]
    assert sum(distribution.values()) == math.factorial(piece_count)
    return distribution


def expectedMaximumSegments(piece_count):
    distribution = maximumSegmentDistribution(piece_count)
    numerator = sum(maximum * count for maximum, count in distribution.items())
    denominator = math.factorial(piece_count)
    return decimal.Decimal(numerator) / decimal.Decimal(denominator)


def roundedExpectation(piece_count):
    decimal.getcontext().prec = 80
    value = expectedMaximumSegments(piece_count)
    rounded = value.quantize(decimal.Decimal("0.000001"), rounding=decimal.ROUND_HALF_UP)
    return format(rounded, ".6f")


def runTests():
    expected_distribution = {
        1: 512,
        2: 250912,
        3: 1815264,
        4: 1418112,
        5: 144000,
    }
    assert maximumSegmentDistribution(10) == expected_distribution
    assert roundedExpectation(10) == "3.400732"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = roundedExpectation(PIECES)
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
