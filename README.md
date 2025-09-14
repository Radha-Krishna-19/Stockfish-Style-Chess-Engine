# Stockfish Chess Engine Clone

## Overview

This project is a simplified chess engine built in Python, with features including:

- Comprehensive move generation for all chess pieces
- Move application and legal move validation
- Check detection and checkmate/stalemate handling
- Minimax search with alpha-beta pruning for AI move selection
- Full algebraic notation (SAN) support for user move input (using python-chess)

## Structure

- `move_generation.py`: Generates all possible moves per piece and combined legal moves
- `move_application.py`: Applies moves to board and updates game state
- `main.py`: Engine search, evaluation, check detection, user interface loop
- `tests/`: Unit tests for move generation and application
- `requirements.txt`: Required packages (includes python-chess)
- `README.md`: Project documentation

## Installation

Install required packages:

pip install -r requirements.txt


## Running

Run the engine and play against the AI:

python main.py


Enter your moves in Standard Algebraic Notation (e.g., `e4`, `Nf3`, `O-O`).

## Testing

Run tests with:

pytest tests/


## Future Work

- Better board evaluation heuristics
- Full move legality validation including pins
- Opening book support
- GUI integration