#!/usr/bin/python3

from player import *
from items import *
from gameparser import *


def list_of_items(items):
    """This function takes a list of items (see items.py for the definition) and
    returns a comma-separated list of item names (as a string). For example:

   # >>> list_of_items([item_pen, item_handbook])
    'a pen, a student handbook'

   # >>> list_of_items([item_id])
    'id card'

   # >>> list_of_items([])
    ''

   # >>> list_of_items([item_money, item_handbook, item_laptop])
    'money, a student handbook, laptop'

    """
    item_names = [item["name"] for item in items]
    # ^ item_names loops through each item in items.py assigning each key and value in the dictionary to item
    # ^ it then looks for value associated with "name"
    return ", ".join(item_names)  # .join() joins item_names together with the specified string


def print_room_items(room):
    """This function takes a room as an input and nicely displays a list of items
    found in this room (followed by a blank line). If there are no items in
    the room, nothing is printed. See map.py for the definition of a room, and
    items.py for the definition of an item. This function uses list_of_items()
    to produce a comma-separated list of item names. For example:

   # >>> print_room_items(rooms["Reception"])
    There is a pack of biscuits, a student handbook here.
    <BLANKLINE>

   # >>> print_room_items(rooms["Office"])
    There is a pen here.
    <BLANKLINE>

   # >>> print_room_items(rooms["Admins"])

    (no output)

    Note: <BLANKLINE> here means that doctest should expect a blank line.

    """
    items = room["items"]  # pulls items from the room
    if len(items) > 0:  # checks if the length of items is greater than 0
        item_name = list_of_items(items)
        # ^ item_name uses list_of_items to return the list of items as a string
        print("There is", item_name, "here.\n")  # prints what is in the room


def print_inventory_items(items):
    """This function takes a list of inventory items and displays it nicely, in a
    manner similar to print_room_items(). The only difference is in formatting:
    print "You have ..." instead of "There is ... here.". For example:

   # >>> print_inventory_items(inventory)
    You have id card, laptop, money.
    <BLANKLINE>

    """
    if len(inventory) == 0:  # if the length of the inventory list is equal to 0
        print("You have no items in your inventory.\n")  # says you have no items
    else:  # otherwise there are items
        item_name = list_of_items(inventory)  # uses list_of_items function again
        print("You have:", item_name + ".\n")  # prints what the player has in their inventory


def print_room(room):
    """This function takes a room as an input and nicely displays its name
    and description. The room argument is a dictionary with entries "name",
    "description" etc. (see map.py for the definition). The name of the room
    is printed in all capitals and framed by blank lines. Then follows the
    description of the room and a blank line again. If there are any items
    in the room, the list of items is printed next followed by a blank line
    (use print_room_items() for this). For example:

   # >>> print_room(rooms["Office"])
    <BLANKLINE>
    THE GENERAL OFFICE
    <BLANKLINE>
    You are standing next to the cashier's till at
    30-36 Newport Road. The cashier looks at you with hope
    in their eyes. If you go west you can return to the
    Queen's Buildings.
    <BLANKLINE>
    There is a pen here.
    <BLANKLINE>

   # >>> print_room(rooms["Reception"])
    <BLANKLINE>
    RECEPTION
    <BLANKLINE>
    You are in a maze of twisty little passages, all alike.
    Next to you is the School of Computer Science and
    Informatics reception. The receptionist, Matt Strangis,
    seems to be playing an old school text-based adventure
    game on his computer. There are corridors leading to the
    south and east. The exit is to the west.
    <BLANKLINE>
    There is a pack of biscuits, a student handbook here.
    <BLANKLINE>

   # >>> print_room(rooms["Admins"])
    <BLANKLINE>
    MJ AND SIMON'S ROOM
    <BLANKLINE>
    You are leaning agains the door of the systems managers'
    room. Inside you notice Matt "MJ" John and Simon Jones. They
    ignore you. To the north is the reception.
    <BLANKLINE>

    Note: <BLANKLINE> here means that doctest should expect a blank line.
    """
    # Display room name
    print()
    print(room["name"].upper())
    print()
    # Display room description
    print(room["description"])
    print()

    if "items" in room and len(room["items"]) > 0:
        # ^ if "items" key is present in the room dictionary
        # ^ if the length of items list is greater than 0
        print_room_items(room)
        # ^ calls print_room_items which prints the items that are in the room

    max_weight = 2.6
    print("Your current inventory weight is: ", total_inventory_weight(inventory), "kg /", max_weight, "kg.")


def exit_leads_to(exits, direction):
    """This function takes a dictionary of exits and a direction (a particular
    exit taken from this dictionary). It returns the name of the room into which
    this exit leads. For example:

   # >>> exit_leads_to(rooms["Reception"]["exits"], "south")
    "MJ and Simon's room"
   # >>> exit_leads_to(rooms["Reception"]["exits"], "east")
    "your personal tutor's office"
   # >>> exit_leads_to(rooms["Tutor"]["exits"], "west")
    'Reception'
    """
    return rooms[exits[direction]]["name"]


def print_exit(direction, leads_to):
    """This function prints a line of a menu of exits. It takes a direction (the
    name of an exit) and the name of the room into which it leads (leads_to),
    and should print a menu line in the following format:

    GO <EXIT NAME UPPERCASE> to <where it leads>.

    For example:
   # >>> print_exit("east", "you personal tutor's office")
    GO EAST to you personal tutor's office.
   # >>> print_exit("south", "MJ and Simon's room")
    GO SOUTH to MJ and Simon's room.
    """
    print("GO " + direction.upper() + " to " + leads_to + ".")


def print_menu(exits, room_items, inv_items):
    """This function displays the menu of available actions to the player. The
    argument exits is a dictionary of exits as exemplified in map.py. The
    arguments room_items and inv_items are the items lying around in the room
    and carried by the player respectively. The menu should, for each exit,
    call the function print_exit() to print the information about each exit in
    the appropriate format. The room into which an exit leads is obtained
    using the function exit_leads_to(). Then, it should print a list of commands
    related to items: for each item in the room print

    "TAKE <ITEM ID> to take <item name>."

    and for each item in the inventory print

    "DROP <ITEM ID> to drop <item name>."

    For example, the menu of actions available at the Reception may look like this:

    You can:
    GO EAST to your personal tutor's office.
    GO WEST to the parking lot.
    GO SOUTH to MJ and Simon's room.
    TAKE BISCUITS to take a pack of biscuits.
    TAKE HANDBOOK to take a student handbook.
    DROP ID to drop your id card.
    DROP LAPTOP to drop your laptop.
    DROP MONEY to drop your money.
    What do you want to do?

    """
    print("You can:")
    # Iterate over available exits
    for direction in exits:
        # Print the exit name and where it leads to
        print_exit(direction, exit_leads_to(exits, direction))

    for item in room_items:  # loops through the items in the room
        print("TAKE", item["id"].upper(), "to take", item["name"] + ".")
        # ^ prints the above string

    for item in inv_items:  # loops through items in the inventory
        print("DROP", item["id"].upper(), "to drop", item["name"] + ".")

    for item in inv_items:
        # ^ I have done the exact same for loop again, so it doesn't print DROP, READ, DROP, READ etc.
        print("READ", item["id"].upper(), "to read the description of", item["name"] + ".")

    print("What do you want to do?")


def is_valid_exit(exits, chosen_exit):
    """This function checks, given a dictionary "exits" (see map.py) and
    a players's choice "chosen_exit" whether the player has chosen a valid exit.
    It returns True if the exit is valid, and False otherwise. Assume that
    the name of the exit has been normalised by the function normalise_input().
    For example:

   # >>> is_valid_exit(rooms["Reception"]["exits"], "south")
    True
   # >>> is_valid_exit(rooms["Reception"]["exits"], "up")
    False
   # >>> is_valid_exit(rooms["Parking"]["exits"], "west")
    False
   # >>> is_valid_exit(rooms["Parking"]["exits"], "east")
    True
    """
    return chosen_exit in exits


def total_inventory_weight(inventory):
    # ^ new function to get the current weight of items in players inventory
    return sum(item["weight"] for item in inventory)
    # ^ adds up the "weight" value for each item in the inventory


def execute_go(direction):
    """This function, given the direction (e.g. "south") updates the current room
    to reflect the movement of the player if the direction is a valid exit
    (and prints the name of the room into which the player is
    moving). Otherwise, it prints "You cannot go there."
    """
    global current_room
    if is_valid_exit(current_room["exits"], direction):
        # ^ call is_valid_exit to check if the direction exists in the current room's exits dictionary
        current_room = rooms[current_room["exits"][direction]]
        # ^ current_room becomes the new room
        # ^ the new room is found using direction as the key in "exits" to retrieve the value (the room)
    else:
        print("You cannot go there.")


def execute_take(item_id):
    """This function takes an item_id as an argument and moves this item from the
    list of items in the current room to the player's inventory. However, if
    there is no such item in the room, this function prints
    "You cannot take that."
    """

    max_weight = 2.6  # testing

    item_taken = None  # item_taken variable is set as none
    for item in current_room["items"]:  # loops through the items in current_room (player.py)
        if item["id"] == item_id:
            # ^ if the item id is equal to item_id that the user tried to take
            item_taken = item  # item taken becomes the item (not None)
            break  # break ends the loop
    if item_taken is not None:
        # print(item_taken) used this to test when it wasn't working
        if total_inventory_weight(inventory) + item_taken["weight"] <= max_weight:
            # ^ if the current inventory weight of the player plus the item being taken weight are less than max_weight
            current_room["items"].remove(item_taken)  # removes the item from the current_room
            inventory.append(item_taken)  # appends this to the player's inventory (player.py)
            print("You took", item_taken["name"] + ".")
        else:
            print("You would be too heavy if you took that.")
    else:
        print("You cannot take that.")


def execute_drop(item_id):
    """This function takes an item_id as an argument and moves this item from the
    player's inventory to list of items in the current room. However, if there is
    no such item in the inventory, this function prints "You cannot drop that."
    """

    max_weight = 2.6

    item_dropped = None  # item_dropped variable is set to None
    for item in inventory:
        if item["id"] == item_id:  # if the item id is equal to item_id
            item_dropped = item  # item_dropped becomes item (not None)
            break  # end the loop
    if item_dropped is not None:
        inventory.remove(item_dropped)  # remove item_dropped from players inventory
        current_room["items"].append(item_dropped)
        # ^ append the item into the current room's room item dictionary
        print("You dropped", item_dropped["name"] + ".")
    else:
        print("You cannot drop that.")


def execute_read(item_id):
    item_read = None  # pretty much a copy of the above ones
    for item in inventory:
        if item["id"] == item_id:
            item_read = item
            break
    if item_read is not None:
        print(item_read["description"])
        print("This item weights: ", item_read["weight"], "kg.")
        #  ^ tells the player how much the item weighs
    else:
        print("You cannot read that.")


def execute_command(command):
    """This function takes a command (a list of words as returned by
    normalise_input) and, depending on the type of action (the first word of
    the command: "go", "take", or "drop"), executes either execute_go,
    execute_take, or execute_drop, supplying the second word as the argument.

    """

    if 0 == len(command):
        return

    if command[0] == "go":
        if len(command) > 1:
            execute_go(command[1])
        else:
            print("Go where?")

    elif command[0] == "take":
        if len(command) > 1:
            execute_take(command[1])
        else:
            print("Take what?")

    elif command[0] == "drop":
        if len(command) > 1:
            execute_drop(command[1])
        else:
            print("Drop what?")

    elif command[0] == "read":
        if len(command) > 1:
            execute_read(command[1])
        else:
            print("Read what?")

    else:
        print("This makes no sense.")


def menu(exits, room_items, inv_items):
    """This function, given a dictionary of possible exits from a room, and a list
    of items found in the room and carried by the player, prints the menu of
    actions using print_menu() function. It then prompts the player to type an
    action. The players's input is normalised using the normalise_input()
    function before being returned.

    """

    # Display menu
    print_menu(exits, room_items, inv_items)

    # Read player's input
    user_input = input("> ")

    # Normalise the input
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input


def move(exits, direction):
    """This function returns the room into which the player will move if, from a
    dictionary "exits" of avaiable exits, they choose to move towards the exit
    with the name given by "direction". For example:

   # >>> move(rooms["Reception"]["exits"], "south") == rooms["Admins"]
    True
   # >>> move(rooms["Reception"]["exits"], "east") == rooms["Tutor"]
    True
   # >>> move(rooms["Reception"]["exits"], "west") == rooms["Office"]
    False
    """

    # Next room to go to
    return rooms[exits[direction]]


# This is the entry point of our program
def main():
    # Main game loop
    while True:
        # Display game status (room description, inventory etc.)
        print_room(current_room)
        print_inventory_items(inventory)

        # Show the menu with possible actions and ask the player
        command = menu(current_room["exits"], current_room["items"], inventory)

        # Execute the player's command
        execute_command(command)


# Are we being run as a script? If so, run main().
# '__main__' is the name of the scope in which top-level code executes.
# See https://docs.python.org/3.4/library/__main__.html for explanation
if __name__ == "__main__":
    main()
