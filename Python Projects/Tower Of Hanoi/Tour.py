# Copyright 2013, 2014 Gary Baumgartner, Danny Heap, Dustin Wehr, Aidan Gomez
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Fall 2013.
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
from ConsoleController import ConsoleController
from GUIController import GUIController
from TOAHModel import TOAHModel

import time
import math


def tour_of_four_stools(model: TOAHModel, delay_btw_moves: float=0.5,
                        console_animate: bool=False):
    """Move a tower of cheeses from the first stool in model to the fourth.

       model - a TOAHModel with a tower of cheese on the first stool
                and three other empty stools
       console_animate - whether to use ConsoleController to animate the tour
       delay_btw_moves - time delay between moves in seconds IF
                         console_animate == True
                         no effect if console_animate == False
    """
    num_cheeses = model.number_of_cheeses()
    # if the animation is activated, print the starting model and then run the
    # animated solver for four stools. Else, run the unanimated one.
    if console_animate:
        print(model)
        time.sleep(delay_btw_moves)
        solve_four_stools_animate(model, num_cheeses, 0, 1, 2, 3,
                                  delay_btw_moves)
    else:
        solve_four_stools(model, num_cheeses, 0, 1, 2, 3)


def solve_four_stools_animate(model: TOAHModel, n: int, origin_stool: int,
                              temp_stool1: int, temp_stool2: int,
                              dest_stool: int, delay_btw_moves: float=0.5):
    '''
    solve the cheese stack problem for four stools.
    '''
    # set the i and n values. This i value is special and is found by using the
    # pattern of most efficient "i"s and manipulating it to find
    # for a given "n". Upon request I would love to explain how this was found
    # and although I can't prove it's the most efficient, it seems to hold for
    # the few we've tested.
    i = n-math.ceil(math.sqrt((2*n)+0.25)-0.5)
    new_n = n-i
    # for the first base of 1, simply use three_stool's base case
    if n == 1:
        three_stools_animate(model, n, origin_stool, temp_stool1, dest_stool,
                             delay_btw_moves)
    # for the second base of 2, use three_stool to solve
    elif n == 2:
        three_stools(model, n, origin_stool, temp_stool1, dest_stool)
    else:
        # move i cheeses to a temporary
        solve_four_stools_animate(model, i, origin_stool, dest_stool,
                                  temp_stool2, temp_stool1, delay_btw_moves)
        # move the remaining n-i to the destination
        three_stools_animate(model, new_n, origin_stool, temp_stool2,
                             dest_stool, delay_btw_moves)
        # move the i cheeses from the temporary to the destination
        solve_four_stools_animate(model, i, temp_stool1, origin_stool,
                                  temp_stool2, dest_stool, delay_btw_moves)


def solve_four_stools(model: TOAHModel, n: int, origin_stool: int,
                      temp_stool1: int, temp_stool2: int, dest_stool: int):
    '''
    solve the cheese stack problem for four stools.
    '''
    # see "solve_four_stools_animate"s comments as the functions are
    # structurally identical
    i = n-math.ceil(math.sqrt((2*n)+0.25)-0.5)
    new_n = n-i
    if n == 1:
        three_stools(model, n, origin_stool, temp_stool1, dest_stool)
    elif n == 2:
        three_stools(model, n, origin_stool, temp_stool1, dest_stool)
    else:
        solve_four_stools(model, i, origin_stool, dest_stool, temp_stool2,
                          temp_stool1)
        three_stools(model, new_n, origin_stool, temp_stool2, dest_stool)
        solve_four_stools(model, i, temp_stool1, origin_stool, temp_stool2,
                          dest_stool)


def three_stools_animate(model: TOAHModel, n: int, origin_stool: int,
                         temp_stool: int, dest_stool: int,
                         delay_btw_moves: float=0.5):
    '''
    solve the cheese stack problem for three stools.
    '''
    # credit: Brian Harrington for algorithm
    # for base case 1, simply move the cheese to the desination
    if n == 1:
        model.move(origin_stool, dest_stool)
        print(model)
        time.sleep(delay_btw_moves)
    else:
        # move n-1 cheese to a temp
        three_stools_animate(model, n-1, origin_stool, dest_stool, temp_stool,
                             delay_btw_moves)
        # move the last cheese on the origin to the destination
        model.move(origin_stool, dest_stool)
        print(model)
        time.sleep(delay_btw_moves)
        # move n-1 cheese from the temp to the destination
        three_stools_animate(model, n-1, temp_stool, origin_stool, dest_stool,
                             delay_btw_moves)


def three_stools(model: TOAHModel, n: int, origin_stool: int,
                 temp_stool: int, dest_stool: int):
    '''
    solve the cheese stack problem for three stools.
    '''
    # see "three_stools_animate"s comments as the functions are
    # structurally identical
    if n == 1:
        model.move(origin_stool, dest_stool)
    else:
        three_stools(model, n-1, origin_stool, dest_stool, temp_stool)
        model.move(origin_stool, dest_stool)
        three_stools(model, n-1, temp_stool, origin_stool, dest_stool)


if __name__ == '__main__':
    NUM_CHEESES = 3
    DELAY_BETWEEN_MOVES = .05
    CONSOLE_ANIMATE = True

    # DO NOT MODIFY THE CODE BELOW.
    four_stools = TOAHModel(3)
    four_stools.fill_first_stool(number_of_cheeses=NUM_CHEESES)

    tour_of_four_stools(four_stools,
                        console_animate=CONSOLE_ANIMATE,
                        delay_btw_moves=DELAY_BETWEEN_MOVES)

    print(four_stools.number_of_moves())
