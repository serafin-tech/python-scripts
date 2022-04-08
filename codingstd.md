---
marp: true
footer: 'Python Coding Standards'
---

# Python Coding Standards

Jaroslaw Wencel

---

*if something is stupid but works - it is not stupid at all*

---

Why the topic:
1. readability + standardization = quality
2. better code scales more easily
3. automation is king
4. ready-to-use examples - maybe, sometime...

---

Topics:
1. PEP-8 - naming conventions
2. logging
3. argparse
4. error processing aka try/except
5. type hints
6. linting

---
## [PEP-8](https://peps.python.org/pep-0008/)

1. indentation - 4 spaces (not tabs...)
2. line length + line breaks

```python
result = var1 \
         + var2 \
         + var3
```
3. blank lines
    1. surround top-level function and class definitions with two blank lines
    2. method definitions inside a class are surrounded by a single blank line

---
## [PEP-8](https://peps.python.org/pep-0008/)

4. import order
    1. standard library imports
    2. related third party imports
    3. local application/library specific imports

---
## [PEP-8](https://peps.python.org/pep-0008/)

5. brackets, dots & commas
```python
spam(ham[1], {eggs: 2})
foo = (0,)
if x == 4: print(x, y); x, y = y, x
dct['key'] = lst[index]
def munge(input: AnyStr): ...
def munge() -> PosInt: ...
```
---
## [PEP-8](https://peps.python.org/pep-0008/)

6. comments & docstrings
---
## [PEP-8](https://peps.python.org/pep-0008/)

### [Naming Conventions](https://peps.python.org/pep-0008/#prescriptive-naming-conventions)

1. b (single lowercase letter)
2. B (single uppercase letter)
3. lowercase
4. lower_case_with_underscores - functions, methods
5. UPPERCASE - constants
6. UPPER_CASE_WITH_UNDERSCORES - constants
7. CapitalizedWords (or CapWords, or CamelCase) - classes, TypeVariables
---
## logging

```python
import logging
logging.warning('Watch out!')  # will print a message to the console
logging.info('I told you so')  # will not print anything
```
---
## logging

```python
import logging
import logging.config

logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('simpleExample')

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')
```
---
```ini
[loggers]
keys=root,simpleExample

[handlers]
keys=consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_simpleExample]
level=DEBUG
handlers=consoleHandler
qualname=simpleExample
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```
---
## logging -> Handlers

1. StreamHandler instances send messages to streams (file-like objects).
2. FileHandler instances send messages to disk files.
3. BaseRotatingHandler is the base class for handlers that rotate log files at a certain point. Base class for RotatingFileHandler or TimedRotatingFileHandler.
4. SocketHandler/DatagramHandler instances send messages to TCP/IP sockets or UDP.
6. SMTPHandler instances send messages to a designated email address.
7. NTEventLogHandler instances send messages to a Windows NT/2000/XP event log.
8. HTTPHandler instances send messages to an HTTP server using either GET or POST semantics.
---
## commandline arguments

```python
import sys

if __name__ == "__main__":
    param1, param2 = sys.argv[1], sys.argv[2]
```

```python
import argparse

parser = argparse.ArtumentParser()
parser.add_argument('param1')
parser.add_argument('param2')

if __name__ == "__main__":
    args = parser.parse_args()
```

---
## [argparse](https://docs.python.org/3/library/argparse.html)

```python
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))
```

---
## [argparse](https://docs.python.org/3/library/argparse.html)

```
$ python prog.py -h
usage: prog.py [-h] [--sum] N [N ...]

Process some integers.

positional arguments:
 N           an integer for the accumulator

options:
 -h, --help  show this help message and exit
 --sum       sum the integers (default: find the max)
```

---
## error processing

Goog tutorial: https://docs.python.org/3/tutorial/errors.html

```python
try:
    some_code
except Exception:
    error_processong_code
else:
    executed_if_success
finally:
    last_task_before_the_try_statement_completes
```

---
## error processing - ANTIPATTERN

```python
try:
    some_code
except:
    pass
```

---
## error processing & logging

`logging.exception(msg, *args, **kwargs)`

Logs a message with level ERROR on the root logger. The arguments are interpreted as for debug(). Exception info is added to the logging message. This function should only be called from an exception handler.

---
## [PEP-484 Type Hints](https://peps.python.org/pep-0484/)

```python
from typing import TypeVar, Text

AnyStr = TypeVar('AnyStr', Text, bytes)

def concat(x: AnyStr, y: AnyStr) -> AnyStr:
    return x + y
```

---
## Python linting

[Pylint](https://pylint.pycqa.org/en/latest/) is a tool that checks for errors in Python code, tries to enforce a coding standard and looks for code smells. It can also look for certain type errors, it can recommend suggestions about how particular blocks can be refactored and can offer you details about the code's complexity.

---
## Python linting

1. in IDE (ie. PyCharm)
2. Pylint directly
3. others?

---
## references

https://github.com/SerafinSahary/PythonCodingStandards
https://www.pythoncheatsheet.org/
https://www.jetbrains.com/pycharm/
