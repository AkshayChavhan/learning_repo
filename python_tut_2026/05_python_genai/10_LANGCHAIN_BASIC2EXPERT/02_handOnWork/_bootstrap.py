"""Re-launch the current script under this project's venv, if it isn't already.

Why this exists
---------------
The packages here need Python >= 3.10, and this machine's system python3 is
3.8.10 - so `python3 some_script.py` from a shell where the venv is not
activated dies with:

    ModuleNotFoundError: No module named 'langchain_google_genai'

Installing the packages system-wide is not an option: 3.8 is below the minimum
the libraries support. The only interpreter that can run this project is
myenv/bin/python (3.12).

So instead of asking you to remember `source myenv/bin/activate`, importing
this module restarts the process under the right interpreter automatically.

Usage - import it BEFORE any third-party import, right after the sys.path
block that every script in src/ already has:

    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))

    import _bootstrap          # noqa: F401  - must precede langchain imports

Trade-off worth knowing: this hides which interpreter you are on, which is a
thing worth understanding rather than papering over. Activating the venv is
still the "proper" habit - `which python3` should point inside myenv/. This is
a convenience so a forgotten activation is not a dead end.
"""

import os
import sys
from pathlib import Path

# The venv lives next to this file, at the project root.
VENV_PYTHON = Path(__file__).resolve().parent / "myenv" / "bin" / "python"

# Set once before re-exec so a failed switch cannot loop forever.
_GUARD = "_HANDONWORK_BOOTSTRAPPED"


def _already_correct() -> bool:
    """True if the running interpreter IS the venv one."""
    try:
        return Path(sys.executable).resolve() == VENV_PYTHON.resolve()
    except OSError:
        return True  # cannot tell - do not risk an exec loop


def _is_script_run() -> bool:
    """True only when python was given a real script file to run.

    Re-exec rebuilds the command from sys.argv, and that only round-trips for
    `python foo.py`. Under `python -c "..."` argv[0] is "-c" and the code
    itself is not in argv at all, so replaying it would run the wrong thing.
    Under `-m`, argv[0] is already rewritten to the module's file. Interactive
    and stdin sessions give "" or "-". In those cases, do nothing and let the
    normal ImportError appear.
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
            f"[bootstrap] create it with:  python3 -m venv myenv && "
            f"source myenv/bin/activate && pip install -r requirements.txt",
            file=sys.stderr,
        )
        return

    os.environ[_GUARD] = "1"
    # execv replaces this process, keeping the cwd and argv, so relative paths
    # on the command line still resolve exactly as the user typed them.
    os.execv(str(VENV_PYTHON), [str(VENV_PYTHON), *sys.argv])


ensure_venv()
