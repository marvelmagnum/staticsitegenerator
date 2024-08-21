import re
from textnode import TextNode

def split_textnode_delimiter(input_nodes, delimiter, text_type):
    result = []
    for node in input_nodes:
        if not isinstance(node, TextNode):
            raise ValueError("Only TextNode type input is allowed")
        
        if node.text_type != 'text':    #only text type is process. Other textnode types are unaffected.
            result.append(node)

        chunks = node.text.split(delimiter)
        if len(chunks) % 2 == 0: # unclosed delimiter 
            raise SyntaxError("Invalid markdown syntax")

        work_lst = []
        is_inline = False
        for i, val in enumerate(chunks):
            if not val: # skip invalid chunks in the middle (except 1st chunk)
                if i == 0:
                    is_inline = True
                continue

            work_lst.append(TextNode(chunks[i], text_type if is_inline else "text"))
            is_inline = not is_inline

        result += work_lst
    return result

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def __node_text_to_inline_type__(node_text, matches, token_template, type):
    result = []
    scan_text = node_text
    token_part1 = token_template.split("item1",1)
    token_part23 = token_part1[1].split("item2",1)
    tokens = [token_part1[0]] + token_part23
    
    for match in matches:
        token = f"{tokens[0]}{match[0]}{tokens[1]}{match[1]}{tokens[2]}"
        chunks = scan_text.split(token, 1)
        if chunks[0]:   # create nodes for non-empty chunks
            result.append(TextNode(chunks[0], "text"))
        result.append(TextNode(match[0], type, match[1]))
        if len(chunks) == 2:
            scan_text = chunks[1]
    return result

def split_nodes_image(input_nodes):
    result = []
    for node in input_nodes:
        if not isinstance(node, TextNode):
            raise ValueError("Only TextNode type input is allowed")
        
        if node.text_type != 'text':    # only text type is process. Other textnode types are unaffected.
            result.append(node)

        matches = extract_markdown_images(node.text)

        if not matches:     # nodes without image links are unaffected
            result.append(node)

        result += __node_text_to_inline_type__(node.text, matches, f"![item1](item2)", "image")
    return result

def split_nodes_link(input_nodes):
    result = []
    for node in input_nodes:
        if not isinstance(node, TextNode):
            raise ValueError("Only TextNode type input is allowed")
        
        if node.text_type != 'text':    # only text type is process. Other textnode types are unaffected.
            result.append(node)

        matches = extract_markdown_links(node.text)

        if not matches:     # nodes without image links are unaffected
            result.append(node)

        
        result += __node_text_to_inline_type__(node.text, matches, f"[item1](item2)", "link")
    return result
