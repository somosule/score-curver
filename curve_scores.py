"""
W14 Class Participation, Q1: Curve student scores with NumPy.

Reads a file of whole-number scores, reports the median and mean of the
original scores, then curves every score so the highest becomes 100.
Invalid input is reported with a clear message instead of a crash.
"""
import os
import re

import numpy as np

MAX_ATTEMPTS = 3          # tries allowed for the file name
MIN_SCORE, MAX_SCORE = 0, 100
WHOLE_NUMBER = re.compile(r"-?[0-9]+")  # ASCII digits only


def parse_scores(text):
    """Turn whitespace-separated text into an integer array, or raise ValueError."""
    # .split() with no argument splits on any spaces, tabs or newlines.
    tokens = text.split()
    if not tokens:
        raise ValueError("the file contains no scores")

    # Check every value before converting, so the message names the bad one.
    for position, token in enumerate(tokens, start=1):
        if not WHOLE_NUMBER.fullmatch(token):
            raise ValueError(f"value {position} ('{token}') is not a whole number")

    try:
        scores = np.array(tokens, dtype=int)
    except OverflowError:   # e.g. a 20-digit number, too big to store
        raise ValueError("a value is far too large to be a score") from None

    # Scores outside 0-100 would make the curve meaningless.
    out_of_range = scores[(scores < MIN_SCORE) | (scores > MAX_SCORE)]
    if out_of_range.size > 0:
        raise ValueError(f"scores must be between {MIN_SCORE} and {MAX_SCORE}; "
                         f"found {out_of_range[0]}")
    return scores


def load_scores(filename):
    """Read a file and return its scores as an integer array."""
    with open(filename) as f:
        return parse_scores(f.read())


def curve_scores(scores):
    """Add (100 - max score) to every score so the top score becomes 100."""
    # Broadcasting: adding one number to an array adds it to every element.
    return scores + (MAX_SCORE - scores.max())


def read_filename():
    """Ask for a file name until one exists, up to MAX_ATTEMPTS. Returns None on failure."""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            filename = input().strip()  # no prompt text, so valid output matches exactly
        except EOFError:
            return None
        if os.path.isfile(filename):
            return filename
        print(f"File not found: '{filename}' (attempt {attempt} of {MAX_ATTEMPTS}).")
    return None


def main():
    filename = read_filename()
    if filename is None:
        print("No valid file was entered. Exiting.")
        return

    try:
        scores = load_scores(filename)
    except (ValueError, OSError) as error:   # bad data, or a file that can't be read
        print(f"Invalid data in '{filename}': {error}.")
        return

    # Stats come from the ORIGINAL scores, before curving.
    median = np.median(scores)
    average = np.mean(scores)
    curved = curve_scores(scores)

    print(f"Median = {median:.2f}")    # :.2f gives two decimal places
    print(f"Average = {average:.2f}")
    print("Curved scores =", curved)   # NumPy's own array formatting


# Runs main() only when this file is run directly, not when tests import it.
if __name__ == "__main__":
    main()
