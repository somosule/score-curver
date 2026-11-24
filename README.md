# W14 Class Participation, Q1: Curve Student Scores (NumPy)

Reads a text file of integer scores, prints the median and mean of the original scores, and curves every score so the highest becomes 100. Invalid input is reported with a clear message instead of a crash.

## Files

| File | Purpose |
|------|---------|
| `curve_scores.py` | The program |
| `test_curve_scores.py` | 21 unit and end-to-end tests |
| `efficiency_metrics.py` | Times the NumPy version against a plain Python loop version |
| `scores.txt` | Example input from the assignment |
| `samples/` | Invalid example files used in the sample runs |

## How it works

| Function | Job |
|----------|-----|
| `read_filename()` | Reads the file name with `input()` (no prompt). Up to 3 attempts if the file does not exist. |
| `load_scores(filename)` | Opens the file and passes its text to `parse_scores`. |
| `parse_scores(text)` | Splits on any whitespace, checks every value is a whole number from 0 to 100, and returns an integer NumPy array. |
| `curve_scores(scores)` | `scores + (100 - scores.max())`: adds the same amount to every score at once (broadcasting, no loop). |
| `main()` | Runs the steps in order, calculates the median and mean on the original scores, and prints the three output lines. |

## Assumptions

1. The output for a valid file matches the assignment exactly, so `input()` has no prompt text.
2. A missing file can be retyped up to 3 times, and then the program exits with a message.
3. Every value must be a whole number written with the digits 0 to 9. Letters, decimals and other scripts' digits are rejected, and the message names the first bad value and its position.
4. Scores must be between 0 and 100. A score above 100 would make the curve negative.
5. An empty file is an error, because there is nothing to summarise. A file that cannot be read (for example, no permission) is reported, not a crash.
6. The median and mean use the original scores, as the assignment says.
7. If the top score is already 100, the curve is 0 and the scores are unchanged.

## Environment setup

- Python 3.10 or newer (tested with Python 3.14.7 and NumPy 2.5.4 on a MacBook Air)
- Install the one dependency from this folder:

```bash
pip3 install -r requirements.txt
```

Everything else (`os`, `re`, `unittest`, `timeit`, `statistics`) is in Python's standard library. There are no parameters to set: the constants `MAX_ATTEMPTS = 3`, `MIN_SCORE = 0` and `MAX_SCORE = 100` are at the top of `curve_scores.py`.

## Run

```bash
python3 curve_scores.py
scores.txt
```

Expected output:

```
Median = 73.00
Average = 73.32
Curved scores = [ 70  95  84  68  98  73  67  88  73 100  79  92 100  83  98  85 100  85
  77  95  99  81  69  74  75]
```

### How to read the output

- `Median` is the middle value of the **original** scores (with an even count, the mean of the two middle values).
- `Average` is the mean of the **original** scores. Both are rounded to 2 decimal places.
- `Curved scores` is every score plus `100 - max`, so the highest is exactly 100. Here the top score is 89, so every score went up by 11. NumPy wraps long arrays onto a second line.

Example error messages (try them with the files in `samples/`):

```
File not found: 'score.txt' (attempt 1 of 3).
Invalid data in 'samples/bad_values.txt': value 3 ('abc') is not a whole number.
Invalid data in 'samples/out_of_range.txt': scores must be between 0 and 100; found 105.
Invalid data in 'samples/empty.txt': the file contains no scores.
```

On Windows, use python and pip in place of python3 and pip3.

## Test

```bash
python3 -m unittest -v
```

The 21 tests cover loading (3), validation (8), curving (4) and the full program run the way the autograder runs it (6).

## Efficiency

Each step (reading, max, median, mean and the curve) passes over the scores a fixed number of times, so time is **O(n)**. The array and the curved copy each hold n integers, so memory is **O(n)**.

```bash
python3 efficiency_metrics.py
```

This compares the NumPy version with the same work written as plain Python loops, for 100 to 1,000,000 random scores (seed 5010), using the best of 7 runs. It prints one row per size: the NumPy time, the loop time (both in milliseconds) and the speed-up, which is loop time divided by NumPy time. Timings depend on the machine; the pattern (the loop is faster at 100 scores, and NumPy is several times faster from 1,000 upwards) should hold.

Results on a MacBook Air (Python 3.14.7, NumPy 2.5.4):

| Scores (n) | NumPy (ms) | Loop (ms) | NumPy speed-up |
|---:|---:|---:|---:|
| 100 | 0.009 | 0.007 | 0.8× (loop faster) |
| 1,000 | 0.011 | 0.073 | 6.9× |
| 10,000 | 0.055 | 0.976 | 17.8× |
| 100,000 | 0.554 | 10.228 | 18.5× |
| 1,000,000 | 8.326 | 105.377 | 12.7× |

NumPy has a small fixed start-up cost per call, so a plain loop wins on tiny inputs. From 1,000 scores NumPy is 7 to 19 times faster; its lead narrows at the largest sizes as the arrays outgrow the processor's fast cache.
