"""Re-launch the current script under this project's venv, if it isn't already.

Why this exists
---------------
`python app.py` picks up whatever interpreter is on PATH. In this repo that is
usually the repo-root .venv, which does NOT have this project's dependencies:

    ModuleNotFoundError: No module named 'dotenv'
    ModuleNotFoundError: No module named 'langchain_groq'

The only interpreter that can run this project is myenv/bin/python. So instead
of asking you to remember `source myenv/bin/activate`, importing this module
restarts the process under the right interpreter automatically.

Usage - import it BEFORE any third-party import:

    import _bootstrap          # noqa: F401  - must precede langchain imports

Trade-off worth knowing: this hides which interpreter you are on, which is a
thing worth understanding rather than papering over. Activating the venv is
still the "proper" habit - `which python` should point inside myenv/. This is
a convenience so a forgotten activation is not a dead end.

Adapted from 02_handOnWork/_bootstrap.py.
"""

import os
import sys
from pathlib import Path

# The venv lives next to this file, at the project root.
VENV_DIR = Path(__file__).resolve().parent / "myenv"
VENV_PYTHON = VENV_DIR / "bin" / "python"

# Set once before re-exec so a failed switch cannot loop forever.
_GUARD = "_TICKET_ANALYSER_BOOTSTRAPPED"


def _already_correct() -> bool:
    """True if the running interpreter IS the venv one.

    Compare sys.prefix - the root of whatever venv we are in - and NOT the
    resolved path of sys.executable. A venv's bin/python is only a symlink to
    the interpreter it was built from, so .resolve() follows it all the way
    back to the shared base binary. Two different venvs built on the same
    python then resolve to the identical path and compare equal: with the
    repo-root .venv active, that returns True, the re-exec never fires, and
    you get the "No module named 'dotenv'" this file exists to prevent.
    sys.prefix stays distinct per venv, so it is the honest question.
    """
    try:
        return Path(sys.prefix).resolve() == VENV_DIR.resolve()
    except OSError:
        return True  # cannot tell - do not risk an exec loop


def _is_script_run() -> bool:
    """True only when python was given a real script file to run.

    Re-exec rebuilds the command from sys.argv, and that only round-trips for
    `python foo.py`. Under `python -c "..."` argv[0] is "-c" and the code
    itself is not in argv at all, so replaying it would run the wrong thing.
    Interactive and stdin sessions give "" or "-".
    """
    if not sys.argv or sys.argv[0] in ("", "-", "-c"):
        return False
    return Path(sys.argv[0]).is_file()


def ensure_venv() -> None:
    if _already_correct():
        return
    if not _is_script_run():
        return
    if os.environ.get(_GUARD) == "1":
        # We already tried to switch and are still here: something is wrong.
        # Fall through and let the normal ImportError surface, which is more
        # informative than silently looping.
        return
    if not VENV_PYTHON.exists():
        print(
            f"[bootstrap] venv not found at {VENV_PYTHON}\n"
            f"[bootstrap] create it with:  /opt/homebrew/bin/python3.11 -m venv myenv "
            f"&& ./myenv/bin/pip install -r requirements.txt",
            file=sys.stderr,
        )
        return

    os.environ[_GUARD] = "1"
    print(f"[bootstrap] switching to {VENV_PYTHON}", file=sys.stderr)
    # execv replaces this process, keeping the cwd and argv, so relative paths
    # on the command line still resolve exactly as the user typed them.
    os.execv(str(VENV_PYTHON), [str(VENV_PYTHON), *sys.argv])


ensure_venv()
