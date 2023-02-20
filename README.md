# Growtopia.py
A simple API for Growtopia, capable of creating servers, clients, and more!

# Installation
### Requirements
- [Python 3.10.7 or above](https://www.python.org/downloads/)

### Installing from source
1. Clone the repository.
2. Open a terminal in the repository's directory.
3. Run the following command:
    ```bash
    pip install -u .
    ```

# Examples
### Server
```python
# SOON
```

### Client
```python
# SOON
```

### Parser
```python
import growtopia

item_data = growtopia.ItemData("tests/data/items_v14.dat") # Represents the items.dat file
player_tribute = growtopia.PlayerTribute("tests/data/player_tribute.dat") # Represents the player_tribute.dat file

growtopia.extensions.parse(item_data, player_tribute) # Parses the items.dat file and player_tribute.dat file. Both parameters are optional, but you should parse at least one of them.

# To fetch an item from the items.dat file, you can use the following:
item = item_data.get_item("dirt") # Returns an object of Item with the name "dirt"
item = item_data.get_item(0) # Returns an object of Item with the ID 0 (blank)
```


# Contributing
All contributions are welcome! If you'd like to contribute, please make a pull request.

Please make sure that your code is formatted correctly before making a new pull request. This project is formatted using [black](https://black.readthedocs.io/en/stable/) and [isort](https://pycqa.github.io/isort/) to sort imports. Read through open and closed pull requests and ensure that no one else has already made a similar pull request. 

# License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# Versions and changelogs
## v0.1.0
    - ItemsData class, which represents the items.dat file.
    - PlayerTribute class, which represents the player_tribute.dat file.
    - Item class, which represents an item in the items.dat file.
    - Extension to parse the items.dat and player_tribute.dat files (provides the parse function)

### Major Changes
There are no major changes in this version. This is the initial release.    