class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ""
        result = ""
        for attrib in self.props:
            result = result + f' {attrib}="{self.props[attrib]}"'
        return result
    
    def __repr__(self):
        str = ""
        for child in self.children:
            str += child.to_html()

        result = self.to_html()
        return result


        