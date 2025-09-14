# Python Chess Engine

This is a classical chess engine implemented entirely in Python, designed to demonstrate core chess engine principles including:

- Board representation and move generation
- Move application and undo
- Alpha-beta search with Principal Variation Search (PVS)
- Quiescence search with captures and checks (recursion depth limited)
- Transposition tables for caching positions
- Advanced evaluation combining piece values, piece-square tables, pawn structure, mobility, and king safety
- Move ordering heuristics including MVV-LVA, killer moves, and history heuristic
- Iterative deepening search with per-move time limits

---

## Features

- **Search:** Implements alpha-beta with PVS and iterative deepening for efficient, deep search.
- **Evaluation:** Combines material count, positional tables, mobility, pawn-structure analysis, and king safety heuristics.
- **Move Ordering:** Prioritizes strong moves using MVV-LVA, killer moves, and history heuristics.
- **Quiescence Search:** Probes tactical moves (captures and checks) to reduce horizon effects, limited to safe depth.
- **Interactive Play:** Play against the engine interactively via console with SAN move input.

---

## Project Structure

- `main.py` - Core engine logic: search, evaluation, and game loop.
- `move_generation.py` - Functions to generate all legal moves for pieces.
- `move_application.py` - Logic for applying and undoing moves.
- `tests/` - Automated tests for move generation, move application, and evaluation.
- `requirements.txt` - Python dependencies (`pytest`, `python-chess` for SAN parsing).
- `run_tests.bat` - Script to run all tests in Windows.
- `.gitignore`, `README.md` - Project metadata and ignore rules.
- `venv/` - (optional) Virtual environment, usually ignored by git.

---

## Usage

To play against the engine:

python main.py



You will be prompted to select your side (`white` or `black`). Enter moves in [Standard Algebraic Notation (SAN)](https://en.wikipedia.org/wiki/Algebraic_notation_(chess)).  
The engine will reply after thinking for a few seconds (default: 4 seconds per move, can be adjusted).

---

## Testing

You can run all tests using either of the following methods:

**A. Using the batch script (Windows):**
Just double-click `run_tests.bat` or run in the command prompt:

run_tests.bat


- This script sets `PYTHONPATH` for correct imports, runs all tests in the `tests` directory with verbose output, and pauses so you can read the results.

**B. Using Pytest directly (all platforms):**

pytest -v tests



---

## Installation

Requires Python 3.8+  
Install dependencies using:

pip install -r requirements.txt



---

## Limitations

- Written in pure Python; search and evaluation are not as fast as compiled engines like Stockfish.
- Some heuristics and evaluation functions are simplified for clarity.
- No opening book, endgame tablebases, or neural evaluation (yet).

---

## Future Directions

- Porting to C++ for bitboard speed and efficiency.
- Integrating neural network (NNUE) evaluation or machine learning.
- Adding opening book and endgame tablebase support.
- Further evaluation and search optimization.

---

## License

MIT License

---

Made by Radha Krishna