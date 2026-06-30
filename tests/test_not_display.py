import io
import sys
from contextlib import redirect_stdout

import pytest

from displayhooks import autorestore_displayhook, not_display


@autorestore_displayhook
def test_not_display_only_ints():
    """Suppress integer displayhook output while preserving normal string output."""
    not_display(int)

    def display_something(something):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            sys.displayhook(something)

        return buffer.getvalue()

    assert display_something(5) == ''
    assert display_something('kek') == f'{"kek"!r}\n'


@pytest.mark.parametrize(
    'some_callable',
    [
        lambda: not_display(int, float),
        lambda: [not_display(int), not_display(float)],  # type: ignore[func-returns-value]
        lambda: not_display(float, int),
        lambda: [not_display(float), not_display(int)],  # type: ignore[func-returns-value]
    ],
)
@autorestore_displayhook
def test_not_display_ints_and_floats(some_callable):
    """Suppress ints and floats for combined or separate registrations in either order while preserving string output."""
    some_callable()

    def display_something(something):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            sys.displayhook(something)

        return buffer.getvalue()

    assert display_something(5) == ''
    assert display_something(5.5) == ''
    assert display_something('kek') == f'{"kek"!r}\n'
