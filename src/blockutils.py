
def markdown_to_blocks(markdown):
    result = list(filter(lambda x: x, list(map(lambda x: x.strip(), markdown.split("\n\n")))))
    return result
