#!/usr/bin/env python

""" DT179G - LAB ASSIGNMENT 3
You find the description for the assignment in Moodle, where each detail regarding requirements
are stated. Below you find the inherent code, some of which fully defined. You add implementation
for those functions which are needed:

 - create_logger()
 - measurements_decorator(..)
 - fibonacci_memory(..)
 - print_statistics(..)
 - write_to_file(..)
"""

from pathlib import Path
from timeit import default_timer as timer
from functools import wraps
import argparse
import logging
import logging.config
import json

__version__ = '1.0'
__desc__ = "Program used for measuríng execution time of various Fibonacci implementations!"

LINE = '\n' + ("---------------" * 5)
RESOURCES = Path(__file__) / "../../_Resources/"
LOGGER = None  # declared at module level, will be defined from main()


def create_logger() -> logging.Logger:
    """Create and return logger object."""
    file_path = RESOURCES / "ass3_log_conf.json"  # Get the filepath to the logger config file
    with open(file_path, "r") as file:  # Open the logger config file in read mode
        config = json.load(file)  # Write the json data to variable
        logging.config.dictConfig(config)  # Configure logger from json-file
        return logging.getLogger("ass_3_logger")  # Return logger with specified name


def measurements_decorator(func):
    """Function decorator, used for time measurements."""
    @wraps(func)
    def wrapper(nth_nmb: int) -> tuple:
        fibonacci_values = list()  # List of fibonacci values, to be filled
        start_time = timer()  # Using imported timer to get current time in ms
        LOGGER.info("Starting measurements...")  # Initialize logging with starting measurements statement
        for i in range(nth_nmb, -1, -1):  # Increment fibonacci-sequence in reverse, from starting value to 0
            fib_val = func(i)  # Run the fib functions to get the current value in sequence
            fibonacci_values.append(fib_val)  # Write value to list
            if i % 5 == 0:  # For every 5 numbers
                LOGGER.debug(f"{i}: {fib_val}")  # Log the sequence, and value of sequence
        end_time = timer()  # Get current time, after the loop is finished
        duration = end_time - start_time  # Get the elapsed time between start and finish
        output = (duration, fibonacci_values)  # Write the elapsed time and list of values to a tuple
        return output  # Return the tuple
    return wrapper


@measurements_decorator
def fibonacci_iterative(nth_nmb: int) -> int:
    """An iterative approach to find Fibonacci sequence value.
    YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    old, new = 0, 1
    if nth_nmb in (0, 1):
        return nth_nmb
    for __ in range(nth_nmb - 1):
        old, new = new, old + new
    return new


@measurements_decorator
def fibonacci_recursive(nth_nmb: int) -> int:
    """An recursive approach to find Fibonacci sequence value.
    YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    def fib(_n):
        return _n if _n <= 1 else fib(_n - 1) + fib(_n - 2)
    return fib(nth_nmb)


@measurements_decorator
def fibonacci_memory(nth_nmb: int) -> int:
    """An recursive approach to find Fibonacci sequence value, storing those already calculated."""
    memory: dict = {0: 0, 1: 1}  # Cache to store calculated fib values in

    def fib(_n):
        if _n <= 1:
            return _n  # Return input nr
        elif _n not in memory:
            # Calculate fib value, store in dict
            memory[list(memory.keys())[-1] + 1] = list(memory.values())[-1] + list(memory.values())[-2]
            return fib(_n)  # return run fib function again
        else:
            return list(memory.values())[-1]  # Return specified element from cache

    return fib(nth_nmb)


def duration_format(duration: float, precision: str) -> str:
    """Function to convert number into string. Switcher is dictionary type here.
    YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    switcher = {
        'Seconds': "{:.5f}".format(duration),
        'Milliseconds': "{:.5f}".format(duration * 1_000),
        'Microseconds': "{:.1f}".format(duration * 1_000_000),
        'Nanoseconds': "{:d}".format(int(duration * 1_000_000_000))
    }

    # get() method of dictionary data type returns value of passed argument if it is present in
    # dictionary otherwise second argument will be assigned as default value of passed argument
    return switcher.get(precision, "nothing")


def print_statistics(fib_details: dict, nth_value: int):
    """Function which handles printing to console."""
    print("{0}\n{1}{0}".format(LINE, f"DURATION FOR EACH APPROACH WITHIN INTERVAL: {nth_value}-0".center(len(LINE))))

    table_data = [  # Initialize list of table data to be printed with column headers
        ["", "Seconds", "Milliseconds", "Microseconds", "Nanoseconds"]
    ]

    for key in fib_details:  # Iterate the dictionary
        table_data.append([
            key.title(),  # Get the current key
            duration_format(fib_details[key][0], "Seconds"),  # Pass the ms value linked to the key to be formatted
            duration_format(fib_details[key][0], "Milliseconds"),
            duration_format(fib_details[key][0], "Microseconds"),
            duration_format(fib_details[key][0], "Nanoseconds"),
        ])
    for i in range(len(table_data)):  # Iterate the table_data list, format "table", print values
        print("{: <13} {: >13} {: >15} {: >15} {: >15}".format(*table_data[i]))


def write_to_file(fib_details: dict):
    """Function to write information to file."""
    for key in fib_details:  # Iterate through dict
        file_name = key.replace(" ", "_") + ".txt"  # Create filename with key as basis
        with open(RESOURCES / file_name, "w") as file1:  # Open/create file
            fib_details[key][1].reverse()  # Reverse the logged fibonacci values in dict
            for i in range(len(fib_details[key][1]) - 1, -1, -1):  # Iterate the fibonacci values in dict
                value = fib_details[key][1][i]  # Write the current value to variable
                file1.write(f"{i}: {value}\n")  # Write the value + sequence nr to file


def main():
    """The main program execution. YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    epilog = "DT179G Assignment 3 v" + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('nth', metavar='nth', type=int, nargs='?', default=30,
                        help="nth Fibonacci sequence to find.")

    global LOGGER  # ignore warnings raised from linters, such as PyLint!
    LOGGER = create_logger()

    args = parser.parse_args()
    nth_value = args.nth  # nth value to sequence. Will fallback on default value!

    fib_details = {  # store measurement information in a dictionary
        'fib iteration': fibonacci_iterative(nth_value),
        'fib recursion': fibonacci_recursive(nth_value),
        'fib memory': fibonacci_memory(nth_value)
    }

    print_statistics(fib_details, nth_value)    # print information in console
    write_to_file(fib_details)                  # write data files


if __name__ == "__main__":
    main()
