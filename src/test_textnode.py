import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is not a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_type_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("This is a text node", "bold", "http://www.google.com")
        node2 = TextNode("This is a text node", "bold", "http://www.amazon.com")
        self.assertNotEqual(node, node2)

    def test_nourl(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(node.url, None)

    def test_to_html_text(self):
        node = TextNode("This is a text node", "text")
        self.assertEqual(node.text_node_to_html_node().to_html(), "This is a text node")

    def test_to_html_bold(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(node.text_node_to_html_node().to_html(), "<b>This is a text node</b>")

    def test_to_html_italic(self):
        node = TextNode("This is a text node", "italic")
        self.assertEqual(node.text_node_to_html_node().to_html(), "<i>This is a text node</i>")

    def test_to_html_code(self):
        node = TextNode("This is a text node", "code")
        self.assertEqual(node.text_node_to_html_node().to_html(), "<code>This is a text node</code>")

    def test_to_html_link(self):
        node = TextNode("This is a text node", "link", "http://www.google.com")
        self.assertEqual(node.text_node_to_html_node().to_html(), '<a href="http://www.google.com">This is a text node</a>')

    def test_to_html_image(self):
        node = TextNode("This is a text node", "image", "https://preview.redd.it/zfohxnf8t3pa1.jpg")
        self.assertEqual(node.text_node_to_html_node().to_html(), '<img src="https://preview.redd.it/zfohxnf8t3pa1.jpg" alt="This is a text node"> </img>')

if __name__ == "__main__":
    unittest.main()