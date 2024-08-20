import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eqNone(self):
        node = LeafNode()
        node2 = LeafNode()
        self.assertEqual(node.tag, node2.tag)
        self.assertEqual(node.value, node2.value)
        self.assertEqual(node.props, node2.props)

    def test_eq(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.tag, node2.tag)
        self.assertEqual(node.value, node2.value)
        if node.props:
            self.assertEqual(len(node.props), len(node2.props))
            self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_to_HTML(self):
        node = LeafNode("p", "This is a paragraph of text.")
        leaf_html = node.to_html()
        expected_html = "<p>This is a paragraph of text.</p>"
        self.assertEqual(leaf_html, expected_html)

    def test_to_HTML_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        leaf_html = node.to_html()
        expected_html = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(leaf_html, expected_html)

    def test_to_HTML_except(self):
        node = LeafNode("a")
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()