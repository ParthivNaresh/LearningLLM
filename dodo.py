# dodo.py
import os


# -----------------------------------------------------------------------------
# Task: Install Requirements
# -----------------------------------------------------------------------------
def task_install_requirements():
    """
    Installs packages from requirements.txt.
    """
    return {
        "actions": ["pip install -r requirements.txt"],
        "verbosity": 2,
    }


# -----------------------------------------------------------------------------
# Task: Lint (Black, Flake8, isort)
# -----------------------------------------------------------------------------
def task_lint():
    """
    Lint code with Black, Flake8, and isort (assuming they're in dev deps).
    """
    return {
        "actions": [
            "black --check .",
            "flake8 .",
            "isort --check-only .",
        ],
        "verbosity": 2,
    }


def task_lint_fix():
    """
    Lint code with Black, Flake8, and isort (assuming they're in dev deps).
    """
    return {
        "actions": [
            "black .",
            "isort .",
        ],
        "verbosity": 2,
    }


# -----------------------------------------------------------------------------
# Task: Test (Pytest)
# -----------------------------------------------------------------------------
def task_test():
    """
    Run tests with pytest.
    """
    return {
        "actions": ["pytest --maxfail=1 --disable-warnings -q"],
        "verbosity": 2,
    }


# -----------------------------------------------------------------------------
# Task: Build Distribution
# -----------------------------------------------------------------------------
def task_build():
    """
    Build wheel and source distribution using 'build'.
    """
    return {
        "actions": ["python -m build"],
        "verbosity": 2,
    }


# -----------------------------------------------------------------------------
# Task: Docs (MkDocs or Sphinx)
# -----------------------------------------------------------------------------
def task_docs():
    """
    Build documentation.
    Adjust command for your doc generator (MkDocs vs Sphinx).
    """
    # Example: MkDocs
    return {
        "actions": ["mkdocs build"],
        "verbosity": 2,
    }
