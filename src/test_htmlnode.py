import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eqNone(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node.tag, node2.tag)
        self.assertEqual(node.value, node2.value)
        self.assertEqual(node.children, node2.children)
        self.assertEqual(node.props, node2.props)

    def test_eq(self):
        node = HTMLNode("p", "content", [], {"href": "https://www.google.com"})
        node2 = HTMLNode("p", "content", [], {"href": "https://www.google.com"})
        self.assertEqual(node.tag, node2.tag)
        self.assertEqual(node.value, node2.value)
        if node.children:
            self.assertEqual(len(node.children), len(node2.children))
            for i in range(len(node.children)):
                self.assertEqual(node.children[i].to_html(), node2.children[i].to_html())
        if node.props:
            self.assertEqual(len(node.props), len(node2.props))
            self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_props1(self):
        node = HTMLNode("p", "content", [], {"href": "https://www.google.com"})
        prop_html = node.props_to_html()
        expected_html = ' href="https://www.google.com"'
        self.assertEqual(prop_html, expected_html)

    def test_props2(self):
        node = HTMLNode("p", "content", [], {"href": "https://www.google.com", "target": "_blank"})
        prop_html = node.props_to_html()
        expected_html = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(prop_html, expected_html)


if __name__ == "__main__":
    unittest.main()