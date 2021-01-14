#!/usr/bin/env python
"""
The universe of the Game of Life is an infinite two-dimensional orthogonal grid of square cells,
each of which is in one of two possible states, alive or dead (populated or unpopulated).
Every cell interacts with its eight neighbours, which are the cells that are horizontally,
vertically, or diagonally adjacent.

At each step in time, the following transitions occur:

****************************************************************************************************
   1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
   2. Any live cell with two or three live neighbours lives on to the next generation.
   3. Any live cell with more than three live neighbours dies, as if by overpopulation.
   4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
****************************************************************************************************

The initial pattern constitutes the seed of the system.

The first generation is created by applying the above rules simultaneously to every cell in the
seed—births and deaths occur simultaneously, and the discrete moment at which this happens is
sometimes called a tick. The rules continue to be applied repeatedly to create further generations.

You run this script as a module:
    python -m Project.gol.py
"""

import argparse
import random
import json
import logging
import itertools
from pathlib import Path
from ast import literal_eval
from time import sleep
from itertools import product

import Project.code_base as cb

__version__ = '1.0'
__desc__ = "A simplified implementation of Conway's Game of Life."

RESOURCES = Path(__file__).parent / "../_Resources/"


# -----------------------------------------
# IMPLEMENTATIONS FOR HIGHER GRADES, C - B
# -----------------------------------------

def load_seed_from_file(_file_name: str) -> tuple:
    """ Load population seed from file. Returns tuple: population (dict) and world_size (tuple). """
    file_name = _file_name if ".json" in _file_name else _file_name + ".json"  # Taking lack of .json into consideration
    file_path = RESOURCES / file_name  # Path to resource folder, ending with the selected file name

    with open(file_path, "r") as file:  # Open file with read permission
        data = json.load(file)
        raw_population: dict = data["population"]
        parsed_population: dict = {}
        for key in raw_population:
            if raw_population[key] is not None:
                # Convert the neighbor strings to tuples
                neighbours: list = list(tuple(i) for i in raw_population[key]["neighbours"])
                parsed_population[literal_eval(key)] = {  # Create the correct population dict from the parsed data
                    "state": raw_population[key]["state"],
                    "neighbours": neighbours
                }
            else:
                parsed_population[literal_eval(key)] = cb.STATE_RIM  # If state = None, Rim-cell
        seed: tuple = parsed_population, data["world_size"]  # Parsed population dict and world size from file as tuple
        return seed


def create_logger() -> logging.Logger:
    """ Creates a logging object to be used for reports. """
    file_path = RESOURCES / "gol.log"  # Create file path with file name and path to Resources folder
    gol_logger = logging.getLogger("gol_logger")  # Create logger object
    gol_logger.setLevel(logging.INFO)  # Logging level set to INFO
    file_handler = logging.FileHandler(file_path)  # Make sure that the logger logs to the correct path
    gol_logger.addHandler(file_handler)  # Add the file handler to the logger object
    return gol_logger


def simulation_decorator(func):
    """ Function decorator, used to run full extent of simulation. """
    def wrapper(nth_generation: int, population: dict, world_size: tuple):
        gol_logger = create_logger()  # Get the logger object
        current_population: dict = population  # Dict to contain every new population state

        for i in range(0, nth_generation):  # Iterate the specified generation ammount
            cb.clear_console()
            population_count: int = 0  # Counters of states to be logged
            alive_count: int = 0
            elder_count: int = 0
            prime_elder_count: int = 0
            dead_count: int = 0
            for coords in current_population:  # Iterate through the dict
                if current_population[coords] is not cb.STATE_RIM:  # Rim cells shouldnt be counted at all
                    population_count += 1
                    if current_population[coords]["state"] != cb.STATE_DEAD:  # If state is considered alive
                        alive_count += 1
                        if current_population[coords]["state"] == cb.STATE_ELDER:
                            elder_count += 1
                        elif current_population[coords]["state"] == cb.STATE_PRIME_ELDER:
                            prime_elder_count += 1
                    else:  # If state is dead
                        dead_count += 1

            gol_logger.info(f"GENERATION {i} \n"  # Format and log the cell data per generation
                            f"  Population: {population_count} \n"
                            f"  Alive: {alive_count} \n"
                            f"  Elders: {elder_count} \n"
                            f"  Prime Elders: {prime_elder_count} \n"
                            f"  Dead: {dead_count}")

            # Calls the wrapped function (run_simulation) to update the population state
            current_population = func(i, current_population, world_size)
            sleep(0.2)  # Wait 200ms before next cycle

    return wrapper


# -----------------------------------------
# BASE IMPLEMENTATIONS
# -----------------------------------------

def parse_world_size_arg(_arg: str) -> tuple:
    """ Parse width and height from command argument. """
    args: list = _arg.split("x")  # Split the world size arg into a list by "x"

    try:
        for i in range(len(args)):  # Iterate the split args
            if len(args) != 2 or args[i] == "":  # If not 2 items, or blank args
                raise AssertionError
            if not isinstance(int(args[i]), int) or int(args[i]) < 1:  # If arg not int, or value below 1
                raise ValueError
        return int(args[0]), int(args[1])  # Return int-parsed args as tuple
    except AssertionError:
        print("World size should contain width and height, separated by ‘x’. Ex: ‘80x40’")
    except ValueError as error:
        msg: str = "Both width and height needs to have positive values above zero."
        print(error) if (len(str(error)) > 0) else print(msg)  # If error contains a message

    print("Using default world size: 80x40")
    sleep(1)  # Making sure that the user gets to see their wrongdoings
    return 80, 40  # Return default values as tuple


def populate_world(_world_size: tuple, _seed_pattern: str = None) -> dict:
    """ Populate the world with cells and initial states. """
    population: dict = {}  # Empty dict to be filled with population data
    pattern: list = []  # List to be filled with a predefined pattern, if any
    if _seed_pattern:  # If a pattern has been specified
        pattern: list = cb.get_pattern(_seed_pattern, _world_size)  # Get the specified pattern

    # List every possible world size coordinate on the grid from 0,0 to the specified range
    coords: list = list(product(range(0, _world_size[1]), range(0, _world_size[0])))
    for i in range(len(coords)):  # Iterate through the coordinates
        # If edge cell (containing 0, or max world size value - 1)
        if coords[i][0] == 0 \
                or coords[i][0] == _world_size[1] - 1 \
                or coords[i][1] == 0 \
                or coords[i][1] == _world_size[0] - 1:
            population[coords[i]] = cb.STATE_RIM  # Edge cell -> Rim cell
        else:
            if pattern:  # If there is a specified pattern
                population[coords[i]] = {
                    # Alive cell if existing in pattern, dead if not
                    "state": cb.STATE_ALIVE if coords[i] in pattern else cb.STATE_DEAD,
                    "neighbours": calc_neighbour_positions(coords[i]),  # Gets the neighbouring cells
                    "age": 0  # The cells default age
                }
            else:
                population[coords[i]] = {
                    # Alive cell if random number between 15 and 20, dead if not
                    "state": cb.STATE_ALIVE if random.randint(0, 21) >= 15 else cb.STATE_DEAD,
                    "neighbours": calc_neighbour_positions(coords[i]),  # Gets the neighbouring cells
                    "age": 0  # The cells default age
                }
    return population


def calc_neighbour_positions(_cell_coord: tuple) -> list:
    """ Calculate neighbouring cell coordinates in all directions (cardinal + diagonal).
    Returns list of tuples. """
    # Finds every neighbouring cell to the inserted coordinate tuple
    # Assumes that a rim cell isnt ever going to be evaluated in this function
    neighbors: list = [
        (_cell_coord[0] - 1, _cell_coord[1] - 1),
        (_cell_coord[0] - 1, _cell_coord[1]),
        (_cell_coord[0] - 1, _cell_coord[1] + 1),
        (_cell_coord[0], _cell_coord[1] - 1),
        (_cell_coord[0], _cell_coord[1] + 1),
        (_cell_coord[0] + 1, _cell_coord[1] - 1),
        (_cell_coord[0] + 1, _cell_coord[1]),
        (_cell_coord[0] + 1, _cell_coord[1] + 1),
    ]
    return neighbors


@simulation_decorator  # Decorator wrapping the function
def run_simulation(_generations: int, _population: dict, _world_size: tuple) -> dict:
    """ Runs a tick in the simulation. """
    return update_world(_population, _world_size)  # Returns the dict from update_world function


def update_world(_cur_gen: dict, _world_size: tuple) -> dict:
    """ Represents a tick in the simulation. """
    next_generation: dict = {}  # Dict to contain the next generation
    for key in _cur_gen:  # Iterate the current generation

        # Defines the output to be printed
        out_str: str = cb.get_print_value(cb.STATE_RIM) if _cur_gen[key] is cb.STATE_RIM \
            else cb.get_print_value(_cur_gen[key]["state"])
        # Print out_str, line break if cell is a x-row right edge cell
        cb.progress(out_str + "\n" if key[1] == _world_size[0] - 1 else out_str)

        # Next gen calculations
        if _cur_gen[key] is cb.STATE_RIM:  # If the cell is a rim, it should continue to be so
            next_generation[key] = cb.STATE_RIM
        else:  # If not a rim cell
            # Count the cells living neighbors
            living: int = count_alive_neighbours(_cur_gen[key]["neighbours"], _cur_gen)

            # If the current generation should be considered alive according to the stated rules
            if _cur_gen[key]["state"] != cb.STATE_DEAD and 2 <= living <= 3 \
                    or _cur_gen[key]["state"] == cb.STATE_DEAD and living == 3:

                try:  # Try to get the cells age value
                    age: int = _cur_gen[key]["age"] + 1  # Ages the cell by 1
                except KeyError:  # If the age value isnt specified in the dict, create an age value
                    age: int = 1  # This will only be hit during the 2nd generation, therefore age = 1

                next_generation[key] = {  # Initialize the creation of a new generation to tict
                    "neighbours": _cur_gen[key]["neighbours"],  # Current gens neighbours is still valid
                    "age": age  # The age value
                }

                # Defines the cells state depending on its age
                if age < 5:
                    next_generation[key]["state"] = cb.STATE_ALIVE
                elif 5 <= age <= 9:
                    next_generation[key]["state"] = cb.STATE_ELDER
                else:
                    next_generation[key]["state"] = cb.STATE_PRIME_ELDER
            else:  # If not considered alive according to rules
                next_generation[key] = {
                    "state": cb.STATE_DEAD,
                    "neighbours": _cur_gen[key]["neighbours"],
                    "age": 0  # Age reverted to 0
                }
    return next_generation


def count_alive_neighbours(_neighbours: list, _cells: dict) -> int:
    """ Determine how many of the neighbouring cells are currently alive. """
    living: int = 0  # Variable to contain the ammount of living neighbours

    for coords in _neighbours:  # Iterate through the cells neighbors
        #  If the neighbor isnt dead, and not a rim
        if _cells[coords] is not cb.STATE_RIM and _cells[coords]["state"] != cb.STATE_DEAD:
            living += 1  # Increment the living neighbours by 1
    return living


def main():
    """ The main program execution. YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!! """
    epilog = "DT179G Project v" + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('-g', '--generations', dest='generations', type=int, default=50,
                        help='Amount of generations the simulation should run. Defaults to 50.')
    parser.add_argument('-s', '--seed', dest='seed', type=str,
                        help='Starting seed. If omitted, a randomized seed will be used.')
    parser.add_argument('-ws', '--worldsize', dest='worldsize', type=str, default='80x40',
                        help='Size of the world, in terms of width and height. Defaults to 80x40.')
    parser.add_argument('-f', '--file', dest='file', type=str,
                        help='Load starting seed from file.')

    args = parser.parse_args()

    try:
        if not args.file:
            raise AssertionError
        population, world_size = load_seed_from_file(args.file)
    except (AssertionError, FileNotFoundError):
        world_size = parse_world_size_arg(args.worldsize)
        population = populate_world(world_size, args.seed)

    run_simulation(args.generations, population, world_size)


if __name__ == "__main__":
    main()
