# Repository Guidelines

## Project Structure & Module Organization

This repository contains standalone Project Euler solutions. Active Python 3 solutions live in `Python3/` and follow the naming pattern `Problem<N>.py`, for example `Python3/Problem51.py`. Supporting input data from Project Euler lives in `Files/`, usually named with the original problem file name such as `Files/p096_sudoku.txt`. Historical or alternate implementations are kept under `Other/`, including `Other/Python2.7/` and `Other/JavaScript/`. There is no package layout or shared application entrypoint.

## Build, Test, and Development Commands

There is no build step. Run scripts directly from the repository root so relative `Files/` paths resolve correctly.

- `python3 Python3/Problem51.py`: runs one solution and prints its answer.
- `python3 -m py_compile Python3/Problem51.py`: syntax-checks one solution without running it.
- `python3 -m compileall Python3`: syntax-checks the Python 3 solution directory after broad edits.

Avoid committing generated `__pycache__/` files or local editor/system artifacts.

## Coding Style & Naming Conventions

Use Python 3 and the standard library unless a problem clearly requires otherwise. Match the existing style: 4-space indentation, small helper functions, and descriptive camelCase function names such as `primeSieve`, `runTests`, or `minimalPentagonalDifference`. Keep each solution self-contained in its own `Problem<N>.py` file. Place executable work behind `if __name__ == "__main__":` when adding or modernizing solutions, and print the final answer clearly.

## Testing Guidelines

There is no central test framework or coverage target. Prefer lightweight in-file checks using `assert` inside a `runTests()` helper, then call it before the final timed or printed answer. Include tests for known examples from the problem statement and for any nontrivial helper functions. Before submitting, run the changed script directly and record the command and final answer.

## Commit & Pull Request Guidelines

Recent commits use concise subjects like `solved Problem 228`. For new solutions, follow `solved Problem <N>` and keep one problem per commit when practical. Pull requests should name the problem number, summarize the mathematical or algorithmic approach, list any added input files under `Files/`, and include the verification command, answer, and runtime if notable. Do not mix unrelated cleanup with a solution commit.

## Agent-Specific Instructions

Treat unrelated worktree changes as user-owned. When adding a solution or guide, edit only the relevant file(s), preserve existing problem files unless asked, and verify locally before reporting completion.
