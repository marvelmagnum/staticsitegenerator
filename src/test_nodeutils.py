import unittest
import nodeutils
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image
)

class TestNodeUtils(unittest.TestCase):
    def test_start(self):
        node = TextNode("**This** is text with a code block word", text_type_text)
        new_nodes = nodeutils.split_textnode_delimiter([node], "**", text_type_bold)
        self.assertEqual(new_nodes[0].text, "This")
        self.assertEqual(new_nodes[0].text_type, text_type_bold)
        self.assertEqual(new_nodes[1].text, " is text with a code block word")
        self.assertEqual(new_nodes[1].text_type, text_type_text)

    def test_middle(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = nodeutils.split_textnode_delimiter([node], "`", text_type_code)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, text_type_text)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, text_type_code)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, text_type_text)

    def test_end(self):
        node = TextNode("This is text with a code block *word*", text_type_text)
        new_nodes = nodeutils.split_textnode_delimiter([node], "*", text_type_italic)
        self.assertEqual(new_nodes[0].text, "This is text with a code block ")
        self.assertEqual(new_nodes[0].text_type, text_type_text)
        self.assertEqual(new_nodes[1].text, "word")
        self.assertEqual(new_nodes[1].text_type, text_type_italic)

    def test_non_text(self):
        node = TextNode("This is text with a code block *word*", text_type_italic)
        new_nodes = nodeutils.split_textnode_delimiter([node], "*", text_type_italic)
        self.assertEqual(new_nodes[0].text, "This is text with a code block *word*")
        self.assertEqual(new_nodes[0].text_type, text_type_italic)

    def test_split_textnode_except(self):
        node = TextNode("This is text with a **code block word", text_type_text)
        with self.assertRaises(SyntaxError):
            nodeutils.split_textnode_delimiter([node], "**", text_type_bold)

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

    def test_split_nodes_image_start(self):
        node = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) are in this text", text_type_text)
        result = nodeutils.split_nodes_image([node])
        self.assertEqual(result[0].text, "rick roll")
        self.assertEqual(result[0].text_type, text_type_image)
        self.assertEqual(result[0].url, "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(result[1].text, " and ")
        self.assertEqual(result[1].text_type, text_type_text)
        self.assertEqual(result[2].text, "obi wan")
        self.assertEqual(result[2].text_type, text_type_image)
        self.assertEqual(result[2].url, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(result[3].text, " are in this text")
        self.assertEqual(result[3].text_type, text_type_text)
        
    def test_split_nodes_image_end(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", text_type_text)
        result = nodeutils.split_nodes_image([node])
        self.assertEqual(result[0].text, "This is text with a ")
        self.assertEqual(result[0].text_type, text_type_text)
        self.assertEqual(result[1].text, "rick roll")
        self.assertEqual(result[1].text_type, text_type_image)
        self.assertEqual(result[1].url, "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(result[2].text, " and ")
        self.assertEqual(result[2].text_type, text_type_text)
        self.assertEqual(result[3].text, "obi wan")
        self.assertEqual(result[3].text_type, text_type_image)
        self.assertEqual(result[3].url, "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_split_nodes_no_image(self):
        node = TextNode("This is text with a rick roll and obi wan", text_type_text)
        result = nodeutils.split_nodes_image([node])
        self.assertEqual(result[0].text, "This is text with a rick roll and obi wan")
        self.assertEqual(result[0].text_type, text_type_text)
        self.assertEqual(len(result), 1)

    def test_split_nodes_link_begin(self):
        node = TextNode("[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) are links in this text", text_type_text)
        result = nodeutils.split_nodes_link([node])
        self.assertEqual(result[0].text, "to boot dev")
        self.assertEqual(result[0].text_type, text_type_link)
        self.assertEqual(result[0].url, "https://www.boot.dev")
        self.assertEqual(result[1].text, " and ")
        self.assertEqual(result[1].text_type, text_type_text)
        self.assertEqual(result[2].text, "to youtube")
        self.assertEqual(result[2].text_type, text_type_link)
        self.assertEqual(result[2].url, "https://www.youtube.com/@bootdotdev")
        self.assertEqual(result[3].text, " are links in this text")
        self.assertEqual(result[3].text_type, text_type_text)

    def test_split_nodes_link_end(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", text_type_text)
        result = nodeutils.split_nodes_link([node])
        self.assertEqual(result[0].text, "This is text with a link ")
        self.assertEqual(result[0].text_type, text_type_text)
        self.assertEqual(result[1].text, "to boot dev")
        self.assertEqual(result[1].text_type, text_type_link)
        self.assertEqual(result[1].url, "https://www.boot.dev")
        self.assertEqual(result[2].text, " and ")
        self.assertEqual(result[2].text_type, text_type_text)
        self.assertEqual(result[3].text, "to youtube")
        self.assertEqual(result[3].text_type, text_type_link)
        self.assertEqual(result[3].url, "https://www.youtube.com/@bootdotdev")

    def test_split_nodes_no_link(self):
        node = TextNode("This is text with a link to boot dev and to youtube", text_type_text)
        result = nodeutils.split_nodes_link([node])
        self.assertEqual(result[0].text, "This is text with a link to boot dev and to youtube")
        self.assertEqual(result[0].text_type, text_type_text)
        self.assertEqual(len(result), 1)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = nodeutils.text_to_textnodes(text)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, text_type_text)
        self.assertEqual(result[1].text, "text")
        self.assertEqual(result[1].text_type, text_type_bold)
        self.assertEqual(result[2].text, " with an ")
        self.assertEqual(result[2].text_type, text_type_text)
        self.assertEqual(result[3].text, "italic")
        self.assertEqual(result[3].text_type, text_type_italic)
        self.assertEqual(result[4].text, " word and a ")
        self.assertEqual(result[4].text_type, text_type_text)
        self.assertEqual(result[5].text, "code block")
        self.assertEqual(result[5].text_type, text_type_code)
        self.assertEqual(result[6].text, " and an ")
        self.assertEqual(result[6].text_type, text_type_text)
        self.assertEqual(result[7].text, "obi wan image")
        self.assertEqual(result[7].text_type, text_type_image)
        self.assertEqual(result[7].url, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(result[8].text, " and a ")
        self.assertEqual(result[8].text_type, text_type_text)
        self.assertEqual(result[9].text, "link")
        self.assertEqual(result[9].text_type, text_type_link)
        self.assertEqual(result[9].url, "https://boot.dev")

if __name__ == "__main__":
    unittest.main()