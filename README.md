# Analytics App for Chess.com

## Installation

The app is built using UV as Python package and project manager.
First, you need to install [UV](https://docs.astral.sh/uv/getting-started/installation/) :

```
# On macOS and Linux.
$ curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows.
$ powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

You might need to add UV command to PATH.

\
You'll then be able to download the required python packages (with dev packages) :

```
uv sync --dev
```

\
To run the app locally :

```
uv run python -m src.chess_analytics.app
```
