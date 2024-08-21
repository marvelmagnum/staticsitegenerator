import re
from textnode import TextNode

def split_textnode_delimiter(input_nodes, delimiter, text_type):
    result = []
    for node in input_nodes:
        if not isinstance(node, TextNode):
            raise ValueError("Only TextNode type input is allowed")
        
        if node.text_type != 'text':    #only text type is process. Other textnode types are unaffected.
            result.append(node)
            continue

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
    last_chunk = node_text
    token_part1 = token_template.split("item1",1)
    token_part23 = token_part1[1].split("item2",1)
    tokens = [token_part1[0]] + token_part23
    
    for match in matches:
        token = f"{tokens[0]}{match[0]}{tokens[1]}{match[1]}{tokens[2]}"
        chunks = last_chunk.split(token, 1)
        if chunks[0]:   # create nodes for non-empty chunks
            result.append(TextNode(chunks[0], "text"))
        result.append(TextNode(match[0], type, match[1]))
        last_chunk = chunks[1]

    if last_chunk:  # add any residual content
        result.append(TextNode(last_chunk, "text"))

    return result

def split_nodes_image(input_nodes):
    result = []
    for node in input_nodes:
        if not isinstance(node, TextNode):
            raise ValueError("Only TextNode type input is allowed")
    
        if node.text_type != 'text':    # only text type is process. Other textnode types are unaffected.
            result.append(node)
            continue

        matches = extract_markdown_images(node.text)

        if not matches:     # nodes without image links are unaffected
            result.append(node)
            continue

        result += __node_text_to_inline_type__(node.text, matches, f"![item1](item2)", "image")
    return result

def split_nodes_link(input_nodes):
    result = []
    for node in input_nodes:
        if not isinstance(node, TextNode):
            raise ValueError("Only TextNode type input is allowed")
        
        if node.text_type != 'text':    # only text type is process. Other textnode types are unaffected.
            result.append(node)
            continue

        matches = extract_markdown_links(node.text)

        if not matches:     # nodes without image links are unaffected
            result.append(node)
            continue
        
        result += __node_text_to_inline_type__(node.text, matches, f"[item1](item2)", "link")
    return result

def text_to_textnodes(text):
    text_node = TextNode(text, "text")
    result = split_textnode_delimiter([text_node], "**", "bold")
    result = split_textnode_delimiter(result, "*", "italic")
    result = split_textnode_delimiter(result, "`", "code")
    result = split_nodes_image(result)
    result = split_nodes_link(result)
    return result
