# growtopia.py

[![Discord server](https://discord.com/api/guilds/1009905646897999913/embed.png)](https://discord.gg/3RYSVwBCQC)
[![PyPI version](https://img.shields.io/pypi/v/growtopia.py.svg?style=flat-square)](https://pypi.org/project/growtopia.py/)
[![Python versions](https://img.shields.io/pypi/pyversions/growtopia.py.svg?style=flat-square)](https://pypi.org/project/growtopia.py/)
![Tests](https://github.com/kajob-dev/growtopia.py/actions/workflows/test.yml/badge.svg)
![Build](https://github.com/kajob-dev/growtopia.py/actions/workflows/build.yml/badge.svg)
![Lint](https://github.com/kajob-dev/growtopia.py/actions/workflows/lint.yml/badge.svg)

> [!WARNING]
> Growtopia.py is still unfinished and is not ready for proper-project use. It is advised to not expect any stability from this project until it reaches a stable release (>=v0.1.6)

A simple asynchronous API for Growtopia, capable of creating servers, clients, and more!

## Installation

### Requirements

- [Python 3.11 or above](https://www.python.org/downloads/)
- [PyENet](https://github.com/kajob-dev/pyenet) (If installing growtopia.py from PyPI)

### Installing from source

1. Clone the repository.
2. Open a terminal in the repository's directory
3. Install it using pip.

```powershell
git clone https://github.com/kaJob-dev/growtopia.py.git
cd growtopia.py

pip(3) install -U .
```

### Installing from PyPI

Please do note that installing growtopia.py from PyPI will require you to install [PyENet](https://github.com/kajob-dev/pyenet) yourself, as PyPI does not support direct dependencies. This'll be resolved in the future by simply having [PyENet](https://github.com/kajob-dev/pyenet) available in PyPI too.

```powershell
pip(3) install growtopia.py
```

---

## Contributing

All contributions are welcome! If you'd like to contribute, please make a pull request.

Please make sure that your code is formatted correctly before making a new pull request. This project is formatted using [black](https://black.readthedocs.io/en/stable/) and [isort](https://pycqa.github.io/isort/) to sort imports. Read through open and closed pull requests and ensure that no one else has already made a similar pull request.

To install and format your code using black and isort, run the following commands:

```powershell
pip(3) install black
pip(3) install isort
```

```powershell
black ./growtopia
isort ./growtopia
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Thanks to

- [RebillionXX](https://github.com/RebillionXX) - For their [open-source Growtopia server](https://github.com/RebillionXX/GrowtopiaServer), which helped with the development of this project.
