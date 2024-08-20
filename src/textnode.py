from leafnode import LeafNode

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, text_node):
        return text_node.text == self.text and \
               text_node.text_type == self.text_type and \
               text_node.url == self.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def text_node_to_html_node(self):
        match (self.text_type):
            case "text":   return LeafNode(None, self.text)
            case "bold":   return LeafNode("b", self.text)
            case "italic": return LeafNode("i", self.text)
            case "code":   return LeafNode("code", self.text)
            case "link":   return LeafNode("a", self.text, {"href": self.url})
            case "image":  return LeafNode("img", " ", {"src": self.url, "alt": self.text})
            case _:        raise ValueError("Invalid text type")