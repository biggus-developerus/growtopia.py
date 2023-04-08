import growtopia

items_data = growtopia.ItemsData("items.dat")
# Represents the items.dat file

player_tribute = growtopia.PlayerTribute("player_tribute.dat")
# Represents the player_tribute.dat file

items_data.parse()  # Parse the items.dat file
player_tribute.parse()  # Parse the player_tribute.dat file


# To fetch an item from the items.dat file, you can use the following:
item = items_data.get_item("dirt")
# Returns an object of Item with the name "dirt"

item = items_data.get_item(0)
# Returns an object of Item with the ID 0 (blank)
