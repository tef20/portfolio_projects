import MH_game_mechanics as mhgm
import re
import time


def main():
    """
    Play Let's Make a Deal! as made famous in the Monty Hall problem.
    """
    game = mhgm.Game()

    run_intro(game)
    first_round(game)
    montys_intervention(game)
    second_round(game)
    final_reveal(game)


def run_intro(game):
    """
     - Welcome message + presentation of doors.
    """
    print("\nWelcome to Let's Make a Deal!\n")
    input("(Press enter to continue...)\n")
    print("In front of you are 3 doors: ")
    list_remaining_doors(game, revealed=False)
    input("...\n")
    print("\nBehind one of the doors is a brand new car! Behind the others are goats...")
    input("...\n")


def first_round(game):
    """
     - Player prompted to select door.
     - game updated.
    """
    player_choice_1 = get_first_choice(game.door_nums)
    game.update_player_choice(player_choice_1)
    input("...\n")


def montys_intervention(game):
    """
     - Monty selects doors to open, revealing booby prizes. Leaves players first choice
    and one other door unopened.
     - game updated.
    """
    print("Monty has offered to open one of the remaining doors!\n")
    available = game.get_selectable_doors("prize", "chosen")
    while len(game.get_selectable_doors("montys_choice")) > 2:
        montys_choice = game.update_monty_choice(available)
        print(f'He opens Door #{montys_choice} and reveals a goat!')
        available.remove(montys_choice)
    input("...\n")


def second_round(game):
    """
     - Player prompted to stick with original choice or switch to the other option.
     - game updated.
    """
    print(f'There remain two unopened doors: ')
    list_remaining_doors(game, "montys_choice")
    old_choice = game.query_player_choice()
    new_choice = input("\nWould you like to stick or twist? ")
    while not re.fullmatch(r"stick|twist", new_choice, re.IGNORECASE):
        new_choice = input(f"Enter 'stick' to stick with Door {old_choice} or 'twist' to change: ")
    player_choice_2 = stick_or_twist(old_choice, new_choice, game)
    game.update_player_choice(player_choice_2)
    print()


def final_reveal(game):
    """
    - Dramatic final prize reveal.
    """
    print("You won", end='', flush=True)
    time.sleep(0.5)
    print(".", end='', flush=True)
    time.sleep(0.5)
    print(".", end='', flush=True)
    time.sleep(0.5)
    print(". ", end='', flush=True)
    time.sleep(0.5)
    if game.check_player_won():
        print("a car!", end='', flush=True)
    else:
        print("a goat!", end='', flush=True)
    time.sleep(1)
    print('\n')


def list_remaining_doors(game, *ignore_list, revealed=False):
    """
    Takes list of ignore criteria and prints doors available for selection.
    revealed option reveals prize for debug purposes.
    """
    for door_num in game.get_selectable_doors(*ignore_list):
        print(f" - Door #{door_num}", end='')
        if revealed:
            print(f": {game.doors[door_num]['prize']}")
        else:
            # print new line if prize not appended
            print()


def get_first_choice(door_nums):
    """
    Takes
    """
    while True:
        try:
            choice = int(input("Choose a door # to open: "))
        except ValueError:
            print("Please enter a digit only.")
            continue
        else:
            if choice in door_nums:
                print(f'You chose Door #{choice}!')
                return choice
            else:
                print(f"{choice} isn't an available door!")


def stick_or_twist(old_choice, new_choice, game):
    """
    Takes old_choice (int) and new_choice (str).
    Returns door choice as int based on player's choice.
    """
    if new_choice.lower() == "stick":
        return old_choice

    twist = game.get_selectable_doors("montys_choice", "chosen")[0]
    return twist


if __name__ == '__main__':
    main()