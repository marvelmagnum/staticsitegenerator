import unittest

from textnode import TextNode
import nodeutils

class TestNodeUtils(unittest.TestCase):
    def test_start(self):
        node = TextNode("**This** is text with a code block word", "text")
        new_nodes = nodeutils.split_textnode_delimiter([node], "**", "bold")
        self.assertEqual(new_nodes[0].text, '"This"')
        self.assertEqual(new_nodes[0].text_type, '"bold"')
        self.assertEqual(new_nodes[1].text, '" is text with a code block word"')
        self.assertEqual(new_nodes[1].text_type, '"text"')

    def test_middle(self):
        node = TextNode("This is text with a `code block` word", "text")
        new_nodes = nodeutils.split_textnode_delimiter([node], "`", "code")
        self.assertEqual(new_nodes[0].text, '"This is text with a "')
        self.assertEqual(new_nodes[0].text_type, '"text"')
        self.assertEqual(new_nodes[1].text, '"code block"')
        self.assertEqual(new_nodes[1].text_type, '"code"')
        self.assertEqual(new_nodes[2].text, '" word"')
        self.assertEqual(new_nodes[2].text_type, '"text"')

    def test_end(self):
        node = TextNode("This is text with a code block *word*", "text")
        new_nodes = nodeutils.split_textnode_delimiter([node], "*", "italic")
        self.assertEqual(new_nodes[0].text, '"This is text with a code block "')
        self.assertEqual(new_nodes[0].text_type, '"text"')
        self.assertEqual(new_nodes[1].text, '"word"')
        self.assertEqual(new_nodes[1].text_type, '"italic"')

    def test_non_text(self):
        node = TextNode("This is text with a code block *word*", "italic")
        new_nodes = nodeutils.split_textnode_delimiter([node], "*", "italic")
        self.assertEqual(new_nodes[0].text, "This is text with a code block *word*")
        self.assertEqual(new_nodes[0].text_type, "italic")

    def test_split_textnode_except(self):
        node = TextNode("This is text with a **code block word", "text")
        with self.assertRaises(SyntaxError):
            nodeutils.split_textnode_delimiter([node], "**", "bold")

if __name__ == "__main__":
    unittest.main()