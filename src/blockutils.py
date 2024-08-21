import re
import nodeutils
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)

block_type_heading = "heading"
block_type_paragraph = "paragraph"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered list"
block_type_ordered_list = "ordered_list"

# markdown blob to separate blocks
def markdown_to_blocks(markdown):
    result = list(filter(lambda x: x, list(map(lambda x: x.strip(), markdown.split("\n\n")))))
    return result

def __is_heading___(block):
    return len(re.findall(r"^#{1,6} ", block)) > 0

def __is_code___(block):
    code_mark = "```"
    return block[:3] == code_mark and block[-3:] == code_mark

def __is_quote___(block):
    lines = block.split('\n')
    matches = list(filter(lambda x: x[0] == '>', lines))
    return len(matches) == len(lines)

def __is__unordered_list__(block):
    lines = block.split('\n')
    matches = list(filter(lambda x: x[0:2] == '- ' or x[0:2] == '* ', lines))
    return len(matches) == len(lines)

def __is__ordered_list__(block):
    lines = block.split('\n')
    counter = 1
    for line in lines:
        if line[1:3] == '. ' and line[0] == str(counter):
            counter += 1
            continue
        else:
            return False
    return True

# identify block type
def block_to_block_type(block):
    if __is_heading___(block):
        return block_type_heading
    elif __is_code___(block):
        return block_type_code
    elif __is_quote___(block):
        return block_type_quote
    elif __is__unordered_list__(block):
        return block_type_unordered_list
    elif __is__ordered_list__(block):
        return block_type_ordered_list
    else:
        return block_type_paragraph
    
def text_to_child_HTML(text):
    result = []
    text_nodes = nodeutils.text_to_textnodes(text)
    for node in text_nodes:
        result.append(node.text_node_to_html_node())
    return result
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    content_html = []
    for block in blocks:
        block_html = []
        block_type = block_to_block_type(block)
        match(block_type):
            case "heading": 
                heading = block.split(' ', 1)
                str = heading[0].count('#')
                child_nodes = text_to_child_HTML(heading[1])
                block_html.append(ParentNode(f"h{str}", child_nodes))
            
            case "code":
                child_nodes = text_to_child_HTML(block)
                block_html.append(ParentNode(f"pre", child_nodes))

            case "paragraph":
                child_nodes = text_to_child_HTML(block)
                block_html.append(ParentNode(f"p", child_nodes))

            case "quote":
                quote_lines = list(map(lambda x: x[1:], block.split('\n')))
                quote = '\n'.join(quote_lines)
                child_nodes = text_to_child_HTML(quote)
                block_html.append(ParentNode(f"blockquote", child_nodes))

            case "unordered list":
                list_items = list(map(lambda x: x[2:], block.split('\n')))
                list_item_block = []
                for item in list_items:
                    child_nodes = text_to_child_HTML(item)
                    list_item_block.append(ParentNode(f"li", child_nodes))
                block_html.append(ParentNode(f"ul", list_item_block))

            case "ordered_list":
                list_items = list(map(lambda x: x[3:], block.split('\n')))
                list_item_block = []
                for item in list_items:
                    child_nodes = text_to_child_HTML(item)
                    list_item_block.append(ParentNode(f"li", child_nodes))
                block_html.append(ParentNode(f"ol", list_item_block))
        
        content_html.extend(block_html)
    return ParentNode("div", content_html)

