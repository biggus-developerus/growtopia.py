# growtopia.py

[![Discord server](https://discord.com/api/guilds/1009905646897999913/embed.png)](https://discord.gg/3RYSVwBCQC)

A simple asynchronous API for Growtopia, capable of creating servers, clients, and more!

Check out the [examples](examples) folder for examples on how to use this library.

## Installation

### Requirements

- [Python 3.11 or above](https://www.python.org/downloads/)

### Installing from source

For ubuntu users, use the -e flag to install the library in editable mode and avoid errors caused by the C extensions.

1. Clone the repository.
2. Open a terminal in the repository's directory
3. Install it using pip.

```powershell
git clone https://github.com/kaJob-dev/growtopia.py.git
cd growtopia.py

pip(3) install -U .
```

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
