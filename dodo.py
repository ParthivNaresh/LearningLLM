# dodo.py


# -----------------------------------------------------------------------------
# Task: Install Requirements
# -----------------------------------------------------------------------------
def task_install():
    """
    Updates and installs packages from requirements.txt.
    """
    return {
        "actions": [
            "pip-compile --upgrade requirements.in",
            "pip install -r requirements.txt",
        ],
        "verbosity": 2,
    }


def task_install_test():
    """
    Updates and installs packages from requirements-test.txt.
    """
    return {
        "actions": [
            "pip-compile --upgrade requirements-test.in",
            "pip install -r requirements-test.txt",
        ],
        "verbosity": 2,
    }


# -----------------------------------------------------------------------------
# Task: Lint (Black, Flake8, isort)
# -----------------------------------------------------------------------------
def task_lint():
    """
    Lint code with Black, Flake8, and isort.
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
    Fix code with Black and isort.
    """
    return {
        "actions": [
            "black .",
            "isort .",
        ],
        "verbosity": 2,
    }


def task_clear_logs():
    """
    Deletes all files under the 'tests/logs/' folder.
    """
    return {
        "actions": ["rm -rf tests/logs/*"],
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
