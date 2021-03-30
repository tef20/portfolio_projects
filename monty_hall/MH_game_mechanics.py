import doors
import random


class Game:
    """
    Underlying game mechanics:
     - Compiles dictionary of doors.
     - Each door contains a dictionary of status information including:
         - whether the door conceals the prize (assigned True at random, otherwise False)
         - whether it's been revealed by Monty
         - whether it's been selected by the player
     - Provides methods to access and update dictionary information for in game.
     - Game can be played with arbitrary number of doors (where n > 3) to accommodate
       non-standard formats.
    """
    def __init__(self, num_of_doors=3):
        if num_of_doors < 3:
            raise ValueError('Game must involve 3 or more doors.')
        self.num_of_doors = num_of_doors
        self.door_nums = [n + 1 for n in range(num_of_doors)]
        self.doors = dict()
        self.assign_new_doors()

    def assign_new_doors(self):
        """
        Populates dictionary of door information for each door.
        Prizes assigned from randomised list: True value indicates car.
        """
        prizes = [False for dn in self.door_nums]
        # prize assigned to one door randomly
        prizes[random.randint(0, len(prizes) - 1)] = True

        self.doors = {
            door_num: {
                "prize": prizes.pop(),
                "chosen": False,
                "montys_choice": False
            }
            for door_num in self.door_nums
        }

    def check_prize(self, door_num):
        return self.doors[door_num]["prize"]

    def update_player_choice(self, new_choice):
        """
        Takes player's choice of door (int), updates "chosen" for all doors in dictionary.
        """
        previous = self.query_player_choice()

        if previous:
            if previous == new_choice:
                return

            # clear any previous choice
            self.doors[previous]["chosen"] = False

        self.doors[new_choice]["chosen"] = True

    def query_player_choice(self):
        """
        Returns player's current door choice (int).
        """
        for door in self.door_nums:
            if self.doors[door]["chosen"]:
                return door

    def update_monty_choice(self, available):
        """
        Takes list of valid doors to choose from.
        Updates dictionary to reflect Monty's choice of door(s).
        Returns choice of door (int).
        """
        choice = random.choice(available)
        self.doors[choice]["montys_choice"] = True
        return choice

    def get_selectable_doors(self, *ignore_criteria):
        """
        Takes a tuple containing criteria to filter the doors dictionary by.
        eg.:
         - Monty must select a door that is not "prize" and not "chosen".
         - Player choosing "twist" must ignore "montys_choice" and "chosen".
        Returns list of door numbers that do not conflict with criteria.
        """
        available = []
        for door in self.door_nums:
            ignore = False
            for criteria in ignore_criteria:
                if self.doors[door][criteria]:
                    ignore = True
                    break
            if not ignore:
                available.append(door)

        return available

    def query_monty_choices(self):
        """
        Returns Monty's current door choice (int), or list of choices where len(list) != 1.
        """
        choices = []
        for door in self.door_nums:
            if self.doors[door]["montys_choice"]:
                choices.append(door)

        return choices

    def check_player_won(self):
        return self.doors[self.query_player_choice()]["prize"]
