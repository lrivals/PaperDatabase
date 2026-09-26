"""Tests de lib/ligatures.py (ligatures fi/ff/fl perdues à l'extraction).

.venv/bin/python -m unittest discover tests
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib import ligatures  # noqa: E402
from lib.doc import Block  # noqa: E402

VOCAB = ligatures.KNOWN | {"a", "the", "we", "that", "of", "to", "is", "an", "roofline", "tuning"}


def fix(text):
    return ligatures.repair(text, VOCAB)


class TestRepair(unittest.TestCase):
    def test_join(self):
        self.assertEqual(fix("an e cient classi cation"), ("an efficient classification", 2))
        self.assertEqual(fix("E cient Processing"), ("Efficient Processing", 1))
        self.assertEqual(fix("the Roo ine model"), ("the Roofline model", 1))

    def test_word_start(self):
        self.assertEqual(fix("we nd that the rst"), ("we find that the first", 2))

    def test_real_word_then_fragment_prefers_word_start(self):
        # « a ne-tuning » : « a fine-tuning », pas « affine-tuning »
        self.assertEqual(fix("a ne-tuning step"), ("a fine-tuning step", 1))

    def test_real_words_untouched(self):
        self.assertEqual(fix("the rest of the list"), ("the rest of the list", 0))
        self.assertEqual(fix("an xyz qqq"), ("an xyz qqq", 0))   # mot joint inconnu

    def test_urls_untouched(self):
        self.assertEqual(fix("github.com/PaddlePadd le/x")[1], 0)

    def test_leftover_ignores_hyphenation(self):
        self.assertEqual(ligatures.leftover("classi cation"), 1)
        self.assertEqual(ligatures.leftover("signifi-\n\ncantly"), 0)

    def test_repair_blocks(self):
        b = Block("section", "2. E cient design", "2.1 The rst step", 2,
                  [("an e cient", 1), ("signifi-", 1), ("cantly more", 2)])
        self.assertEqual(ligatures.repair_blocks([b], VOCAB), (1, 0))
        self.assertEqual(b.paras[0], ("an efficient", 1))
        self.assertEqual((b.section, b.subsection), ("2. Efficient design", "2.1 The first step"))


if __name__ == "__main__":
    unittest.main()
