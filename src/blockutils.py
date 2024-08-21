import re

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
