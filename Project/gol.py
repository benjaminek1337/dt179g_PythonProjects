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
    file_name = _file_name if ".json" in _file_name else _file_name + ".json"
    file_path = RESOURCES / file_name

    with open(file_path, "r") as file:
        data = json.load(file)
        raw_population: dict = data["population"]
        parsed_population: dict = {}
        for key in raw_population:
            if raw_population[key] is not None:
                neighbours: list = list(tuple(i) for i in raw_population[key]["neighbours"])
                parsed_population[literal_eval(key)] = {
                    "state": raw_population[key]["state"],
                    "neighbours": neighbours
                }
            else:
                parsed_population[literal_eval(key)] = cb.STATE_RIM
        seed: tuple = parsed_population, data["world_size"]
        return seed


def create_logger() -> logging.Logger:
    """ Creates a logging object to be used for reports. """
    file_path = RESOURCES / "gol.log"
    gol_logger = logging.getLogger("gol_logger")
    gol_logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(file_path)
    file_handler.setLevel(logging.INFO)
    gol_logger.addHandler(file_handler)
    return gol_logger


def simulation_decorator(func):
    """ Function decorator, used to run full extent of simulation. """
    def wrapper(nth_generation: int, population: dict, world_size: tuple):
        gol_logger = create_logger()
        current_population: dict = population

        for i in range(0, nth_generation):
            cb.clear_console()
            population_count: int = 0
            alive_count: int = 0
            elder_count: int = 0
            prime_elder_count: int = 0
            dead_count: int = 0
            for coords in current_population:
                if current_population[coords] is not cb.STATE_RIM:
                    population_count += 1
                    if current_population[coords]["state"] != cb.STATE_DEAD:
                        alive_count += 1
                        if current_population[coords]["state"] == cb.STATE_ELDER:
                            elder_count += 1
                        elif current_population[coords]["state"] == cb.STATE_PRIME_ELDER:
                            prime_elder_count += 1
                    else:
                        dead_count += 1

            gol_logger.info(f"GENERATION {i} \n"
                            f" Population: {population_count} \n"
                            f" Alive: {alive_count} \n"
                            f" Elders: {elder_count} \n"
                            f" Prime: {prime_elder_count} \n"
                            f" Dead: {dead_count} \n")

            current_population = func(i, current_population, world_size)
            sleep(0.2)

    return wrapper


# -----------------------------------------
# BASE IMPLEMENTATIONS
# -----------------------------------------

def parse_world_size_arg(_arg: str) -> tuple:
    """ Parse width and height from command argument. """
    args = _arg.split("x")

    try:
        for i in range(len(args)):
            if len(args) != 2 or args[i] == "":
                raise AssertionError
            if not isinstance(int(args[i]), int) or int(args[i]) < 1:
                raise ValueError
        return int(args[0]), int(args[1])
    except AssertionError:
        print("World size should contain width and height, separated by ‘x’. Ex: ‘80x40’")
    except ValueError as error:
        msg: str = "Both width and height needs to have positive values above zero."
        print(error) if (len(str(error)) > 0) else print(msg)

    print("Using default world size: 80x40")
    sleep(1)
    return 80, 40


def populate_world(_world_size: tuple, _seed_pattern: str = None) -> dict:
    """ Populate the world with cells and initial states. """
    population: dict = {}
    pattern: list = []
    if _seed_pattern:
        pattern: list = cb.get_pattern(_seed_pattern, _world_size)

    coords: list = list(product(range(0, _world_size[1]), range(0, _world_size[0])))
    for i in range(len(coords)):
        if coords[i][0] == 0 \
                or coords[i][0] == _world_size[1] - 1 \
                or coords[i][1] == 0 \
                or coords[i][1] == _world_size[0] - 1:
            population[coords[i]] = cb.STATE_RIM
        else:
            if pattern:
                population[coords[i]] = {
                    "state": cb.STATE_ALIVE if coords[i] in pattern else cb.STATE_DEAD,
                    "neighbours": calc_neighbour_positions(coords[i]),
                    "age": 0
                }
            else:
                population[coords[i]] = {
                    "state": cb.STATE_ALIVE if random.randint(0, 21) >= 15 else cb.STATE_DEAD,
                    "neighbours": calc_neighbour_positions(coords[i]),
                    "age": 0
                }
    return population


def calc_neighbour_positions(_cell_coord: tuple) -> list:
    """ Calculate neighbouring cell coordinates in all directions (cardinal + diagonal).
    Returns list of tuples. """
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


@simulation_decorator
def run_simulation(_generations: int, _population: dict, _world_size: tuple) -> dict:
    """ Runs a tick in the simulation. """
    return update_world(_population, _world_size)


def update_world(_cur_gen: dict, _world_size: tuple) -> dict:
    """ Represents a tick in the simulation. """
    next_generation: dict = {}
    for key in _cur_gen:
        out_str: str = cb.get_print_value(cb.STATE_RIM) if _cur_gen[key] is cb.STATE_RIM \
            else cb.get_print_value(_cur_gen[key]["state"])
        cb.progress(out_str + "\n" if key[1] == _world_size[0] - 1 else out_str)

        if _cur_gen[key] is cb.STATE_RIM:
            next_generation[key] = cb.STATE_RIM
        else:
            living: int = count_alive_neighbours(_cur_gen[key]["neighbours"], _cur_gen)
            if _cur_gen[key]["state"] != cb.STATE_DEAD and 2 <= living <= 3 \
                    or _cur_gen[key]["state"] == cb.STATE_DEAD and living == 3:

                try:
                    age: int = _cur_gen[key]["age"] + 1
                except KeyError:
                    age: int = 1

                next_generation[key] = {
                    "neighbours": _cur_gen[key]["neighbours"],
                    "age": age
                }
                if age < 5:
                    next_generation[key]["state"] = cb.STATE_ALIVE
                elif 5 <= age <= 9:
                    next_generation[key]["state"] = cb.STATE_ELDER
                else:
                    next_generation[key]["state"] = cb.STATE_PRIME_ELDER
            else:
                next_generation[key] = {
                    "state": cb.STATE_DEAD,
                    "neighbours": _cur_gen[key]["neighbours"],
                    "age": 0
                }
    return next_generation


def count_alive_neighbours(_neighbours: list, _cells: dict) -> int:
    """ Determine how many of the neighbouring cells are currently alive. """
    living: int = 0
    for coords in _neighbours:
        if _cells[coords] is not cb.STATE_RIM and _cells[coords]["state"] != cb.STATE_DEAD:
            living += 1
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
