from fractions import Fraction
from functools import cache
import time


P_ADIC_ORDER_LIMIT = 12


class HarmonicDenominatorSearch:
    def __init__(self, p):
        self.p = p
        self.binomial = self._binomialTable(P_ADIC_ORDER_LIMIT)
        self.prefixPowers = self._prefixPowerTable()
        self.digitPowerSums = [
            self.prefixPowers[p][exponent]
            for exponent in range(P_ADIC_ORDER_LIMIT + 1)
        ]
        self.harmonicResidueDigits = self._harmonicResidueDigits()

    def _binomialTable(self, limit):
        table = [[0] * (limit + 1) for _ in range(limit + 1)]
        for n in range(limit + 1):
            table[n][0] = table[n][n] = 1
            for k in range(1, n):
                table[n][k] = table[n - 1][k - 1] + table[n - 1][k]
        return table

    def _prefixPowerTable(self):
        table = [[0] * (P_ADIC_ORDER_LIMIT + 1) for _ in range(self.p + 1)]
        for r in range(1, self.p + 1):
            base = r - 1
            for exponent in range(P_ADIC_ORDER_LIMIT + 1):
                table[r][exponent] = table[r - 1][exponent] + base**exponent
        return table

    def _harmonicResidueDigits(self):
        residueToDigits = {}
        total = 0
        for digit in range(self.p):
            if digit:
                total = (total + pow(digit, -1, self.p)) % self.p
            residueToDigits.setdefault(total, []).append(digit)
        return residueToDigits

    @cache
    def powerSum(self, exponent, limit, modulusPower):
        if limit <= 0:
            return 0

        modulus = self.p**modulusPower
        if limit <= self.p:
            return self.prefixPowers[limit][exponent] % modulus

        quotient, remainder = divmod(limit, self.p)
        total = 0
        for termExponent in range(exponent + 1):
            total = (
                total
                + self.binomial[exponent][termExponent]
                * pow(self.p, termExponent, modulus)
                * self.powerSum(termExponent, quotient, modulusPower)
                * (self.digitPowerSums[exponent - termExponent] % modulus)
            ) % modulus

        blockBase = (quotient * self.p) % modulus
        for termExponent in range(exponent + 1):
            total = (
                total
                + self.binomial[exponent][termExponent]
                * pow(blockBase, termExponent, modulus)
                * (self.prefixPowers[remainder][exponent - termExponent] % modulus)
            ) % modulus
        return total

    @cache
    def inversePowerSums(self, modulusPower):
        modulus = self.p**modulusPower
        result = []
        for exponent in range(modulusPower):
            total = 0
            for residue in range(1, self.p):
                inverse = pow(residue, -1, modulus)
                total = (total + pow(inverse, exponent + 1, modulus)) % modulus
            result.append(total)
        return tuple(result)

    @cache
    def unitInverseSum(self, limit, modulusPower):
        if limit <= 0:
            return 0

        modulus = self.p**modulusPower
        quotient, remainder = divmod(limit, self.p)
        coefficients = self.inversePowerSums(modulusPower)
        total = 0

        for exponent in range(modulusPower):
            term = (
                pow(self.p, exponent, modulus)
                * self.powerSum(exponent, quotient, modulusPower)
                * coefficients[exponent]
            ) % modulus
            if exponent % 2:
                term = (-term) % modulus
            total = (total + term) % modulus

        blockBase = quotient * self.p
        for residue in range(1, remainder + 1):
            total = (total + pow(blockBase + residue, -1, modulus)) % modulus
        return total

    @cache
    def scaledHarmonicSum(self, level, prefix, modulusPower):
        modulus = self.p**modulusPower
        total = 0
        divisor = 1
        for block in range(1, level + 1):
            total = (
                total
                + self.p ** (level - block)
                * self.unitInverseSum(prefix // divisor, modulusPower)
            ) % modulus
            divisor *= self.p
        return total

    def search(self):
        if self.p == 3:
            return self._smallPrimeSearch()

        best = self.p - 1
        candidates = [
            digit
            for digit in self.harmonicResidueDigits.get(0, [])
            if 1 <= digit < self.p
        ]
        level = 1

        while candidates:
            best = max(best, self.p * max(candidates) + (self.p - 1))
            nextCandidates = set()

            for prefix in candidates:
                value = self.scaledHarmonicSum(level, prefix, level + 1)
                nextDigitTarget = (-(value // (self.p**level))) % self.p
                for digit in self.harmonicResidueDigits.get(nextDigitTarget, []):
                    nextCandidates.add(prefix * self.p + digit)

            candidates = sorted(nextCandidates)
            level += 1

        return best

    def _smallPrimeSearch(self):
        harmonic = Fraction(0, 1)
        best = 0
        for n in range(1, 500):
            harmonic += Fraction(1, n)
            if harmonic.denominator % self.p != 0:
                best = n
        return best


def harmonicDenominatorLimit(p):
    return HarmonicDenominatorSearch(p).search()


def runTests():
    assert harmonicDenominatorLimit(3) == 68
    assert harmonicDenominatorLimit(7) == 719_102


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = harmonicDenominatorLimit(137)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
