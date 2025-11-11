from typing import Union, List, Any

from ydnatl.core.element import HTMLElement


class Fragment(HTMLElement):
    """A container that renders only its children without wrapping tags.

    Useful for grouping elements without introducing extra DOM nodes.

    Example:
        fragment = Fragment(
            H1("Title"),
            Paragraph("Content")
        )
        # Renders: <h1>Title</h1><p>Content</p>
        # Instead of: <fragment><h1>Title</h1><p>Content</p></fragment>
    """

    def __init__(
        self, *children: Union["HTMLElement", str, List[Any]], **attributes: str
    ):
        # Initialize with a dummy tag name since we won't render it
        super().__init__(*children, tag="fragment", **attributes)

    def render(self, pretty: bool = False, _indent: int = 0) -> str:
        """Renders only the children without the fragment wrapper.

        Args:
            pretty: If True, renders children with indentation
            _indent: Internal parameter for tracking indentation level

        Returns:
            HTML string of all children concatenated
        """
        self.on_before_render()

        # Render only children, not the fragment tag itself
        if pretty:
            result = "".join(
                child.render(pretty=True, _indent=_indent) for child in self._children
            )
        else:
            result = "".join(
                child.render(pretty=False, _indent=_indent) for child in self._children
            )

        # Include text content if any
        if self._text:
            import html

            result = html.escape(self._text) + result

        self.on_after_render()
        return result
