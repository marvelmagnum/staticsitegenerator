from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image
)


def main():
    text_node = TextNode("This is a test node", text_type_bold, "https://www.boot.dev")
    print(text_node)

main()
