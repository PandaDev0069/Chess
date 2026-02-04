# This is a README FOR CHESS GAME MADE IN PYTHON

## Setup (Windows)

```powershell
# Create venv (Python 3.12 recommended for pygame)
py -3.12 -m venv .venv

# Activate venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install -r requirements.txt

# Run
python main.py
```

## File Structure

``` text
chess_game/
│
├── main.py
│
├── core/
│   ├── board.py
│   ├── piece.py
│   ├── move.py
│   ├── game_state.py
│   │
│   ├── pieces/
│   │   ├── pawn.py
│   │   ├── knight.py
│   │   ├── bishop.py
│   │   ├── rook.py
│   │   ├── queen.py
│   │   └── king.py
│   │
│   └── rules/
│       ├── attack.py
│       ├── legality.py
│       ├── check.py
│       └── special.py
│
├── ui/
│   ├── renderer/
│   │   ├── board_renderer.py
│   │   ├── piece_renderer.py
│   │   └── highlight_renderer.py
│   ├── input/
│   │   └── input_handler.py
│   └── assets.py
│
├── assets/
│   └── images/
│
├── utils/
│   ├── constants.py
│   └── helpers.py
│
└── README.md

```
