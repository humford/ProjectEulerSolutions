import time


MODULUS = 2**30
FIRST_ATOM_TERM = 8


CONWAY_ATOMS = [
    ("H", "22", "H"),
    ("He", "13112221133211322112211213322112", "Hf.Pa.H.Ca.Li"),
    ("Li", "312211322212221121123222112", "He"),
    ("Be", "111312211312113221133211322112211213322112", "Ge.Ca.Li"),
    ("B", "1321132122211322212221121123222112", "Be"),
    ("C", "3113112211322112211213322112", "B"),
    ("N", "111312212221121123222112", "C"),
    ("O", "132112211213322112", "N"),
    ("F", "31121123222112", "O"),
    ("Ne", "111213322112", "F"),
    ("Na", "123222112", "Ne"),
    ("Mg", "3113322112", "Pm.Na"),
    ("Al", "1113222112", "Mg"),
    ("Si", "1322112", "Al"),
    ("P", "311311222112", "Ho.Si"),
    ("S", "1113122112", "P"),
    ("Cl", "132112", "S"),
    ("Ar", "3112", "Cl"),
    ("K", "1112", "Ar"),
    ("Ca", "12", "K"),
    ("Sc", "3113112221133112", "Ho.Pa.H.Ca.Co"),
    ("Ti", "11131221131112", "Sc"),
    ("V", "13211312", "Ti"),
    ("Cr", "31132", "V"),
    ("Mn", "111311222112", "Cr.Si"),
    ("Fe", "13122112", "Mn"),
    ("Co", "32112", "Fe"),
    ("Ni", "11133112", "Zn.Co"),
    ("Cu", "131112", "Ni"),
    ("Zn", "312", "Cu"),
    ("Ga", "13221133122211332", "Eu.Ca.Ac.H.Ca.Zn"),
    ("Ge", "31131122211311122113222", "Ho.Ga"),
    ("As", "11131221131211322113322112", "Ge.Na"),
    ("Se", "13211321222113222112", "As"),
    ("Br", "3113112211322112", "Se"),
    ("Kr", "11131221222112", "Br"),
    ("Rb", "1321122112", "Kr"),
    ("Sr", "3112112", "Rb"),
    ("Y", "1112133", "Sr.U"),
    ("Zr", "12322211331222113112211", "Y.H.Ca.Tc"),
    ("Nb", "1113122113322113111221131221", "Er.Zr"),
    ("Mo", "13211322211312113211", "Nb"),
    ("Tc", "311322113212221", "Mo"),
    ("Ru", "132211331222113112211", "Eu.Ca.Tc"),
    ("Rh", "311311222113111221131221", "Ho.Ru"),
    ("Pd", "111312211312113211", "Rh"),
    ("Ag", "132113212221", "Pd"),
    ("Cd", "3113112211", "Ag"),
    ("In", "11131221", "Cd"),
    ("Sn", "13211", "In"),
    ("Sb", "3112221", "Pm.Sn"),
    ("Te", "1322113312211", "Eu.Ca.Sb"),
    ("I", "311311222113111221", "Ho.Te"),
    ("Xe", "11131221131211", "I"),
    ("Cs", "13211321", "Xe"),
    ("Ba", "311311", "Cs"),
    ("La", "11131", "Ba"),
    ("Ce", "1321133112", "La.H.Ca.Co"),
    ("Pr", "31131112", "Ce"),
    ("Nd", "111312", "Pr"),
    ("Pm", "132", "Nd"),
    ("Sm", "311332", "Pm.Ca.Zn"),
    ("Eu", "1113222", "Sm"),
    ("Gd", "13221133112", "Eu.Ca.Co"),
    ("Tb", "3113112221131112", "Ho.Gd"),
    ("Dy", "111312211312", "Tb"),
    ("Ho", "1321132", "Dy"),
    ("Er", "311311222", "Ho.Pm"),
    ("Tm", "11131221133112", "Er.Ca.Co"),
    ("Yb", "1321131112", "Tm"),
    ("Lu", "311312", "Yb"),
    ("Hf", "11132", "Lu"),
    ("Ta", "13112221133211322112211213322113", "Hf.Pa.H.Ca.W"),
    ("W", "312211322212221121123222113", "Ta"),
    ("Re", "111312211312113221133211322112211213322113", "Ge.Ca.W"),
    ("Os", "1321132122211322212221121123222113", "Re"),
    ("Ir", "3113112211322112211213322113", "Os"),
    ("Pt", "111312212221121123222113", "Ir"),
    ("Au", "132112211213322113", "Pt"),
    ("Hg", "31121123222113", "Au"),
    ("Tl", "111213322113", "Hg"),
    ("Pb", "123222113", "Tl"),
    ("Bi", "3113322113", "Pm.Pb"),
    ("Po", "1113222113", "Bi"),
    ("At", "1322113", "Po"),
    ("Rn", "311311222113", "Ho.At"),
    ("Fr", "1113122113", "Rn"),
    ("Ra", "132113", "Fr"),
    ("Ac", "3113", "Ra"),
    ("Th", "1113", "Ac"),
    ("Pa", "13", "Th"),
    ("U", "3", "Pa"),
]


def lookAndSay(term):
    pieces = []
    index = 0

    while index < len(term):
        end = index + 1

        while end < len(term) and term[end] == term[index]:
            end += 1

        pieces.append(str(end - index))
        pieces.append(term[index])
        index = end

    return "".join(pieces)


def bruteDigitCounts(index):
    term = "1"

    for _ in range(1, index):
        term = lookAndSay(term)

    return tuple(term.count(digit) for digit in "123")


def atomIndexes():
    return {name: index for index, (name, _, _) in enumerate(CONWAY_ATOMS)}


def validateAtomTable():
    sequences = {name: sequence for name, sequence, _ in CONWAY_ATOMS}

    for name, sequence, decay in CONWAY_ATOMS:
        expected = "".join(sequences[child] for child in decay.split("."))
        assert lookAndSay(sequence) == expected, name


def transitionMatrix():
    indexes = atomIndexes()
    size = len(CONWAY_ATOMS)
    matrix = [[0] * size for _ in range(size)]

    for source, (_, _, decay) in enumerate(CONWAY_ATOMS):
        for target in decay.split("."):
            matrix[source][indexes[target]] += 1

    return matrix


def multiplyMatrices(left, right):
    size = len(left)
    product = [[0] * size for _ in range(size)]

    for row in range(size):
        productRow = product[row]

        for middle, leftValue in enumerate(left[row]):
            if leftValue == 0:
                continue

            rightRow = right[middle]

            for column, rightValue in enumerate(rightRow):
                if rightValue:
                    productRow[column] = (
                        productRow[column] + leftValue * rightValue
                    ) % MODULUS

    return product


def multiplyVector(vector, matrix):
    result = [0] * len(vector)

    for source, value in enumerate(vector):
        if value == 0:
            continue

        for target, multiplier in enumerate(matrix[source]):
            if multiplier:
                result[target] = (result[target] + value * multiplier) % MODULUS

    return result


def initialAtomVector():
    indexes = atomIndexes()
    term = "1"

    for _ in range(1, FIRST_ATOM_TERM):
        term = lookAndSay(term)

    assert term == CONWAY_ATOMS[indexes["Hf"]][1] + CONWAY_ATOMS[indexes["Sn"]][1]
    vector = [0] * len(CONWAY_ATOMS)
    vector[indexes["Hf"]] = 1
    vector[indexes["Sn"]] = 1

    return vector


def atomVectorAt(index):
    vector = initialAtomVector()

    if index < FIRST_ATOM_TERM:
        raise ValueError("atom decomposition starts at term 8")

    matrix = transitionMatrix()
    exponent = index - FIRST_ATOM_TERM

    while exponent:
        if exponent % 2 == 1:
            vector = multiplyVector(vector, matrix)

        exponent //= 2

        if exponent:
            matrix = multiplyMatrices(matrix, matrix)

    return vector


def digitCounts(index):
    if index < FIRST_ATOM_TERM:
        return bruteDigitCounts(index)

    vector = atomVectorAt(index)
    totals = []

    for digit in "123":
        totals.append(
            sum(
                atomCount * sequence.count(digit)
                for atomCount, (_, sequence, _) in zip(vector, CONWAY_ATOMS)
            )
            % MODULUS
        )

    return tuple(totals)


def formattedCounts(index):
    return ",".join(str(count) for count in digitCounts(index))


def runTests():
    validateAtomTable()
    assert digitCounts(1) == (1, 0, 0)
    assert digitCounts(8) == (6, 2, 2)
    assert digitCounts(40) == (31254, 20259, 11625)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = formattedCounts(10**12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
