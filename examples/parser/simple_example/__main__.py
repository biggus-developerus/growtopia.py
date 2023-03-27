import growtopia

item_data = growtopia.ItemsData("items.dat")
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
