import uuid
import copy
import os
import functools
from ydnatl.core.cycode.cython_render import render_c
from typing import Callable, Any, Iterator, Union, List


class HTMLElement:
    __slots__ = ["_tag", "_children", "_text", "_attributes", "_self_closing"]

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
        
        fixed_attributes = {(k if k in PRESERVE_UNDERSCORE else k.replace("_", "-")): v for k, v in attributes.items()}

        self._tag: str = tag
        self._children: List[HTMLElement] = []
        self._text: str = ""
        self._attributes: dict = fixed_attributes
        self._self_closing: bool = self_closing

        if os.environ.get("YDNATL_GENERATE_IDS"):
            self.generate_id()

        for child in self._flatten(children):
            self._add_child(child)

        self.on_load()

    def __str__(self) -> str:
        return self.render()
    
    def __del__(self) -> None:
        self.on_unload()

    @staticmethod
    def _flatten(items: Union[List[Any], tuple]) -> Iterator[Any]:
        """Recursively flattens nested iterables of children."""
        for item in items:
            if isinstance(item, (list, tuple)):
                yield from HTMLElement._flatten(item)
            else:
                yield item

    def _add_child(self, child: Union["HTMLElement", str]) -> None:
        """Adds a single child to the element."""
        if isinstance(child, HTMLElement):
            self._children.append(child)
        elif isinstance(child, str):
            self._text += child

    def prepend(self, *children: Union["HTMLElement", str, List[Any]]) -> None:
        """Prepends children to the current tag."""
        new_children: List[HTMLElement] = []
        for child in self._flatten(children):
            if isinstance(child, HTMLElement):
                new_children.append(child)
            elif isinstance(child, str):
                self._text = child + self._text
            else:
                raise ValueError(f"Invalid child type: {child}")
        self._children = new_children + self._children

    def append(self, *children: Union["HTMLElement", str, List[Any]]) -> None:
        """Appends children to the current tag."""
        for child in self._flatten(children):
            self._add_child(child)

    def filter(
        self, condition: Callable[[Any], bool], recursive: bool = False
    ) -> Iterator["HTMLElement"]:
        """Yields children (and optionally descendants) that meet the condition."""
        for child in self._children:
            if condition(child):
                yield child
            if recursive:
                yield from child.filter(condition, recursive=True)

    def remove_all(self, condition: Callable[[Any], bool]) -> None:
        """Removes all children that meet the condition."""
        to_remove = list(self.filter(condition))
        for child in to_remove:
            if child in self._children:
                self._children.remove(child)

    def clear(self) -> None:
        """Clears all children from the tag."""
        self._children.clear()

    def pop(self, index: int = 0) -> "HTMLElement":
        """Pops a child from the tag."""
        return self._children.pop(index)

    def first(self) -> Union["HTMLElement", None]:
        """Returns the first child of the tag."""
        return self._children[0] if self._children else None

    def last(self) -> Union["HTMLElement", None]:
        """Returns the last child of the tag."""
        return self._children[-1] if self._children else None

    def add_attribute(self, key: str, value: str) -> None:
        """Adds an attribute to the current tag."""
        self._attributes[key] = value
        
    def add_attributes(self, attributes: list[tuple[str, str]]) -> None:
        """Adds multiple attributes to the current tag."""
        for key, value in attributes:
            self._attributes[key] = value
        
    def remove_attribute(self, key: str) -> None:
        """Removes an attribute from the current tag."""
        self._attributes.pop(key, None)

    def get_attribute(self, key: str) -> Union[str, None]:
        """Gets an attribute from the current tag."""
        return self._attributes.get(key)

    def has_attribute(self, key: str) -> bool:
        """Checks if an attribute exists in the current tag."""
        return key in self._attributes

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

    def find_by_attribute(self, attr_name: str, attr_value: Any) -> Union["HTMLElement", None]:
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

    @property
    def self_closing(self) -> bool:
        return self._self_closing

    @self_closing.setter
    def self_closing(self, value: bool) -> None:
        self._self_closing = value

    def _render_attributes(self) -> str:
        """Returns a string of HTML attributes for the tag."""
        attr_str = " ".join(
            f'{("class" if k == "class_name" else k)}="{v}"'
            for k, v in self._attributes.items()
        )
        return f" {attr_str}" if attr_str else ""

    def render(self) -> str:
        """Renders the HTML element and its children to a string."""
        self.on_before_render()
        attributes = self._render_attributes()
        tag_start = f"<{self._tag}{attributes}"

        if self._self_closing:
            result = f"{tag_start} />"
        else:
            children_html = "".join(child.render() for child in self._children)
            result = f"{tag_start}>{self._text}{children_html}</{self._tag}>"

        if hasattr(self, "_prefix") and self._prefix:
            result = f"{self._prefix}{result}"

        self.on_after_render()
        return result
    
    def render_c(self) -> str:
        return render_c(self)

    def to_dict(self) -> dict:
        return {
            "tag": self._tag,
            "self_closing": self._self_closing,
            "attributes": self._attributes.copy(),
            "text": self._text,
            "children": list(map(lambda child: child.to_dict(), self._children))
        }