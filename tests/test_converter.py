import io
import sys
from contextlib import redirect_stdout
from typing import Any

import pytest

from displayhooks import autorestore_displayhook, converted_displayhook


@pytest.mark.parametrize(
    'value',
    [
        'kek',
        'lol',
        1,
        1.5,
    ],
)
@autorestore_displayhook
def test_empty_convert(value):
    """Identity converters preserve normal displayhook output for non-None values."""
    @converted_displayhook
    def new_displayhook(value: Any) -> Any:
        return value

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        sys.displayhook(value)

    output = buffer.getvalue()

    assert output == f'{value!r}\n'


@autorestore_displayhook
def test_empty_convert_with_none():
    """An identity converter preserves sys.displayhook's no-output behavior for None."""
    @converted_displayhook
    def new_displayhook(value: Any) -> Any:
        return value

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        sys.displayhook(None)

    output = buffer.getvalue()

    assert output == ''


@pytest.mark.parametrize(
    'value',
    [
        'kek',
        'lol',
        1,
        1.5,
    ],
)
@autorestore_displayhook
def test_elliminating_convertion(value):
    """Suppress output for non-None values when the converter returns None."""
    @converted_displayhook
    def new_displayhook(value: Any) -> Any:  # noqa: ARG001
        return None

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        sys.displayhook(value)

    output = buffer.getvalue()

    assert output == ''


@autorestore_displayhook
def test_elliminating_convertion_with_none():
    """Write no output when the input is None and the converter returns None."""
    @converted_displayhook
    def new_displayhook(value: Any) -> Any:  # noqa: ARG001
        return None

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        sys.displayhook(None)

    output = buffer.getvalue()

    assert output == ''


@pytest.mark.parametrize(
    'value',
    [
        'kek',
        'lol',
        1,
        1.5,
    ],
)
@autorestore_displayhook
def test_real_convertion(value):
    """A converted displayhook shows the converter result with normal displayhook formatting."""
    @converted_displayhook
    def new_displayhook(value: Any) -> Any:  # noqa: ARG001
        return 'cheburek'

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        sys.displayhook(value)

    output = buffer.getvalue()

    assert output == f'{"cheburek"!r}\n'
