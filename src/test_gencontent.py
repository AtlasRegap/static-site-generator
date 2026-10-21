import unittest
from gencontent import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_strips_whitespace(self):
        self.assertEqual(extract_title("#   Hello world   "), "Hello world")

    def test_title_not_on_first_line(self):
        md = "Some intro text\n\n# The Title\n\nMore text"
        self.assertEqual(extract_title(md), "The Title")

    def test_ignores_h2_before_h1(self):
        md = "## Not this\n\n# This one"
        self.assertEqual(extract_title(md), "This one")

    def test_only_h2_raises(self):
        with self.assertRaises(ValueError):
            extract_title("## Only an h2")

    def test_no_heading_raises(self):
        with self.assertRaises(ValueError):
            extract_title("Just a paragraph")


if __name__ == "__main__":
    unittest.main()
