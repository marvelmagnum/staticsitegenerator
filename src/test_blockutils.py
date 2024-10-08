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


class TestBlockIdentifiers(unittest.TestCase):
    def test_heading1(self):
        text = "## This is a heading"
        self.assertEqual(blockutils.__is_heading___(text), True)

    def test_heading2(self):
        text = "####### This is not a heading"
        self.assertEqual(blockutils.__is_heading___(text), False)

    def test_heading2(self):
        text = "#This is not a heading"
        self.assertEqual(blockutils.__is_heading___(text), False) 

    def test_heading2(self):
        text = "This is # not a heading"
        self.assertEqual(blockutils.__is_heading___(text), False) 

    def test_code1(self):
        text = "```This is a code block```"
        self.assertEqual(blockutils.__is_code___(text), True)

    def test_code2(self):
        text = """```This is a code block
        still continues```"""
        self.assertEqual(blockutils.__is_code___(text), True)

    def test_code3(self):
        text = """``This is a not code block
        still continues```"""
        self.assertEqual(blockutils.__is_code___(text), False)

    def test_code4(self):
        text = """```This is a not code block
        still continues`"""
        self.assertEqual(blockutils.__is_code___(text), False)

    def test_code5(self):
        text = """This is a ```not``` code block
        still continues"""
        self.assertEqual(blockutils.__is_code___(text), False)

    def test_quote1(self):
        text = "> This is a quote block"
        self.assertEqual(blockutils.__is_quote___(text), True)

    def test_quote2(self):
        text = """>This is a quote block
> still continues"""
        self.assertEqual(blockutils.__is_quote___(text), True)

    def test_quote3(self):
        text = """>> This is a quote block
> still continues"""
        self.assertEqual(blockutils.__is_quote___(text), True)

    def test_quote4(self):
        text = """>This is a quote block
>>still continues`"""
        self.assertEqual(blockutils.__is_quote___(text), True)

    def test_quote5(self):
        text = """This is a > not quote block
>still continues"""
        self.assertEqual(blockutils.__is_quote___(text), False)

    def test_uo_list1(self):
        text = """* list item1
- list item2
- list item3
* list item4"""
        self.assertEqual(blockutils.__is__unordered_list__(text), True)

    def test_uo_list2(self):
        text = """* list item1
-list item2
- list item3
* list item4"""
        self.assertEqual(blockutils.__is__unordered_list__(text), False)

    def test_uo_list3(self):
        text = """* list item1
- list item2
list item3
* list item4"""
        self.assertEqual(blockutils.__is__unordered_list__(text), False) 

    def test_uo_list4(self):
        text = """* list item1
* list item2
* list item3
* list item4"""
        self.assertEqual(blockutils.__is__unordered_list__(text), True)

    def test_uo_list5(self):
        text = """* list item1
* list item2
* list - item3
* list item4"""
        self.assertEqual(blockutils.__is__unordered_list__(text), True)

    def test_uo_list6(self):
        text = """- list item1
- list item2
list - item3
- list item4"""
        self.assertEqual(blockutils.__is__unordered_list__(text), False)

    def test_o_list1(self):
        text = """1. list item1
2. list item2
3. list item3
4. list item4"""
        self.assertEqual(blockutils.__is__ordered_list__(text), True)

    def test_o_list2(self):
        text = """1. list item1
2.list item2
3. list item3
4. list item4"""
        self.assertEqual(blockutils.__is__ordered_list__(text), False)

    def test_o_list3(self):
        text = """1. list item1
2. list item2
list item3
3. list item4"""
        self.assertEqual(blockutils.__is__ordered_list__(text), False)

    def test_o_list4(self):
        text = """1 list item1
2 list item2
3 list item3
4 list item4"""
        self.assertEqual(blockutils.__is__ordered_list__(text), False)

    def test_o_list5(self):
        text = """1. list item1
2. list item2
3. list 3. item3
4. list item4"""
        self.assertEqual(blockutils.__is__ordered_list__(text), True)

    def test_o_list6(self):
        text = """1. list item1
2. list item2
list 3. item3
4. list item4"""
        self.assertEqual(blockutils.__is__ordered_list__(text), False)

    def test_o_list7(self):
        text = """1. list item1
2. list item2
2. list item3
3. list item4"""
        self.assertEqual(blockutils.__is__ordered_list__(text), False)


class TestBlockToType(unittest.TestCase):
    def test_heading(self):
        text = "# This is a heading"
        self.assertEqual(blockutils.block_to_block_type(text), blockutils.block_type_heading)

    def test_code(self):
        text = """```This is a code block
        still continues```"""
        self.assertEqual(blockutils.block_to_block_type(text), blockutils.block_type_code)

    def test_quote(self):
        text = """>This is a quote block
> still continues"""
        self.assertEqual(blockutils.block_to_block_type(text), blockutils.block_type_quote)

    def test_unordered_list(self):
        text = """- list item1
- list item2
- list item3
- list item4"""
        self.assertEqual(blockutils.block_to_block_type(text), blockutils.block_type_unordered_list)

    def test_ordered_list(self):
        text = """1. list item1
2. list item2
3. list item3
4. list item4"""
        self.assertEqual(blockutils.block_to_block_type(text), blockutils.block_type_ordered_list)

    def test_paragraph(self):
        text = """This is a paragraph of text. It has some **bold** and *italic* words inside of it.
More blah blah text here."""
        self.assertEqual(blockutils.block_to_block_type(text), blockutils.block_type_paragraph)


class TestMarkdownToHTML(unittest.TestCase):
    def test_heading(self):
        md = """# This is a heading"""
        html = blockutils.markdown_to_html_node(md)
        self.assertEqual(html.to_html(), "<div><h1>This is a heading</h1></div>")

    def test_code(self):
        md = """```
{
    red = 1,
    blue = 2
}
```"""
        html = blockutils.markdown_to_html_node(md)
        self.assertEqual(html.to_html(), """<div><pre><code>
{
    red = 1,
    blue = 2
}
</code></pre></div>""")
        
    def test_quote(self):
        md = """>Roses are red,
>   Violets are blue."""
        html = blockutils.markdown_to_html_node(md)
        self.assertEqual(html.to_html(), """<div><blockquote>Roses are red,
Violets are blue.</blockquote></div>""")
        
    def test_uo_list(self):
        md = """* This is the first list item in a list block
* This is a list item
* This is another list item"""
        html = blockutils.markdown_to_html_node(md)
        self.assertEqual(html.to_html(), "<div><ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul></div>")
    
    def test_uo_list(self):
        md = """1. This is the first list item in a list block
2. This is a list item
3. This is another list item"""
        html = blockutils.markdown_to_html_node(md)
        self.assertEqual(html.to_html(), "<div><ol><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ol></div>")

    def test_paragraph(self):
        md = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        html = blockutils.markdown_to_html_node(md)
        self.assertEqual(html.to_html(), "<div><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p></div>")

    def test_all(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

1. This is the first list item in a list block
2. This is a list item
3. This is another list item

```
{
    red = 1,
    blue = 2
}
```

>Roses are red,
>   Violets are blue."""
        html = blockutils.markdown_to_html_node(md)
        self.assertEqual(html.to_html(), """<div><h1>This is a heading</h1><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul><ol><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ol><pre><code>
{
    red = 1,
    blue = 2
}
</code></pre><blockquote>Roses are red,
Violets are blue.</blockquote></div>""")
        

class TestExtractTitle(unittest.TestCase):
    def test_h1(self):
        text = "# This is h1"
        self.assertEqual(blockutils.extract_title(text), "This is h1")

    def test_no_h1_except(self):
        text = "## This is h1"
        with self.assertRaises(SyntaxError):
            blockutils.extract_title(text)