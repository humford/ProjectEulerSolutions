import re
import time


STATEMENT_HTML = """
<p>Let $A$ be an <b>affine plane</b> over a
<b>radically integral local field</b> $F$ with residual characteristic $p$.</p>
<p>We consider an <b>open oriented line section</b> $U$ of $A$ with normalized
Haar measure $m$.</p>
<p>Define $f(m, p)$ as the maximal possible discriminant of the
<b>jacobian</b> associated to the <b>orthogonal kernel embedding</b> of $U$
into $A$.</p>
<p>Find $f(20230401, 57)$. Give as your answer the concatenation of the first
letters of each bolded word.</p>
"""


def boldedPhrases(statementHtml=STATEMENT_HTML):
    return re.findall(r"<b>(.*?)</b>", statementHtml, re.DOTALL)


def solve(statementHtml=STATEMENT_HTML):
    answer = []
    for phrase in boldedPhrases(statementHtml):
        for word in phrase.split():
            answer.append(word[0].lower())
    return "".join(answer)


def runTests():
    assert boldedPhrases() == [
        "affine plane",
        "radically integral local field",
        "open oriented line section",
        "jacobian",
        "orthogonal kernel embedding",
    ]
    assert solve() == "aprilfoolsjoke"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
