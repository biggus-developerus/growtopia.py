# growtopia.py
[![](https://discord.com/api/guilds/1009905646897999913/embed.png)](https://discord.gg/3RYSVwBCQC)

A simple asynchronous API for Growtopia, capable of creating servers, clients, and more! 

# Installation
### Requirements
- [Python 3.11 or above](https://www.python.org/downloads/)

### Installing from source

1. Clone the repository.
2. Open a terminal in the repository's directory
3. Install it using pip.

```powershell
git clone https://github.com/kaJob-dev/growtopia.py.git
cd growtopia.py

make install
-- or --
pip(3) install -U .
```

# Examples
### Server
```python
import growtopia

server = growtopia.Server(("127.0.0.1", 10000))


@server.listener
async def on_server_ready(ctx: growtopia.Context):
    print(f"The server is now running on {ctx.server.address}")


@server.listener
async def on_connect(ctx: growtopia.Context):
    print(f"{ctx.peer.address} has connected to the server!")


@server.listener
async def on_disconnect(ctx: growtopia.Context):
    print(f"{ctx.peer.address} has disconnected from the server!")


@server.listener
async def on_receive(ctx: growtopia.Context):
    print(f"{ctx.peer.address} sent a packet: {ctx.enet_packet.data}")


server.start()
```

### Client
```python
# SOON
```

### Parser
```python
import growtopia

item_data = growtopia.ItemData("items.dat") 
# Represents the items.dat file

player_tribute = growtopia.PlayerTribute("player_tribute.dat") 
# Represents the player_tribute.dat file

growtopia.extensions.parse(item_data, player_tribute) 
# Parses the items.dat and player_tribute.dat files. 
# Both parameters are optional, but you should parse at least one of them.

# To fetch an item from the items.dat file, you can use the following:
item = item_data.get_item("dirt") 
# Returns an object of Item with the name "dirt"

item = item_data.get_item(0) 
# Returns an object of Item with the ID 0 (blank)
```


# Contributing
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

# License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# Thanks to
- [RebillionXX](https://github.com/RebillionXX) - For their [open-source Growtopia server](https://github.com/RebillionXX/GrowtopiaServer), which helped with the development of this project.

# TODO
- [ ] Finish the client
- [ ] Add more examples and tests
- [ ] Document functions and classes
- [ ] Add a from_bytes function to both the variant and variant list