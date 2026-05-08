import heapq
import time
from pathlib import Path


def readAttempts():
    path = Path(__file__).resolve().parents[1] / "Files" / "p079_keylog.txt"
    return path.read_text().strip().splitlines()


def shortestPasscode(attempts):
    digits = set("".join(attempts))
    outgoing = {digit: set() for digit in digits}
    incoming = {digit: set() for digit in digits}

    for attempt in attempts:
        for before, after in zip(attempt, attempt[1:]):
            outgoing[before].add(after)
            incoming[after].add(before)

    available = [digit for digit in digits if not incoming[digit]]
    heapq.heapify(available)
    result = []

    while available:
        digit = heapq.heappop(available)
        result.append(digit)

        for after in sorted(outgoing[digit]):
            incoming[after].remove(digit)
            if not incoming[after]:
                heapq.heappush(available, after)

    if len(result) != len(digits):
        raise ValueError("Cycle found in login attempts")

    return "".join(result)


def runTests():
    assert shortestPasscode(["123", "345"]) == "12345"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = shortestPasscode(readAttempts())
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
