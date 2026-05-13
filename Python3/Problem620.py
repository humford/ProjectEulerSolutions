import math
import time


TAU = 2 * math.pi


def gearArrangementCount(sunTeeth, smallPlanetTeeth, largePlanetTeeth):
    """Return g(s+p+q, s, p, q)."""
    p = smallPlanetTeeth
    q = largePlanetTeeth
    outerTeeth = sunTeeth + p + q

    # Work in circumference-scaled units, so a physical 1 cm radial clearance
    # subtracts 2*pi from the maximum scaled centre distance.
    centerDistance = p + q - TAU
    if centerDistance <= q - p:
        return 0

    outerToSmallCenter = outerTeeth - p
    sunToSmallCenter = sunTeeth + p

    x = (
        centerDistance * centerDistance
        + outerToSmallCenter * outerToSmallCenter
        - sunToSmallCenter * sunToSmallCenter
    ) / (2 * centerDistance)
    ySquared = outerToSmallCenter * outerToSmallCenter - x * x
    y = math.sqrt(max(0.0, ySquared))

    outerAngle = math.atan2(y, x)
    sunAngle = math.atan2(y, x - centerDistance)

    phaseRange = (
        outerToSmallCenter * outerAngle + sunToSmallCenter * sunAngle
    ) / math.pi
    return int(phaseRange + 1e-12)


def totalGearArrangements(limit):
    total = 0
    for sunTeeth in range(5, limit - 9):
        maxSmallPlanet = (limit - sunTeeth - 1) // 2
        for smallPlanetTeeth in range(5, maxSmallPlanet + 1):
            maxLargePlanet = limit - sunTeeth - smallPlanetTeeth
            for largePlanetTeeth in range(smallPlanetTeeth + 1, maxLargePlanet + 1):
                total += gearArrangementCount(
                    sunTeeth, smallPlanetTeeth, largePlanetTeeth
                )
    return total


def runTests():
    assert gearArrangementCount(5, 5, 6) == 9
    assert totalGearArrangements(16) == 9
    assert totalGearArrangements(20) == 205


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = totalGearArrangements(500)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
