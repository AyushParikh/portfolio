# Copyright 2014 Dustin Wehr, Aidan Gomez
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Winter 2014.
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""
ConsoleController: User interface for manually solving Anne Hoy's problems
from the console.

move: Apply one move to the given model, and print any error message
to the console.
"""

# LET'S DO THISSSS!!!

from TOAHModel import TOAHModel, Cheese, IllegalMoveError


def move(model: TOAHModel, origin: int, dest: int):
    '''
    Module method to apply one move to the given model, and print any
    error message to the console.

    model - the TOAHModel that you want to modify
    origin - the stool number (indexing from 0!) of the cheese you want
             to move
    dest - the stool number that you want to move the top cheese
            on stool origin onto.
    '''
    # for the way my code works this function is unnecessary, but I used it.
    model.move(origin, dest)


class ConsoleController:
    def __init__(self: 'ConsoleController',
                 number_of_cheeses: int, number_of_stools: int):
        """
        Initialize a new 'ConsoleController'.

        number_of_cheeses - number of cheese to tower on the first stool
        number_of_stools - number of stools
        """
        # create a model and fill it's first stool
        self._model = TOAHModel(number_of_stools)
        self._model.fill_first_stool(number_of_cheeses)
        # create a _complete_model that is the completed form of _model
        self._complete_model = TOAHModel(number_of_stools)
        # make the last stool a copy of _model's first
        self._complete_model._stools[-1] = self._model._stools[0][:]

    def play_loop(self: 'ConsoleController'):
        '''
        Console-based game.
        TODO:
        -Start by giving instructions about how to enter moves (which is up to
        you). Be sure to provide some way of exiting the game, and indicate
        that in the instructions.
        -Use python's built-in function input() to read a potential move from
        the user/player. You should print an error message if the input does
        not meet the specifications given in your instruction or if it denotes
        an invalid move (e.g. moving a cheese onto a smaller cheese).
        You can print error messages from this method and/or from
        ConsoleController.move; it's up to you.
        -After each valid move, use the method TOAHModel.__str__ that we've
        provided to print a representation of the current state of the game.
        '''
        # give user the instructions to play
        print('''
            Welcome to the Tower of Cheese!

            Here are a few useful tidbits for playing the game:
            - First, you'll be asked to enter moves one-by-one into this
              console. The way these moves are to be formatted is stool1,
              stool2. That means NO SPACES, NO LETTERS, NO SPECIAL
              CHARACTERS (other than the comma). Only enter two integers
              seperated by a comma. Simple, right?
            - You'll continue this way until you have successfully moved all
              the cheeses from the first stool to the last.
            - Remember the rules of the game and don't stack larger cheeses
              on top of small ones. You'll get an error message if you do.

            Below you're presented with the current state of the game and
            will be asked to begin inputting moves. Follow the aforementioned
            format for inputting moves and play the game until you succeed.
            If at any time you wish to quit your game simply type 'quit' as
            your move. Best of luck, I wish you few moves.
            ''')
        usr_move = ""
        # until the user enters quit or wins keep intaking move commands
        while (usr_move != "quit") and (self._model != self._complete_model):
            # print the model each loop
            print(self._model)
            usr_move = input("Please enter a move: ")
            if (usr_move != "quit"):
                # try splitting at the comma as per how you input commands and
                # then try moving using those inputs, if anything doesn't work,
                # ask the user to fix their input.
                try:
                    usr_move = usr_move.split(",")
                    move(self._model, int(usr_move[0]), int(usr_move[1]))
                except:
                    print("Invalid entry")
            # if they have completed the puzzle print a congratulatory message
            if (self._model == self._complete_model):
                print("You win! Congratulations.")
        # upon completing the game or quiting, acknowledge their end of play
        print("Thank you for playing.")


if __name__ == '__main__':
    # greet the lovely players
    print('''
        Hello!
        To begin playing Tower of Cheese you'll be asked to enter a the
        number of stools and then the number of cheeses, below. Please enter
        an integer greater than or equal to 3 for the stools and an integer
        greater than or equal to 1 for the cheeses.
        ''')
    num_stools = ""
    num_cheeses = ""
    # keep taking inputs while the input does not meet the stated criteria
    while type(num_stools) != int or int(num_stools) < 3:
        num_stools = input("How many stools would you like to play with?: ")
        # if the input is not an interger or less than three ask the user to
        # correct the entry
        try:
            num_stools = int(num_stools)
            if int(num_stools) < 3:
                print("Please input an integer of at least 3")
        except ValueError:
            print("Please enter an integer.")
    # keep taking inputs while the input does not meet the stated criteria
    while type(num_cheeses) != int or int(num_cheeses) < 1:
        num_cheeses = input("How many cheeses would you like to play with?: ")
        # if the input is not an interger or less than one ask the user to
        # correct the entry
        try:
            num_cheeses = int(num_cheeses)
            if int(num_cheeses) < 1:
                print("Please input an integer of at least 1")
        except ValueError:
            print("Please enter an integer.")

    game_gen = ConsoleController(num_cheeses, num_stools)
    # show the user what they're working with
    print(game_gen._model)
    # begin the loop
    game_gen.play_loop()
