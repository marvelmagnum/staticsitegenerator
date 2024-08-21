import unittest

from textnode import TextNode
import nodeutils

class TestNodeUtils(unittest.TestCase):
    def test_start(self):
        node = TextNode("**This** is text with a code block word", "text")
        new_nodes = nodeutils.split_textnode_delimiter([node], "**", "bold")
        self.assertEqual(new_nodes[0].text, "This")
        self.assertEqual(new_nodes[0].text_type, "bold")
        self.assertEqual(new_nodes[1].text, " is text with a code block word")
        self.assertEqual(new_nodes[1].text_type, "text")

    def test_middle(self):
        node = TextNode("This is text with a `code block` word", "text")
        new_nodes = nodeutils.split_textnode_delimiter([node], "`", "code")
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, "text")
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, "code")
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, "text")

    def test_end(self):
        node = TextNode("This is text with a code block *word*", "text")
        new_nodes = nodeutils.split_textnode_delimiter([node], "*", "italic")
        self.assertEqual(new_nodes[0].text, "This is text with a code block ")
        self.assertEqual(new_nodes[0].text_type, "text")
        self.assertEqual(new_nodes[1].text, "word")
        self.assertEqual(new_nodes[1].text_type, "italic")

    def test_non_text(self):
        node = TextNode("This is text with a code block *word*", "italic")
        new_nodes = nodeutils.split_textnode_delimiter([node], "*", "italic")
        self.assertEqual(new_nodes[0].text, "This is text with a code block *word*")
        self.assertEqual(new_nodes[0].text_type, "italic")

    def test_split_textnode_except(self):
        node = TextNode("This is text with a **code block word", "text")
        with self.assertRaises(SyntaxError):
            nodeutils.split_textnode_delimiter([node], "**", "bold")

    def test_extract_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = nodeutils.extract_markdown_images(text)
        self.assertEqual(result[0][0], "rick roll")
        self.assertEqual(result[0][1], "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(result[1][0], "obi wan")
        self.assertEqual(result[1][1], "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_extract_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = nodeutils.extract_markdown_links(text)
        self.assertEqual(result[0][0], "to boot dev")
        self.assertEqual(result[0][1], "https://www.boot.dev")
        self.assertEqual(result[1][0], "to youtube")
        self.assertEqual(result[1][1], "https://www.youtube.com/@bootdotdev")
        
    def test_split_nodes_image(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", "text")
        result = nodeutils.split_nodes_image([node])
        self.assertEqual(result[0].text, "This is text with a ")
        self.assertEqual(result[0].text_type, "text")
        self.assertEqual(result[1].text, "rick roll")
        self.assertEqual(result[1].text_type, "image")
        self.assertEqual(result[1].url, "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(result[2].text, " and ")
        self.assertEqual(result[2].text_type, "text")
        self.assertEqual(result[3].text, "obi wan")
        self.assertEqual(result[3].text_type, "image")
        self.assertEqual(result[3].url, "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_split_nodes_no_image(self):
        node = TextNode("This is text with a rick roll and obi wan", "text")
        result = nodeutils.split_nodes_image([node])
        self.assertEqual(result[0].text, "This is text with a rick roll and obi wan")
        self.assertEqual(result[0].text_type, "text")
        self.assertEqual(len(result), 1)

    def test_split_nodes_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", "text")
        result = nodeutils.split_nodes_link([node])
        self.assertEqual(result[0].text, "This is text with a link ")
        self.assertEqual(result[0].text_type, "text")
        self.assertEqual(result[1].text, "to boot dev")
        self.assertEqual(result[1].text_type, "link")
        self.assertEqual(result[1].url, "https://www.boot.dev")
        self.assertEqual(result[2].text, " and ")
        self.assertEqual(result[2].text_type, "text")
        self.assertEqual(result[3].text, "to youtube")
        self.assertEqual(result[3].text_type, "link")
        self.assertEqual(result[3].url, "https://www.youtube.com/@bootdotdev")

    def test_split_nodes_no_link(self):
        node = TextNode("This is text with a link to boot dev and to youtube", "text")
        result = nodeutils.split_nodes_link([node])
        self.assertEqual(result[0].text, "This is text with a link to boot dev and to youtube")
        self.assertEqual(result[0].text_type, "text")
        self.assertEqual(len(result), 1)

if __name__ == "__main__":
    unittest.main()