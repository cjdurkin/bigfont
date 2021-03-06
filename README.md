[![Build Status](https://travis-ci.org/cjdurkin/bigfont.svg?branch=master)](https://travis-ci.org/cjdurkin/bigfont)

# bigfont

bigfont is a pure Python library for rendering large console text
using fixed-width characters (ASCII art), similar to the programs
FIGlet or TOIlet.

## Simple usage

```text
>>> import bigfont
>>> bigfont.bigprint("hello")
  _            _  _
 | |__    ___ | || |  ___
 | '_ \  / _ \| || | / _ \
 | | | ||  __/| || || (_) |
 |_| |_| \___||_||_| \___/
```

This loads the first default font from those included in the fonts
directory of this library, and prints it.

## Loading fonts

To load a specific font from an flf file:

```text
>>> from font import font_from_file
>>> myfont = font_from_file('bigfont\\fonts\\script.flf')
>>> myfont.bigprint("text")

 _|_  _       _|_
  |  |/  /\/   |
  |_/|__/ /\_/ |_/

>>> print(myfont("more text"))

  _  _  _    __   ,_    _   _|_  _       _|_
 / |/ |/ |  /  \_/  |  |/    |  |/  /\/   |
   |  |  |_/\__/    |_/|__/  |_/|__/ /\_/ |_/


>>> txt = myfont.render('saved for later')
>>> print(txt)
                            _               _
                       |   | |             | |
  ,   __,        _   __|   | |  __   ,_    | |  __,  _|_  _   ,_
 / \_/  |  |  |_|/  /  |   |/  /  \_/  |   |/  /  |   |  |/  /  |
  \/ \_/|_/ \/  |__/\_/|_/ |__/\__/    |_/ |__/\_/|_/ |_/|__/   |_/
                           |\
                           |/
```

More fonts can be obtained from:
http://www.jave.de/figlet/fonts.html

Help in the python interpreter:

```python
import bigfont
help(bigfont)
```
