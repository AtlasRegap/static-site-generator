import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple(self):
        node = HTMLNode(
            "a",
            "Click me",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_none(self):
        node = HTMLNode("p", "Hello")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode("p", "Hello", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_defaults_are_none(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "Hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just raw text")
        self.assertEqual(node.to_html(), "Just raw text")

    def test_leaf_to_html_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_has_no_children(self):
        node = LeafNode("p", "Hello")
        self.assertIsNone(node.children)


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("span", "child")],
            {"class": "container"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="container"><span>child</span></div>',
        )

    def test_to_html_mixed_nesting(self):
        node = ParentNode(
            "div",
            [
                LeafNode(None, "Start "),
                ParentNode("p", [LeafNode("b", "bold")]),
                LeafNode("a", "link", {"href": "https://www.boot.dev"}),
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<div>Start <p><b>bold</b></p><a href="https://www.boot.dev">link</a></div>',
        )

    def test_to_html_empty_children_list(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_to_html_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("b", "text")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_children_none_raises(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_child_error_bubbles_up(self):
        node = ParentNode("div", [LeafNode("b", None)])
        with self.assertRaises(ValueError):
            node.to_html()





if __name__ == "__main__":
    unittest.main()
