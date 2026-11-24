"""
Compare the NumPy version with a pure-Python loop version on growing inputs.

Run from this folder with:  python efficiency_metrics.py
"""
import statistics
import sys
import timeit

import numpy as np

SIZES = [100, 1_000, 10_000, 100_000, 1_000_000]
REPEATS = 7


def numpy_version(scores):
    """Median, mean and curve using NumPy (the approach in curve_scores.py)."""
    return np.median(scores), np.mean(scores), scores + (100 - scores.max())


def loop_version(scores):
    """The same work with plain Python lists and loops."""
    top = 0
    for s in scores:
        if s > top:
            top = s
    curved = []
    for s in scores:
        curved.append(s + (100 - top))
    return statistics.median(scores), sum(scores) / len(scores), curved


def best_time_ms(func, data, number):
    """Best average time per call over REPEATS runs, in milliseconds."""
    runs = timeit.repeat(lambda: func(data), number=number, repeat=REPEATS)
    return min(runs) / number * 1000


def main():
    rng = np.random.default_rng(seed=5010)
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}")
    print(f"{'n':>10} {'NumPy (ms)':>12} {'Loop (ms)':>12} {'Speed-up':>10}")
    for n in SIZES:
        array = rng.integers(0, 101, size=n)
        as_list = array.tolist()
        number = max(1, 100_000 // n)
        t_numpy = best_time_ms(numpy_version, array, number)
        t_loop = best_time_ms(loop_version, as_list, number)
        print(f"{n:>10,} {t_numpy:>12.3f} {t_loop:>12.3f} {t_loop / t_numpy:>9.1f}x")


if __name__ == "__main__":
    main()
