import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_heading_paragraph_list(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_excessive_newlines(self):
        md = """
First block



Second block




Third block
"""
        self.assertEqual(
            markdown_to_blocks(md),
            ["First block", "Second block", "Third block"],
        )

    def test_whitespace_around_blocks(self):
        md = "   First block   \n\n\tSecond block\t"
        self.assertEqual(
            markdown_to_blocks(md),
            ["First block", "Second block"],
        )

    def test_single_block(self):
        self.assertEqual(markdown_to_blocks("Just one block"), ["Just one block"])

    def test_empty_document(self):
        self.assertEqual(markdown_to_blocks(""), [])
        self.assertEqual(markdown_to_blocks("\n\n\n\n"), [])


class TestBlockToBlockType(unittest.TestCase):
    # Headings
    def test_heading_level_1(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)

    def test_heading_level_6(self):
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)

    def test_heading_seven_hashes_is_paragraph(self):
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)

    def test_heading_no_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    # Code
    def test_code(self):
        block = "```\nprint('hi')\nx = 1\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_no_newline_after_opening_is_paragraph(self):
        self.assertEqual(block_to_block_type("```print('hi')```"), BlockType.PARAGRAPH)

    def test_code_unclosed_is_paragraph(self):
        self.assertEqual(block_to_block_type("```\nprint('hi')"), BlockType.PARAGRAPH)

    # Quotes
    def test_quote(self):
        block = "> First line\n> Second line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_without_space(self):
        block = ">First line\n>Second line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_with_bad_line_is_paragraph(self):
        block = "> First line\nSecond line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Unordered lists
    def test_unordered_list(self):
        block = "- one\n- two\n- three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_missing_space_is_paragraph(self):
        block = "- one\n-two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Ordered lists
    def test_ordered_list(self):
        block = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_not_starting_at_1_is_paragraph(self):
        block = "2. one\n3. two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_skipped_number_is_paragraph(self):
        block = "1. one\n3. two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_double_digits(self):
        block = "\n".join(f"{i}. item" for i in range(1, 12))
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    # Paragraphs
    def test_paragraph(self):
        block = "Just some text\nover two lines"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
