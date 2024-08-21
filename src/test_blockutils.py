import unittest
import blockutils

class TestMarkdownToBlock(unittest.TestCase):
    def test_markdown_default(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        
        result = blockutils.markdown_to_blocks(text)
        self.assertEqual(result[0], '# This is a heading')
        self.assertEqual(result[1], 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.')
        self.assertEqual(result[2], '* This is the first list item in a list block\n* This is a list item\n* This is another list item')

    def test_markdown_extra_newlines(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.



* This is the first list item in a list block
* This is a list item
* This is another list item"""
        
        result = blockutils.markdown_to_blocks(text)
        self.assertEqual(result[0], '# This is a heading')
        self.assertEqual(result[1], 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.')
        self.assertEqual(result[2], '* This is the first list item in a list block\n* This is a list item\n* This is another list item')

    def test_markdown_extra_whitespace(self):
        text = """        # This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.        



         * This is the first list item in a list block
* This is a list item
* This is another list item             """
        
        result = blockutils.markdown_to_blocks(text)
        self.assertEqual(result[0], '# This is a heading')
        self.assertEqual(result[1], 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.')
        self.assertEqual(result[2], '* This is the first list item in a list block\n* This is a list item\n* This is another list item')