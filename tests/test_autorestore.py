import sys

import pytest
from full_match import match

from displayhooks import autorestore_displayhook


def test_restore():
    """Restore the pre-call sys.displayhook and preserve the return value after a decorated function changes it."""
    hook_before_declaration = sys.displayhook
    result = object()

    @autorestore_displayhook
    def do_something():
        sys.displayhook = 5
        return result

    hook_before_calling = sys.displayhook

    assert do_something() is result

    assert hook_before_declaration is sys.displayhook
    assert hook_before_calling is sys.displayhook


def test_restore_after_exception():
    """Restore the pre-call sys.displayhook and propagate an exception from a decorated function that changes it."""
    hook_before_declaration = sys.displayhook

    @autorestore_displayhook
    def do_something():
        sys.displayhook = 5
        raise ValueError("message")

    hook_before_calling = sys.displayhook

    with pytest.raises(ValueError, match=match("message")):
        do_something()

    assert hook_before_declaration is sys.displayhook
    assert hook_before_calling is sys.displayhook
