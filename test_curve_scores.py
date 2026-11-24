"""
Tests for curve_scores.py.

Run from this folder with:  python -m unittest -v
"""
import os
import subprocess
import sys
import tempfile
import unittest

import numpy as np

from curve_scores import curve_scores, load_scores, parse_scores

HERE = os.path.dirname(os.path.abspath(__file__))


def write_temp_file(text):
    """Write text to a temporary file and return its path."""
    f = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False)
    f.write(text)
    f.close()
    return f.name


def run_program(user_input):
    """Run curve_scores.py as the autograder would and return its output."""
    result = subprocess.run(
        [sys.executable, os.path.join(HERE, "curve_scores.py")],
        input=user_input, capture_output=True, text=True, cwd=HERE,
    )
    return result.stdout


class TestLoading(unittest.TestCase):
    def test_spaces(self):
        self.assertEqual(load_scores(write_temp_file("59 84 73")).tolist(), [59, 84, 73])

    def test_mixed_whitespace(self):
        # Spaces, newlines, tabs and blank lines all work as separators.
        path = write_temp_file("59  84\n73\t57\n\n")
        self.assertEqual(load_scores(path).tolist(), [59, 84, 73, 57])

    def test_integer_type(self):
        self.assertTrue(np.issubdtype(parse_scores("1 2 3").dtype, np.integer))


class TestValidation(unittest.TestCase):
    def test_empty_file(self):
        with self.assertRaisesRegex(ValueError, "no scores"):
            parse_scores("  \n\n ")

    def test_letters(self):
        with self.assertRaisesRegex(ValueError, "value 2 \\('abc'\\)"):
            parse_scores("59 abc 73")

    def test_decimal(self):
        with self.assertRaisesRegex(ValueError, "not a whole number"):
            parse_scores("59 85.5")

    def test_negative(self):
        with self.assertRaisesRegex(ValueError, "between 0 and 100; found -5"):
            parse_scores("59 -5 73")

    def test_over_100(self):
        with self.assertRaisesRegex(ValueError, "found 105"):
            parse_scores("59 105")

    def test_huge_number(self):
        with self.assertRaisesRegex(ValueError, "far too large"):
            parse_scores("59 99999999999999999999")

    def test_non_ascii_digit(self):
        # Arabic-Indic digit three: a digit, but not 0-9.
        with self.assertRaisesRegex(ValueError, "not a whole number"):
            parse_scores("59 \u0663")

    def test_boundaries_allowed(self):
        self.assertEqual(parse_scores("0 100").tolist(), [0, 100])


class TestCurving(unittest.TestCase):
    def test_top_score_becomes_100(self):
        self.assertEqual(curve_scores(np.array([59, 89, 70])).tolist(), [70, 100, 81])

    def test_already_100_unchanged(self):
        self.assertEqual(curve_scores(np.array([100, 80, 65])).tolist(), [100, 80, 65])

    def test_single_score(self):
        self.assertEqual(curve_scores(np.array([42])).tolist(), [100])

    def test_original_not_changed(self):
        scores = np.array([50, 60])
        curve_scores(scores)
        self.assertEqual(scores.tolist(), [50, 60])


class TestFullProgram(unittest.TestCase):
    def test_matches_assignment_example(self):
        expected = (
            "Median = 73.00\n"
            "Average = 73.32\n"
            "Curved scores = [ 70  95  84  68  98  73  67  88  73 100  79  92 100  83  98  85 100  85\n"
            "  77  95  99  81  69  74  75]\n"
        )
        self.assertEqual(run_program("scores.txt\n"), expected)

    def test_even_count_median(self):
        # With an even count, the median is the mean of the two middle values.
        lines = run_program(write_temp_file("10 20 30 40") + "\n").splitlines()
        self.assertEqual(lines, ["Median = 25.00", "Average = 25.00",
                                 "Curved scores = [ 70  80  90 100]"])

    def test_missing_file_then_valid(self):
        lines = run_program("nope.txt\nscores.txt\n").splitlines()
        self.assertIn("File not found: 'nope.txt' (attempt 1 of 3).", lines[0])
        self.assertEqual(lines[1], "Median = 73.00")

    def test_three_missing_files_exits(self):
        output = run_program("a.txt\nb.txt\nc.txt\n")
        self.assertIn("attempt 3 of 3", output)
        self.assertTrue(output.strip().endswith("No valid file was entered. Exiting."))

    def test_no_input_exits_cleanly(self):
        self.assertIn("No valid file was entered", run_program(""))

    def test_invalid_data_message(self):
        output = run_program(write_temp_file("59 abc") + "\n")
        self.assertIn("value 2 ('abc') is not a whole number", output)


if __name__ == "__main__":
    unittest.main()
