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

            work_lst.append(TextNode(f'"{chunks[i]}"', f'"{text_type}"' if is_inline else f'"text"'))
            is_inline = not is_inline

        result += work_lst
    return result