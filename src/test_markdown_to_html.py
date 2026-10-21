import unittest
from markdown_to_html import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        fence = "`" * 3
        md = f"""
{fence}
This is text that _should_ remain
the **same** even with inline stuff
{fence}
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# Heading 1

### Heading **three**

###### Six
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><h1>Heading 1</h1><h3>Heading <b>three</b></h3><h6>Six</h6></div>",
        )

    def test_quote(self):
        md = """
> This is a quote
> with **bold**
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><blockquote>This is a quote with <b>bold</b></blockquote></div>",
        )

    def test_quote_without_space(self):
        md = """
>no space
>here
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><blockquote>no space here</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- one
- _two_
- [three](https://boot.dev)
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            '<div><ul><li>one</li><li><i>two</i></li><li><a href="https://boot.dev">three</a></li></ul></div>',
        )

    def test_ordered_list(self):
        md = """
1. first
2. `second`
3. third. with a dot
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><ol><li>first</li><li><code>second</code></li><li>third. with a dot</li></ol></div>",
        )

    def test_mixed_document(self):
        md = """
# Title

Some text.

- a
- b
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><h1>Title</h1><p>Some text.</p><ul><li>a</li><li>b</li></ul></div>",
        )


if __name__ == "__main__":
    unittest.main()
