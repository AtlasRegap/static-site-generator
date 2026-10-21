import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.TEXT),
            ],
        )

    def test_italic(self):
        node = TextNode("An _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("An ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_multiple_pairs(self):
        node = TextNode("A **bold** and **strong** finish", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("A ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("strong", TextType.BOLD),
                TextNode(" finish", TextType.TEXT),
            ],
        )

    def test_delimiter_at_start_and_end(self):
        node = TextNode("**bold** in the middle **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" in the middle ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
        )

    def test_no_delimiter(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("Just plain text", TextType.TEXT)])

    def test_non_text_node_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("already bold", TextType.BOLD)])

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("First `one`", TextType.TEXT),
            TextNode("a link", TextType.LINK, "https://www.boot.dev"),
            TextNode("Second `two`", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("First ", TextType.TEXT),
                TextNode("one", TextType.CODE),
                TextNode("a link", TextType.LINK, "https://www.boot.dev"),
                TextNode("Second ", TextType.TEXT),
                TextNode("two", TextType.CODE),
            ],
        )

    def test_bold_then_italic_chained(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
        )

    def test_unclosed_delimiter_raises(self):
        node = TextNode("This has an `unclosed code block", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = (
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) "
            "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            extract_markdown_images(text),
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_multiple_links(self):
        text = (
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            extract_markdown_links(text),
        )

    def test_links_ignore_images(self):
        text = "An ![image](https://example.com/a.png) and a [link](https://example.com)"
        self.assertListEqual(
            [("link", "https://example.com")],
            extract_markdown_links(text),
        )

    def test_images_ignore_links(self):
        text = "An ![image](https://example.com/a.png) and a [link](https://example.com)"
        self.assertListEqual(
            [("image", "https://example.com/a.png")],
            extract_markdown_images(text),
        )

    def test_no_matches(self):
        text = "Just plain text with no links or images"
        self.assertListEqual([], extract_markdown_images(text))
        self.assertListEqual([], extract_markdown_links(text))

    def test_empty_alt_text(self):
        matches = extract_markdown_images("![](https://example.com/a.png)")
        self.assertListEqual([("", "https://example.com/a.png")], matches)

class TestSplitImagesAndLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_image_at_start_with_text_after(self):
        node = TextNode("![logo](https://example.com/logo.png) then some text", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("logo", TextType.IMAGE, "https://example.com/logo.png"),
                TextNode(" then some text", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_split_image_only(self):
        node = TextNode("![logo](https://example.com/logo.png)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("logo", TextType.IMAGE, "https://example.com/logo.png")],
            split_nodes_image([node]),
        )

    def test_split_images_none_found(self):
        node = TextNode("No images here", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_images_non_text_unchanged(self):
        node = TextNode("bold", TextType.BOLD)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            split_nodes_link([node]),
        )

    def test_split_link_with_text_after(self):
        node = TextNode("Go [here](https://example.com) now", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("Go ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://example.com"),
                TextNode(" now", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_split_links_leaves_images_as_text(self):
        node = TextNode(
            "An ![img](https://example.com/a.png) and a [link](https://example.com)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("An ![img](https://example.com/a.png) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            split_nodes_link([node]),
        )

    def test_split_links_multiple_input_nodes(self):
        nodes = [
            TextNode("First [one](https://one.com)", TextType.TEXT),
            TextNode("already code", TextType.CODE),
            TextNode("[two](https://two.com) second", TextType.TEXT),
        ]
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("one", TextType.LINK, "https://one.com"),
                TextNode("already code", TextType.CODE),
                TextNode("two", TextType.LINK, "https://two.com"),
                TextNode(" second", TextType.TEXT),
            ],
            split_nodes_link(nodes),
        )

    def test_split_images_then_links(self):
        node = TextNode(
            "See ![pic](https://example.com/p.png) and [site](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        self.assertListEqual(
            [
                TextNode("See ", TextType.TEXT),
                TextNode("pic", TextType.IMAGE, "https://example.com/p.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("site", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )



class TestTextToTextNodes(unittest.TestCase):
    def test_all_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_to_textnodes(text),
        )

    def test_plain_text(self):
        self.assertListEqual(
            [TextNode("Nothing special here", TextType.TEXT)],
            text_to_textnodes("Nothing special here"),
        )

    def test_only_bold(self):
        self.assertListEqual(
            [TextNode("bold", TextType.BOLD)],
            text_to_textnodes("**bold**"),
        )

    def test_code_protects_contents(self):
        self.assertListEqual(
            [
                TextNode("Use ", TextType.TEXT),
                TextNode("**kwargs and _private", TextType.CODE),
                TextNode(" in Python", TextType.TEXT),
            ],
            text_to_textnodes("Use `**kwargs and _private` in Python"),
        )

    def test_underscore_in_url(self):
        self.assertListEqual(
            [
                TextNode("A ", TextType.TEXT),
                TextNode("photo", TextType.IMAGE, "https://example.com/my_photo.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            text_to_textnodes("A ![photo](https://example.com/my_photo.png) and _italic_"),
        )

    def test_unclosed_delimiter_raises(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("This has **unclosed bold")

if __name__ == "__main__":
    unittest.main()
