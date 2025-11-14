# roarmpy

Minimal Python library to interface RoArm robot arms.

Features:
- High-level `RoArmClient` with pluggable transports (serial, TCP, dummy)
- Small CLI for quick commands

Quick install (local):

```bash
python -m pip install --upgrade build twine
python -m build
python -m pip install dist/roarmpy-0.0.1-py3-none-any.whl
```

Publish to PyPI:

```bash
python -m pip install --upgrade twine
python -m build
python -m twine upload dist/*
```

Basic usage:

```python
from roarmpy import RoArmClient

client = RoArmClient.with_dummy()
client.move_joint([0, 1.0, 2.0])
```

See `tests` for example unit tests and `src/roarmpy/cli.py` for CLI usage.
