__all__ = ("ignored_attributes",)

"""
As new items.dat versions are being supported, new attributes are being added to the Item class. 
Meaning that older versions of the items.dat file will not be parsed correctly.
However, you are able to exclude attributes from being parsed for a specifc items.dat version,
by adding them to the ignored_attributes dict.

Example:
    items.dat version 15 introduces 4 new bytes to the items.dat file.
    old ignored_attributes:
        {    
            11 : ["flags3", "bodypart", "flags4", "flags5"],
            12 : ["flags4", "flags5"],
            13 : ["flags5"],
            14 : []
        }
    new ignored_attributes:
        {    
            11 : ["flags3", "bodypart", "flags4", "flags5"],
            12 : ["flags4", "flags5"],
            13 : ["flags5"],
            14 : ["flags6"],
            15 : []
        }
"""

ignored_attributes = {
    11: ["flags3", "bodypart", "flags4", "flags5", "unknown", "sit_file"],
    12: ["flags4", "flags5", "unknown", "sit_file"],
    13: ["flags5", "unknown", "sit_file"],
    14: ["unknown", "sit_file"],
    15: [],
}
