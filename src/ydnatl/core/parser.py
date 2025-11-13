"""HTML Parser for YDNATL - Convert raw HTML to YDNATL elements."""

from html.parser import HTMLParser
from typing import List, Optional, Union

from ydnatl.core.element import HTMLElement


class YDNATLHTMLParser(HTMLParser):
    """Parse HTML and convert to YDNATL element tree."""

    VOID_ELEMENTS = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }

    def __init__(self):
        super().__init__()
        self.roots: List[HTMLElement] = []
        self.stack: List[HTMLElement] = []
        self.current: Optional[HTMLElement] = None
        self.text_buffer: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[tuple]):
        """Handle opening tags."""
        self._flush_text_buffer()

        attributes = {}
        for key, value in attrs:
            if key == "class":
                attributes["class_name"] = value
            else:
                attributes[key.replace("-", "_")] = value if value is not None else ""

        is_self_closing = tag in self.VOID_ELEMENTS

        element = HTMLElement(tag=tag, self_closing=is_self_closing, **attributes)

        if self.current is not None:
            self.current.append(element)
        else:
            self.roots.append(element)

        if not is_self_closing:
            self.stack.append(element)
            self.current = element

    def handle_endtag(self, tag: str):
        """Handle closing tags."""
        self._flush_text_buffer()

        if self.stack and self.stack[-1].tag == tag:
            self.stack.pop()
            self.current = self.stack[-1] if self.stack else None

    def handle_data(self, data: str):
        """Handle text content between tags."""
        text = data.strip()
        if text and self.current is not None:
            self.text_buffer.append(text)

    def _flush_text_buffer(self):
        """Flush accumulated text to the current element."""
        if self.text_buffer and self.current is not None:
            if self.current.text:
                self.current.text += "".join(self.text_buffer)
            else:
                self.current.text = "".join(self.text_buffer)
            self.text_buffer.clear()

    def parse_html(self, html_string: str) -> Optional[HTMLElement]:
        """Parse HTML string and return root element."""
        self.feed(html_string)
        return self.roots[0] if self.roots else None

    def parse_fragment(self, html_string: str) -> List[HTMLElement]:
        """Parse HTML fragment and return list of elements."""
        self.feed(html_string)
        return self.roots


def from_html(
    html_string: str, fragment: bool = False
) -> Union[HTMLElement, List[HTMLElement], None]:
    """Parse HTML string and convert to YDNATL element(s).

    Args:
        html_string: Raw HTML string to parse
        fragment: If True, returns list of elements (for HTML fragments)
                 If False, returns single root element (default)

    Returns:
        HTMLElement if fragment=False, List[HTMLElement] if fragment=True

    Example:
        >>> from ydnatl.core.parser import from_html
        >>>
        >>> # Parse single element
        >>> element = from_html('<div class="container"><h1>Hello</h1></div>')
        >>> print(element.render())
        <div class="container"><h1>Hello</h1></div>
        >>>
        >>> # Parse fragment (multiple root elements)
        >>> elements = from_html('<h1>Title</h1><p>Content</p>', fragment=True)
        >>> for el in elements:
        ...     print(el.render())
    """
    parser = YDNATLHTMLParser()

    if fragment:
        return parser.parse_fragment(html_string)
    else:
        return parser.parse_html(html_string)


# Add convenience method to HTMLElement
def _from_html_classmethod(cls, html_string: str, fragment: bool = False):
    """Parse HTML string and convert to HTMLElement(s).

    This is a class method added to HTMLElement for convenience.

    Args:
        html_string: Raw HTML string to parse
        fragment: If True, returns list of elements

    Returns:
        HTMLElement or List[HTMLElement]
    """
    return from_html(html_string, fragment=fragment)


# Monkey-patch HTMLElement to add from_html class method
HTMLElement.from_html = classmethod(_from_html_classmethod)
