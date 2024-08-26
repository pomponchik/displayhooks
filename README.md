# displayhooks

It's a micro library for manipulating [`sys.displayhook`](https://docs.python.org/3/library/sys.html#sys.displayhook).


## Table of contents

- [**Quick start**](#quick-start)
- [**Change the displayed value**](#change-the-displayed-value)
- [**Prohibiting the display of certain types of values**](#prohibiting-the-display-of-certain-types-of-values)
- [**Automatic recovery of the default hook**](#automatic-recovery-of-the-default-hook)


## Quick start

Install it:

```bash
pip install displayhooks
```

And use:

```python
import sys
from displayhooks import not_display

not_display(int)

sys.displayhook('Most of the adventures recorded in this book really occurred; one or two were experiences of my own, the rest those of boys who were schoolmates of mine.')
#> Most of the adventures recorded in this book really occurred; one or two were experiences of my own, the rest those of boys who were schoolmates of mine.
sys.displayhook(666)
# [nothing!]
```

## Change the displayed value

You can declaratively declare a converter function for the printed values. What it returns will be used to call the original `displayhook` function.

```python
import sys
from displayhooks import converted_displayhook
from termcolor import colored

@converted_displayhook
def new_displayhook(value: Any) -> Any:
    colored(repr(value), 'red')

sys.displayhook("What’s gone with that boy, I wonder? You TOM!")
#> What’s gone with that boy, I wonder? You TOM!
# You can't see it here, but believe me, if you repeat the code at home, the output in the console will be red!
```

If your function returns `None`, nothing will be printed.


## Prohibiting the display of certain types of values
## Automatic recovery of the default hook
