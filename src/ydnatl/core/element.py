import copy
import html
import json
import os
import uuid
from typing import Callable, Any, Iterator, Union, List, TypeVar

T = TypeVar("T", bound="HTMLElement")


class HTMLElement:
    __slots__ = ["_tag", "_children", "_text", "_attributes", "_self_closing", "_styles_cache"]

    def __init__(
        self,
        *children: Union["HTMLElement", str, List[Any]],
        tag: str,
        self_closing: bool = False,
        **attributes: str,
    ):
        PRESERVE_UNDERSCORE = {"class_name"}

        if not tag:
            raise ValueError("A valid HTML tag name is required")

        fixed_attributes = {
            (k if k in PRESERVE_UNDERSCORE else k.replace("_", "-")): v
            for k, v in attributes.items()
        }

        self._tag: str = tag
        self._children: List[HTMLElement] = []
        self._text: str = ""
        self._attributes: dict = fixed_attributes
        self._self_closing: bool = self_closing
        self._styles_cache: Union[dict, None] = None

        if os.environ.get("YDNATL_GENERATE_IDS"):
            self.generate_id()

        # Batch text children to avoid repeated string concatenation
        text_parts: List[str] = []
        for child in self._flatten(children):
            if isinstance(child, HTMLElement):
                self._children.append(child)
            elif isinstance(child, str):
                text_parts.append(child)
        if text_parts:
            self._text = "".join(text_parts)

        self.on_load()

    def __str__(self) -> str:
        return self.render()

    def __del__(self) -> None:
        self.on_unload()

    def __enter__(self) -> "HTMLElement":
        """Context manager entry - returns self for use in with statements."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - no cleanup needed."""
        pass

    @staticmethod
    def _flatten(items: Union[List[Any], tuple]) -> Iterator[Any]:
        """Recursively flattens nested iterables of children."""
        for item in items:
            if isinstance(item, (list, tuple)):
                yield from HTMLElement._flatten(item)
            else:
                yield item

    def prepend(self, *children: Union["HTMLElement", str, List[Any]]) -> "HTMLElement":
        """Prepends children to the current tag.

        Returns:
            self for method chaining
        """
        new_children: List[HTMLElement] = []
        text_parts: List[str] = []
        for child in self._flatten(children):
            if isinstance(child, HTMLElement):
                new_children.append(child)
            elif isinstance(child, str):
                text_parts.append(child)
            else:
                raise ValueError(f"Invalid child type: {child}")
        if text_parts:
            self._text = "".join(text_parts) + self._text
        self._children = new_children + self._children
        return self

    def append(self, *children: Union["HTMLElement", str, List[Any]]) -> "HTMLElement":
        """Appends children to the current tag.

        Returns:
            self for method chaining
        """
        text_parts: List[str] = []
        for child in self._flatten(children):
            if isinstance(child, HTMLElement):
                self._children.append(child)
            elif isinstance(child, str):
                text_parts.append(child)
        if text_parts:
            self._text += "".join(text_parts)
        return self

    def filter(
        self, condition: Callable[[Any], bool], recursive: bool = False
    ) -> Iterator["HTMLElement"]:
        """Yields children (and optionally descendants) that meet the condition."""
        for child in self._children:
            if condition(child):
                yield child
            if recursive:
                yield from child.filter(condition, recursive=True)

    def remove_all(self, condition: Callable[[Any], bool]) -> "HTMLElement":
        """Removes all children that meet the condition.

        Returns:
            self for method chaining
        """
        to_remove = list(self.filter(condition))
        for child in to_remove:
            if child in self._children:
                self._children.remove(child)
        return self

    def clear(self) -> "HTMLElement":
        """Clears all children from the tag.

        Returns:
            self for method chaining
        """
        self._children.clear()
        return self

    def pop(self, index: int = 0) -> "HTMLElement":
        """Pops a child from the tag."""
        return self._children.pop(index)

    def first(self) -> Union["HTMLElement", None]:
        """Returns the first child of the tag."""
        return self._children[0] if self._children else None

    def last(self) -> Union["HTMLElement", None]:
        """Returns the last child of the tag."""
        return self._children[-1] if self._children else None

    def add_attribute(self, key: str, value: str) -> "HTMLElement":
        """Adds an attribute to the current tag.

        Returns:
            self for method chaining
        """
        self._attributes[key] = value
        if key == "style":
            self._styles_cache = None
        return self

    def add_attributes(self, attributes: list[tuple[str, str]]) -> "HTMLElement":
        """Adds multiple attributes to the current tag.

        Returns:
            self for method chaining
        """
        has_style = False
        for key, value in attributes:
            self._attributes[key] = value
            if key == "style":
                has_style = True

        if has_style:
            self._styles_cache = None
        return self

    def remove_attribute(self, key: str) -> "HTMLElement":
        """Removes an attribute from the current tag.

        Returns:
            self for method chaining
        """
        self._attributes.pop(key, None)
        return self

    def get_attribute(self, key: str) -> Union[str, None]:
        """Gets an attribute from the current tag."""
        return self._attributes.get(key)

    def has_attribute(self, key: str) -> bool:
        """Checks if an attribute exists in the current tag."""
        return key in self._attributes

    def _get_styles_dict(self) -> dict:
        """Gets the cached styles dictionary, parsing if necessary.

        Returns:
            Dictionary of CSS properties and values
        """
        if self._styles_cache is None:
            current_style = self._attributes.get("style", "")
            self._styles_cache = self._parse_styles(current_style)
        return self._styles_cache

    def _flush_styles_cache(self) -> None:
        """Flushes the styles cache back to the style attribute."""
        if self._styles_cache is not None:
            if self._styles_cache:
                self._attributes["style"] = self._format_styles(self._styles_cache)
            else:
                self._attributes.pop("style", None)

    def add_style(self, key: str, value: str) -> "HTMLElement":
        """
        Adds a CSS style to the element's inline styles.

        Args:
            key: CSS property name (e.g., 'color', 'font-size')
            value: CSS property value (e.g., 'red', '14px')

        Returns:
            self for method chaining
        """
        styles_dict = self._get_styles_dict()
        styles_dict[key] = value
        self._flush_styles_cache()
        return self

    def add_styles(self, styles: dict) -> "HTMLElement":
        """
        Adds multiple CSS styles to the element's inline styles.

        Args:
            styles: Dictionary of CSS properties and values
                   e.g., {"color": "red", "font-size": "14px"}

        Returns:
            self for method chaining
        """
        styles_dict = self._get_styles_dict()
        styles_dict.update(styles)
        self._flush_styles_cache()
        return self

    def get_style(self, key: str) -> Union[str, None]:
        """
        Gets a specific CSS style value from the element's inline styles.

        Args:
            key: CSS property name

        Returns:
            The CSS property value or None if not found
        """
        styles_dict = self._get_styles_dict()
        return styles_dict.get(key)

    def remove_style(self, key: str) -> "HTMLElement":
        """
        Removes a CSS style from the element's inline styles.

        Args:
            key: CSS property name to remove

        Returns:
            self for method chaining
        """
        styles_dict = self._get_styles_dict()
        styles_dict.pop(key, None)
        self._flush_styles_cache()
        return self

    @staticmethod
    def _parse_styles(style_str: str) -> dict:
        """
        Parses a CSS style string into a dictionary.

        Args:
            style_str: CSS style string (e.g., "color: red; font-size: 14px")

        Returns:
            Dictionary of CSS properties and values
        """
        if not style_str:
            return {}

        styles = {}
        for style in style_str.split(";"):
            style = style.strip()
            if ":" in style:
                key, value = style.split(":", 1)
                styles[key.strip()] = value.strip()
        return styles

    @staticmethod
    def _format_styles(styles_dict: dict) -> str:
        """
        Formats a dictionary of styles into a CSS style string.

        Args:
            styles_dict: Dictionary of CSS properties and values

        Returns:
            CSS style string (e.g., "color: red; font-size: 14px")
        """
        return "; ".join(f"{k}: {v}" for k, v in styles_dict.items())

    def generate_id(self) -> None:
        """Generates an id for the current tag if not already present."""
        if "id" not in self._attributes:
            self._attributes["id"] = f"el-{str(uuid.uuid4())[:6]}"

    def clone(self) -> "HTMLElement":
        """Clones the current tag."""
        return copy.deepcopy(self)

    def replace_child(self, old_index: int, new_child: "HTMLElement") -> None:
        """Replaces a existing child element with a new child element."""
        self._children[old_index] = new_child

    def find_by_attribute(
        self, attr_name: str, attr_value: Any
    ) -> Union["HTMLElement", None]:
        """Finds a child by an attribute."""

        def _find(element: "HTMLElement") -> Union["HTMLElement", None]:
            if element.get_attribute(attr_name) == attr_value:
                return element
            for child in element._children:
                result = _find(child)
                if result:
                    return result
            return None

        return _find(self)

    def get_attributes(self, *keys: str) -> dict:
        """Returns the attributes of the current tag."""
        if keys:
            return {key: self._attributes.get(key) for key in keys}
        return self._attributes

    def count_children(self) -> int:
        """Returns the number of children in the current tag."""
        return len(self._children)

    def on_load(self) -> None:
        """Callback called when the tag is loaded."""
        pass

    def on_before_render(self) -> None:
        """Callback called before the tag is rendered."""
        pass

    def on_after_render(self) -> None:
        """Callback called after the tag is rendered."""
        pass

    def on_unload(self) -> None:
        """Callback called when the tag is unloaded."""
        pass

    @property
    def tag(self) -> str:
        return self._tag

    @tag.setter
    def tag(self, value: str) -> None:
        self._tag = value

    @property
    def children(self) -> List["HTMLElement"]:
        return self._children

    @children.setter
    def children(self, value: List["HTMLElement"]) -> None:
        self._children = value

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value

    @property
    def attributes(self) -> dict:
        return self._attributes

    @attributes.setter
    def attributes(self, value: dict) -> None:
        self._attributes = value
        self._styles_cache = None

    @property
    def self_closing(self) -> bool:
        return self._self_closing

    @self_closing.setter
    def self_closing(self, value: bool) -> None:
        self._self_closing = value

    def _render_attributes(self) -> str:
        """Returns a string of HTML attributes for the tag."""
        attr_str = " ".join(
            f'{("class" if k == "class_name" else k)}="{html.escape(str(v), quote=True)}"'
            for k, v in self._attributes.items()
        )
        return f" {attr_str}" if attr_str else ""

    def render(self, pretty: bool = False, _indent: int = 0) -> str:
        """
        Renders the HTML element and its children to a string.

        Args:
            pretty: If True, renders with indentation and newlines for readability
            _indent: Internal parameter for tracking indentation level

        Returns:
            String representation of the HTML element
        """
        self.on_before_render()

        attributes = self._render_attributes()
        indent_str = "  " * _indent if pretty else ""
        tag_start = f"{indent_str}<{self._tag}{attributes}"

        if self._self_closing:
            parts = [tag_start, " />"]
            if pretty:
                parts.append("\n")
            result = "".join(parts)
        else:
            if pretty and self._children:
                children_html = "".join(
                    child.render(pretty=True, _indent=_indent + 1)
                    for child in self._children
                )
                escaped_text = html.escape(self._text)

                if self._children or self._text:
                    parts = [tag_start, ">"]
                    if escaped_text:
                        parts.append(escaped_text)
                    if self._children:
                        parts.extend(["\n", children_html, indent_str])
                    parts.append(f"</{self._tag}>\n")
                    result = "".join(parts)
                else:
                    result = f"{tag_start}></{self._tag}>\n"
            else:
                children_html = "".join(
                    child.render(pretty=pretty, _indent=_indent + 1)
                    for child in self._children
                )
                escaped_text = html.escape(self._text)
                result = f"{tag_start}>{escaped_text}{children_html}</{self._tag}>"

        if hasattr(self, "_prefix") and self._prefix:
            result = f"{self._prefix}{result}"

        self.on_after_render()
        return result

    def to_dict(self) -> dict:
        return {
            "tag": self._tag,
            "self_closing": self._self_closing,
            "attributes": self._attributes.copy(),
            "text": self._text,
            "children": list(map(lambda child: child.to_dict(), self._children)),
        }

    def to_json(self, indent: int = None) -> str:
        """
        Serializes the element and its children to a JSON string.

        Args:
            indent: Number of spaces for JSON indentation (None for compact output)

        Returns:
            JSON string representation of the element
        """
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: dict) -> "HTMLElement":
        """
        Reconstructs an HTMLElement from a dictionary.

        Args:
            data: Dictionary containing element data (from to_dict())

        Returns:
            Reconstructed HTMLElement instance
        """
        if not isinstance(data, dict):
            raise ValueError("Input must be a dictionary")

        if "tag" not in data:
            raise ValueError("Dictionary must contain 'tag' key")

        element = cls(
            tag=data["tag"],
            self_closing=data.get("self_closing", False),
            **data.get("attributes", {}),
        )

        if "text" in data and data["text"]:
            element._text = data["text"]

        if "children" in data and data["children"]:
            for child_data in data["children"]:
                child = cls.from_dict(child_data)
                element._children.append(child)

        return element

    @classmethod
    def from_json(cls, json_str: str) -> "HTMLElement":
        """
        Reconstructs an HTMLElement from a JSON string.

        Args:
            json_str: JSON string representation (from to_json())

        Returns:
            Reconstructed HTMLElement instance
        """
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {e}")

        return cls.from_dict(data)
