import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_eqNone(self):
        node = ParentNode()
        node2 = ParentNode()
        self.assertEqual(node.tag, node2.tag)
        self.assertEqual(node.children, node2.children)
        self.assertEqual(node.props, node2.props)

    def test_eq(self):
        node = ParentNode(
                            "p",
                            [
                                LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"),
                                LeafNode("i", "italic text"),
                                LeafNode(None, "Normal text"),
                            ],
                        )
        node2 = ParentNode(
                            "p",
                            [
                                LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"),
                                LeafNode("i", "italic text"),
                                LeafNode(None, "Normal text"),
                            ],
                        )
        self.assertEqual(node.tag, node2.tag)
        if node.children:
            self.assertEqual(len(node.children), len(node2.children))
            for i in range(len(node.children)):
                self.assertEqual(node.children[i].to_html(), node2.children[i].to_html())
        if node.props:
            self.assertEqual(len(node.props), len(node2.props))
            self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_to_HTML(self):
        node = ParentNode(
                            "p",
                            [
                                LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"),
                                LeafNode("i", "italic text"),
                                LeafNode(None, "Normal text"),
                            ],
                        )
        parent_html = node.to_html()
        expected_html = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(parent_html, expected_html)

    def test_to_HTML_props(self):
        node = ParentNode(
                            "a",
                            [
                                LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"),
                                LeafNode("i", "italic text"),
                                LeafNode(None, "Normal text")
                            ],
                            {"href": "https://www.google.com"}
                        )
        parent_html = node.to_html()
        expected_html = '<a href="https://www.google.com"><b>Bold text</b>Normal text<i>italic text</i>Normal text</a>'
        self.assertEqual(parent_html, expected_html)

    def test_to_HTML_nested_parent(self):
        node = ParentNode(
                            "p",
                            [
                                LeafNode("b", "Bold text"),
                                ParentNode(
                                    "a",
                                    [
                                        LeafNode(None, "Click Me!"),
                                    ],
                                    {"href": "https://www.google.com"}
                                ),
                                LeafNode("i", "italic text"),
                                LeafNode(None, "Normal text")
                            ],
                        )
        parent_html = node.to_html()
        expected_html = '<p><b>Bold text</b><a href="https://www.google.com">Click Me!</a><i>italic text</i>Normal text</p>'
        self.assertEqual(parent_html, expected_html)

    def test_to_HTML_except_tag(self):
        node = ParentNode()
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_HTML_except_child(self):
        node = LeafNode("a")
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()