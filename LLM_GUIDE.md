# YDNATL - LLM Developer Guide

**Version:** 1.0.x
**Language:** Python 3.8+
**Dependencies:** None (pure Python, uses only stdlib)

## Overview

YDNATL (You Don't Need Another Template Language) is a Python library for programmatic HTML generation. It uses a declarative, class-based API similar to Flutter's widget system. All elements are subclasses of `HTMLElement` and support method chaining, context managers, and serialization.

## Core Concepts

### 1. Element Hierarchy
- All HTML elements inherit from `HTMLElement`
- Elements can have children (other elements)
- Elements have attributes (HTML attributes like id, class, etc.)
- Elements have text content
- Some elements are self-closing (br, img, hr, input, etc.)

### 2. Rendering
- `render()` method converts element tree to HTML string
- Supports compact (default) and pretty (indented) output
- Automatic HTML entity escaping for security

### 3. Serialization
- Elements can be serialized to JSON (`to_json()`)
- Elements can be deserialized from JSON (`from_json()`)
- Elements can be parsed from HTML strings (`from_html()`)

---

## Import Patterns

### Import Everything (Quick Start)
```python
from ydnatl import *
```

### Selective Imports (Recommended for Production)
```python
from ydnatl import HTMLElement, Fragment, from_html
from ydnatl.tags.text import H1, Paragraph, Span
from ydnatl.tags.layout import Div, Section
from ydnatl.tags.form import Form, Input, Button
```

### Import from Core
```python
from ydnatl.core.element import HTMLElement
from ydnatl.core.fragment import Fragment
from ydnatl.core.parser import from_html
```

---

## HTMLElement Class

**Location:** `ydnatl.core.element.HTMLElement`

### Constructor

```python
HTMLElement(
    *children,           # Variable number of child elements or text
    tag: str = "div",   # HTML tag name
    text: str = "",     # Text content
    self_closing: bool = False,  # Whether element is self-closing
    **attributes        # HTML attributes as keyword arguments
)
```

**Special Attribute Handling:**
- `class_name` → renders as `class` attribute
- `data_*` attributes → preserved with hyphens (data-value)
- Boolean attributes (checked, disabled) → rendered without values when True
- `style` → can be string or managed via style helper methods

**Example:**
```python
div = HTMLElement(
    H1("Title"),
    Paragraph("Content"),
    tag="div",
    id="main",
    class_name="container",
    data_value="123"
)
```

### Properties

| Property       | Type                     | Description       | Mutable               |
|----------------|--------------------------|-------------------|-----------------------|
| `tag`          | str                      | HTML tag name     | Yes                   |
| `children`     | List[HTMLElement \| str] | Child elements    | Yes (but use methods) |
| `text`         | str                      | Text content      | Yes                   |
| `attributes`   | Dict[str, str]           | HTML attributes   | Yes (but use methods) |
| `self_closing` | bool                     | Self-closing flag | Yes                   |

---

## Element Manipulation Methods

### Adding Children

#### append(*children) → self
Adds children to end of children list.

```python
div = Div()
div.append(H1("Title"))
div.append(Paragraph("Para 1"), Paragraph("Para 2"))
```

**Parameters:**
- `*children`: Variable number of HTMLElement or str

**Returns:** self (for chaining)

#### prepend(*children) → self
Adds children to beginning of children list.

```python
div = Div(Paragraph("Second"))
div.prepend(H1("First"))  # H1 now comes before Paragraph
```

**Parameters:**
- `*children`: Variable number of HTMLElement or str

**Returns:** self (for chaining)

### Removing Children

#### clear() → self
Removes all children.

```python
div.clear()  # Now has no children
```

**Returns:** self (for chaining)

#### pop(index: int = -1) → HTMLElement
Removes and returns child at index.

```python
last_child = div.pop()      # Remove last child
first_child = div.pop(0)    # Remove first child
```

**Parameters:**
- `index`: int (default: -1) - Index of child to remove

**Returns:** Removed HTMLElement

#### remove_all(condition: Callable) → self
Removes all children matching condition.

```python
# Remove all paragraphs
div.remove_all(lambda el: el.tag == "p")

# Remove elements with specific class
div.remove_all(lambda el: el.get_attribute("class_name") == "hidden")
```

**Parameters:**
- `condition`: Callable[[HTMLElement], bool] - Function that returns True for elements to remove

**Returns:** self (for chaining)

### Querying Children

#### filter(condition: Callable) → Iterator[HTMLElement]
Returns iterator of children matching condition.

```python
# Get all paragraphs
paragraphs = list(div.filter(lambda el: el.tag == "p"))

# Get elements with specific attribute
highlighted = list(div.filter(lambda el: el.has_attribute("highlight")))
```

**Parameters:**
- `condition`: Callable[[HTMLElement], bool]

**Returns:** Iterator[HTMLElement]

#### find_by_attribute(key: str, value: str) → Optional[HTMLElement]
Finds first child with matching attribute.

```python
main = div.find_by_attribute("id", "main")
container = div.find_by_attribute("class_name", "container")
```

**Parameters:**
- `key`: str - Attribute name
- `value`: str - Attribute value to match

**Returns:** HTMLElement or None

#### first() → Optional[HTMLElement]
Returns first child.

```python
first = div.first()
```

**Returns:** HTMLElement or None

#### last() → Optional[HTMLElement]
Returns last child.

```python
last = div.last()
```

**Returns:** HTMLElement or None

#### count_children() → int
Returns number of direct children.

```python
count = div.count_children()
```

**Returns:** int

### Modifying Children

#### replace_child(index: int, new_child: HTMLElement) → self
Replaces child at index with new child.

```python
div.replace_child(0, H1("New Title"))
```

**Parameters:**
- `index`: int - Index of child to replace
- `new_child`: HTMLElement - New child element

**Returns:** self (for chaining)

---

## Attribute Management Methods

### add_attribute(key: str, value: str) → self
Adds or updates single attribute.

```python
div.add_attribute("id", "main")
div.add_attribute("data-value", "123")
```

**Parameters:**
- `key`: str - Attribute name
- `value`: str - Attribute value

**Returns:** self (for chaining)

### add_attributes(attributes: List[Tuple[str, str]]) → self
Adds multiple attributes at once.

```python
div.add_attributes([
    ("id", "main"),
    ("class", "container"),
    ("role", "main")
])
```

**Parameters:**
- `attributes`: List[Tuple[str, str]] - List of (key, value) tuples

**Returns:** self (for chaining)

### remove_attribute(key: str) → self
Removes an attribute.

```python
div.remove_attribute("data-old")
```

**Parameters:**
- `key`: str - Attribute name to remove

**Returns:** self (for chaining)

### get_attribute(key: str) → Optional[str]
Gets attribute value.

```python
id_value = div.get_attribute("id")
class_name = div.get_attribute("class_name")
```

**Parameters:**
- `key`: str - Attribute name

**Returns:** str or None

### has_attribute(key: str) → bool
Checks if attribute exists.

```python
if div.has_attribute("id"):
    print("Has ID")
```

**Parameters:**
- `key`: str - Attribute name

**Returns:** bool

### get_attributes(*keys: str) → Dict[str, str]
Gets multiple attributes or all attributes.

```python
all_attrs = div.get_attributes()
some_attrs = div.get_attributes("id", "class_name")
```

**Parameters:**
- `*keys`: str - Attribute names (if empty, returns all)

**Returns:** Dict[str, str]

### generate_id() → str
Generates unique ID if element doesn't have one.

```python
element_id = div.generate_id()  # Returns existing or generates new
```

**Returns:** str - The element's ID

---

## CSS Style Management Methods

### add_style(key: str, value: str) → self
Adds or updates single inline style.

```python
div.add_style("color", "red")
div.add_style("font-size", "16px")
```

**Parameters:**
- `key`: str - CSS property name (kebab-case or camelCase)
- `value`: str - CSS property value

**Returns:** self (for chaining)

### add_styles(styles: Dict[str, str]) → self
Adds multiple inline styles at once.

```python
div.add_styles({
    "color": "blue",
    "background-color": "#f0f0f0",
    "padding": "20px",
    "margin": "10px"
})
```

**Parameters:**
- `styles`: Dict[str, str] - Dictionary of CSS property: value pairs

**Returns:** self (for chaining)

### get_style(key: str) → Optional[str]
Gets value of specific inline style.

```python
color = div.get_style("color")
padding = div.get_style("padding")
```

**Parameters:**
- `key`: str - CSS property name

**Returns:** str or None

### remove_style(key: str) → self
Removes specific inline style.

```python
div.remove_style("margin")
```

**Parameters:**
- `key`: str - CSS property name to remove

**Returns:** self (for chaining)

---

## Rendering Methods

### render(pretty: bool = False, _indent: int = 0) → str
Renders element to HTML string.

```python
# Compact (default)
html = div.render()
# <div><h1>Title</h1><p>Content</p></div>

# Pretty (indented)
html = div.render(pretty=True)
# <div>
#   <h1>Title</h1>
#   <p>Content</p>
# </div>
```

**Parameters:**
- `pretty`: bool (default: False) - Enable pretty printing with indentation
- `_indent`: int (default: 0) - Internal parameter for indentation level

**Returns:** str - HTML string

**Note:** `_indent` is for internal use. Don't set it manually.

### __str__() → str
String representation (calls render() with pretty=False).

```python
html = str(div)
# Same as: html = div.render()
```

**Returns:** str - Compact HTML string

---

## Serialization Methods

### to_dict() → Dict
Converts element to dictionary representation.

```python
data = div.to_dict()
# {
#     "tag": "div",
#     "self_closing": False,
#     "attributes": {"id": "main"},
#     "text": "",
#     "children": [...]
# }
```

**Returns:** Dict with keys:
- `tag`: str
- `self_closing`: bool
- `attributes`: Dict[str, str]
- `text`: str
- `children`: List[Dict]

### to_json(indent: Optional[int] = None) → str
Converts element to JSON string.

```python
# Compact JSON
json_str = div.to_json()

# Pretty JSON
json_str = div.to_json(indent=2)
```

**Parameters:**
- `indent`: Optional[int] - Number of spaces for indentation (None = compact)

**Returns:** str - JSON string

### from_dict(data: Dict) → HTMLElement (classmethod)
Creates element from dictionary.

```python
data = {
    "tag": "div",
    "self_closing": False,
    "attributes": {"id": "main"},
    "text": "Content",
    "children": []
}
element = HTMLElement.from_dict(data)
```

**Parameters:**
- `data`: Dict - Dictionary with element data

**Returns:** HTMLElement

**Raises:**
- `ValueError` if data is invalid or missing required fields

### from_json(json_str: str) → HTMLElement (classmethod)
Creates element from JSON string.

```python
json_str = '{"tag": "div", "text": "Hello", "children": []}'
element = HTMLElement.from_json(json_str)
```

**Parameters:**
- `json_str`: str - JSON string

**Returns:** HTMLElement

**Raises:**
- `ValueError` if JSON is invalid

### from_html(html_str: str, fragment: bool = False) → Union[HTMLElement, List[HTMLElement]] (classmethod)
Parses HTML string to YDNATL element(s).

```python
# Single element
element = HTMLElement.from_html('<div class="container">Content</div>')

# Multiple root elements (fragment)
elements = HTMLElement.from_html('<h1>Title</h1><p>Text</p>', fragment=True)
```

**Parameters:**
- `html_str`: str - HTML string to parse
- `fragment`: bool (default: False) - If True, returns list of elements

**Returns:**
- If `fragment=False`: HTMLElement or None
- If `fragment=True`: List[HTMLElement]

---

## Parser Function

### from_html(html_str: str, fragment: bool = False) → Union[HTMLElement, List[HTMLElement], None]

**Location:** `ydnatl.core.parser.from_html` or `ydnatl.from_html`

Standalone function for parsing HTML strings.

```python
from ydnatl import from_html

# Parse single element
element = from_html('<div>Content</div>')

# Parse fragment
elements = from_html('<h1>One</h1><p>Two</p>', fragment=True)
```

**Parameters:**
- `html_str`: str - HTML string to parse
- `fragment`: bool (default: False) - If True, returns list of elements

**Returns:**
- If `fragment=False`: HTMLElement or None
- If `fragment=True`: List[HTMLElement]

**Features:**
- Handles all HTML5 elements
- Converts `class` attribute to `class_name`
- Preserves all attributes including data-*
- Handles self-closing tags (br, img, hr, input, etc.)
- Handles HTML entities (&amp;, &lt;, etc.)
- Strips whitespace-only text nodes

---

## Utility Methods

### clone() → HTMLElement
Creates deep copy of element.

```python
original = Div(H1("Title"))
copy = original.clone()
# Modifying copy won't affect original
```

**Returns:** HTMLElement - Deep copy

### __enter__() → self
Enables use as context manager.

```python
with Div(id="container") as div:
    div.append(H1("Title"))
    div.append(Paragraph("Content"))
```

**Returns:** self

### __exit__(exc_type, exc_val, exc_tb) → None
Exits context manager.

**Parameters:** Standard context manager parameters

---

## Event Callbacks

### on_load() → None
Called when element is loaded. Override in subclass.

```python
class MyElement(HTMLElement):
    def on_load(self):
        print("Element loaded")
        # Custom initialization logic
```

### on_before_render() → None
Called before element is rendered. Override in subclass.

```python
class MyElement(HTMLElement):
    def on_before_render(self):
        print("About to render")
        # Pre-render logic
```

### on_after_render() → None
Called after element is rendered. Override in subclass.

```python
class MyElement(HTMLElement):
    def on_after_render(self):
        print("Rendered")
        # Post-render logic
```

### on_unload() → None
Called when element is unloaded. Override in subclass.

```python
class MyElement(HTMLElement):
    def on_unload(self):
        print("Element unloaded")
        # Cleanup logic
```

---

## Fragment Class

**Location:** `ydnatl.core.fragment.Fragment`

Special element that renders only its children without a wrapper tag.

### Constructor

```python
Fragment(*children, **kwargs)
```

**Note:** Any attributes passed are ignored (Fragment doesn't render a tag).

### Usage

```python
from ydnatl import Fragment, H1, Paragraph

# Without Fragment - adds wrapper
content = Div(H1("Title"), Paragraph("Text"))
# Output: <div><h1>Title</h1><p>Text</p></div>

# With Fragment - no wrapper
content = Fragment(H1("Title"), Paragraph("Text"))
# Output: <h1>Title</h1><p>Text</p>
```

### Methods
Inherits all methods from HTMLElement.

**Important:** `render()` outputs only children without wrapper tags.

---

## Tag Classes by Module

All tag classes follow the same constructor pattern as HTMLElement:

```python
TagName(*children, **attributes)
```

### ydnatl.tags.text

**Headings:**
- `H1(*children, **attributes)`
- `H2(*children, **attributes)`
- `H3(*children, **attributes)`
- `H4(*children, **attributes)`
- `H5(*children, **attributes)`
- `H6(*children, **attributes)`

**Text Elements:**
- `Paragraph(*children, **attributes)` - `<p>`
- `Span(*children, **attributes)` - `<span>`
- `Bold(*children, **attributes)` - `<b>`
- `Strong(*children, **attributes)` - `<strong>`
- `Italic(*children, **attributes)` - `<i>`
- `Em(*children, **attributes)` - `<em>`
- `Underline(*children, **attributes)` - `<u>`
- `Strikethrough(*children, **attributes)` - `<s>`
- `Small(*children, **attributes)` - `<small>`
- `Mark(*children, **attributes)` - `<mark>`
- `Del(*children, **attributes)` - `<del>`
- `Ins(*children, **attributes)` - `<ins>`
- `Subscript(*children, **attributes)` - `<sub>`
- `Superscript(*children, **attributes)` - `<sup>`

**Code/Technical:**
- `Code(*children, **attributes)` - `<code>`
- `Pre(*children, **attributes)` - `<pre>`
- `Kbd(*children, **attributes)` - `<kbd>`
- `Samp(*children, **attributes)` - `<samp>`
- `Var(*children, **attributes)` - `<var>`

**Semantic:**
- `Blockquote(*children, **attributes)` - `<blockquote>`
- `Quote(*children, **attributes)` - `<q>`
- `Cite(*children, **attributes)` - `<cite>`
- `Abbr(*children, **attributes)` - `<abbr>`
- `Dfn(*children, **attributes)` - `<dfn>`
- `Time(*children, **attributes)` - `<time>`

**Links & Line Breaks:**
- `Link(*children, **attributes)` - `<a>`
- `Br(**attributes)` - `<br>` (self-closing)
- `Wbr(**attributes)` - `<wbr>` (self-closing)

### ydnatl.tags.layout

- `Div(*children, **attributes)` - `<div>`
- `Section(*children, **attributes)` - `<section>`
- `Article(*children, **attributes)` - `<article>`
- `Aside(*children, **attributes)` - `<aside>`
- `Header(*children, **attributes)` - `<header>`
- `Footer(*children, **attributes)` - `<footer>`
- `Nav(*children, **attributes)` - `<nav>`
- `Main(*children, **attributes)` - `<main>`
- `HorizontalRule(**attributes)` - `<hr>` (self-closing)
- `Details(*children, **attributes)` - `<details>`
- `Summary(*children, **attributes)` - `<summary>`
- `Dialog(*children, **attributes)` - `<dialog>`

### ydnatl.tags.form

- `Form(*children, **attributes)` - `<form>`
- `Input(**attributes)` - `<input>` (self-closing)
- `Textarea(*children, **attributes)` - `<textarea>`
- `Button(*children, **attributes)` - `<button>`
- `Label(*children, **attributes)` - `<label>`
- `Select(*children, **attributes)` - `<select>`
- `Option(*children, **attributes)` - `<option>`
- `Optgroup(*children, **attributes)` - `<optgroup>`
- `Fieldset(*children, **attributes)` - `<fieldset>`
- `Legend(*children, **attributes)` - `<legend>`
- `Output(*children, **attributes)` - `<output>`
- `Progress(*children, **attributes)` - `<progress>`
- `Meter(*children, **attributes)` - `<meter>`

### ydnatl.tags.lists

- `UnorderedList(*children, **attributes)` - `<ul>`
- `OrderedList(*children, **attributes)` - `<ol>`
- `ListItem(*children, **attributes)` - `<li>`
- `Datalist(*children, **attributes)` - `<datalist>`
- `DescriptionList(*children, **attributes)` - `<dl>`
- `DescriptionTerm(*children, **attributes)` - `<dt>`
- `DescriptionDetails(*children, **attributes)` - `<dd>`

### ydnatl.tags.table

- `Table(*children, **attributes)` - `<table>`
- `TableHeader(*children, **attributes)` - `<thead>`
- `TableBody(*children, **attributes)` - `<tbody>`
- `TableFooter(*children, **attributes)` - `<tfoot>`
- `TableRow(*children, **attributes)` - `<tr>`
- `TableHeaderCell(*children, **attributes)` - `<th>`
- `TableDataCell(*children, **attributes)` - `<td>`
- `Caption(*children, **attributes)` - `<caption>`
- `Colgroup(*children, **attributes)` - `<colgroup>`
- `Col(**attributes)` - `<col>` (self-closing)

**Special Table Methods:**

#### Table.from_json(file_path: str, **table_attrs)
Creates table from JSON file.

```python
table = Table.from_json("data.json", class_name="data-table")
```

**JSON Format:**
```json
{
  "headers": ["Name", "Age", "City"],
  "rows": [
    ["Alice", "30", "NYC"],
    ["Bob", "25", "LA"]
  ]
}
```

#### Table.from_csv(file_path: str, **table_attrs)
Creates table from CSV file.

```python
table = Table.from_csv("data.csv", class_name="data-table")
```

### ydnatl.tags.media

- `Image(**attributes)` - `<img>` (self-closing)
- `Video(*children, **attributes)` - `<video>`
- `Audio(*children, **attributes)` - `<audio>`
- `Source(**attributes)` - `<source>` (self-closing)
- `Track(**attributes)` - `<track>` (self-closing)
- `Picture(*children, **attributes)` - `<picture>`
- `Figure(*children, **attributes)` - `<figure>`
- `Figcaption(*children, **attributes)` - `<figcaption>`
- `Canvas(*children, **attributes)` - `<canvas>`
- `Embed(**attributes)` - `<embed>` (self-closing)
- `Object(*children, **attributes)` - `<object>`
- `Param(**attributes)` - `<param>` (self-closing)
- `Map(*children, **attributes)` - `<map>`
- `Area(**attributes)` - `<area>` (self-closing)

### ydnatl.tags.html

- `HTML(*children, **attributes)` - `<html>` (includes DOCTYPE)
- `Head(*children, **attributes)` - `<head>`
- `Body(*children, **attributes)` - `<body>`
- `Title(*children, **attributes)` - `<title>`
- `Meta(**attributes)` - `<meta>` (self-closing)
- `Link(**attributes)` - `<link>` (self-closing)
- `HtmlLink(**attributes)` - Alias for Link (avoid conflicts)
- `Script(*children, **attributes)` - `<script>`
- `Style(*children, **attributes)` - `<style>`
- `Base(**attributes)` - `<base>` (self-closing)
- `Noscript(*children, **attributes)` - `<noscript>`
- `IFrame(*children, **attributes)` - `<iframe>`

**Note:** `HTML` element automatically includes `<!DOCTYPE html>` in render output.

---

## Styling System (ydnatl.styles)

**Location:** `ydnatl.styles`

YDNATL includes a comprehensive styling system for managing external stylesheets, themes, and reusable component styles. This complements the existing inline style methods and is perfect for larger applications.

### Key Features

- **External Stylesheets**: Extract styles to `<style>` tags instead of inline
- **BEM Support**: Built-in BEM naming convention (Block__Element--Modifier)
- **Theming**: Pre-built themes (Modern, Classic, Minimal) with CSS variables
- **Responsive**: Automatic media query generation with breakpoints
- **Pseudo-selectors**: Support for :hover, :active, :focus, etc.
- **JSON Serialization**: Save/load styles for website builders
- **Compatible**: Works seamlessly with existing inline styles

### Import Patterns

```python
# Import styling classes
from ydnatl.styles import CSSStyle, StyleSheet, Theme

# Or from main module
from ydnatl import CSSStyle, StyleSheet, Theme
```

---

## CSSStyle Class

**Location:** `ydnatl.styles.CSSStyle`

Represents CSS styles with support for pseudo-selectors and responsive breakpoints.

### Constructor

```python
CSSStyle(**kwargs)
```

**Parameters:**
- `**kwargs`: CSS properties as keyword arguments
  - Use snake_case (converted to kebab-case automatically)
  - Prefix with `_` for pseudo-selectors: `_hover`, `_active`, `_focus`
  - Prefix with `_` for breakpoints: `_sm`, `_md`, `_lg`, `_xl`

**Example:**
```python
style = CSSStyle(
    background_color="#007bff",
    color="white",
    padding="10px 20px",
    border_radius="5px",
    _hover=CSSStyle(background_color="#0056b3"),
    _md=CSSStyle(padding="15px 30px")
)
```

### Properties

| Property       | Type                      | Description                |
|----------------|---------------------------|----------------------------|
| `_styles`      | Dict[str, str]            | Base CSS properties        |
| `_pseudo`      | Dict[str, CSSStyle]       | Pseudo-selector styles     |
| `_breakpoints` | Dict[str, CSSStyle]       | Responsive breakpoint styles |

### Methods

#### to_inline() → str
Generates inline style string (for `style="..."` attribute).

```python
style = CSSStyle(color="blue", padding="10px")
inline = style.to_inline()
# Returns: "color: blue; padding: 10px"
```

**Returns:** str - CSS string for inline styles

**Note:** Only includes base styles, not pseudo-selectors or breakpoints.

#### merge(other: CSSStyle) → CSSStyle
Merges another CSSStyle, returning new CSSStyle. Other style overrides this one.

```python
base = CSSStyle(color="blue", padding="10px")
override = CSSStyle(color="red", margin="5px")
merged = base.merge(override)
# Result: color="red", padding="10px", margin="5px"
```

**Parameters:**
- `other`: CSSStyle - Style to merge

**Returns:** CSSStyle - New merged style object

#### has_pseudo_or_breakpoints() → bool
Checks if style has pseudo-selectors or breakpoints.

```python
style = CSSStyle(color="blue", _hover=CSSStyle(color="red"))
has_special = style.has_pseudo_or_breakpoints()  # True
```

**Returns:** bool

#### is_complex(threshold: int = 3) → bool
Checks if style is complex (has many properties).

```python
simple = CSSStyle(color="blue")
simple.is_complex()  # False

complex_style = CSSStyle(color="blue", padding="10px", margin="5px", border="1px solid")
complex_style.is_complex()  # True
```

**Parameters:**
- `threshold`: int (default: 3) - Number of properties considered complex

**Returns:** bool

#### to_dict() → Dict[str, Any]
Serializes to JSON-compatible dictionary.

```python
style = CSSStyle(color="blue", _hover=CSSStyle(color="red"))
data = style.to_dict()
# Returns: {"styles": {"color": "blue"}, "pseudo": {"hover": {...}}, "breakpoints": {}}
```

**Returns:** Dict with keys:
- `styles`: Dict[str, str]
- `pseudo`: Dict[str, Dict] (if present)
- `breakpoints`: Dict[str, Dict] (if present)

#### from_dict(data: Dict[str, Any]) → CSSStyle (classmethod)
Deserializes from dictionary.

```python
data = {"styles": {"color": "blue"}, "pseudo": {}, "breakpoints": {}}
style = CSSStyle.from_dict(data)
```

**Parameters:**
- `data`: Dict - Dictionary from to_dict()

**Returns:** CSSStyle

### Pseudo-selectors

Supported pseudo-selectors (prefix with `_`):
- `_hover` → `:hover`
- `_active` → `:active`
- `_focus` → `:focus`
- `_visited` → `:visited`
- `_link` → `:link`
- `_first_child` → `:first-child`
- `_last_child` → `:last-child`

### Breakpoints

Supported breakpoints (prefix with `_`):
- `_xs` → 0px (default)
- `_sm` → 640px
- `_md` → 768px
- `_lg` → 1024px
- `_xl` → 1280px
- `_2xl` → 1536px

---

## StyleSheet Class

**Location:** `ydnatl.styles.StyleSheet`

Manages CSS classes and generates `<style>` tag content.

### Constructor

```python
StyleSheet(theme: Optional[Theme] = None)
```

**Parameters:**
- `theme`: Optional[Theme] - Theme to include CSS variables

**Example:**
```python
# Without theme
stylesheet = StyleSheet()

# With theme
theme = Theme.modern()
stylesheet = StyleSheet(theme=theme)
```

### Methods

#### register(name: Optional[str] = None, style: Optional[CSSStyle] = None) → str
Registers a style as a CSS class.

```python
stylesheet = StyleSheet()
btn_class = stylesheet.register("btn-primary", CSSStyle(
    background_color="#007bff",
    color="white"
))
# Returns: "btn-primary"
```

**Parameters:**
- `name`: Optional[str] - Class name (auto-generated if None)
- `style`: Optional[CSSStyle] - Style to register

**Returns:** str - Class name (for use in `class_name` attribute)

#### register_bem(block: str, element: Optional[str] = None, modifier: Optional[str] = None, style: Optional[CSSStyle] = None) → str
Registers a style using BEM naming convention.

```python
# Block
card = stylesheet.register_bem("card", style=CSSStyle(padding="20px"))
# Returns: "card"

# Block + Element
header = stylesheet.register_bem("card", element="header", style=CSSStyle(font_weight="bold"))
# Returns: "card__header"

# Block + Modifier
featured = stylesheet.register_bem("card", modifier="featured", style=CSSStyle(border="2px solid blue"))
# Returns: "card--featured"

# Block + Element + Modifier
icon = stylesheet.register_bem("card", element="icon", modifier="large", style=CSSStyle(font_size="24px"))
# Returns: "card__icon--large"
```

**Parameters:**
- `block`: str - Block name
- `element`: Optional[str] - Element name
- `modifier`: Optional[str] - Modifier name
- `style`: Optional[CSSStyle] - Style to register

**Returns:** str - BEM class name

#### get_style(name: str) → Optional[CSSStyle]
Gets a registered style by class name.

```python
style = stylesheet.get_style("btn-primary")
```

**Parameters:**
- `name`: str - Class name

**Returns:** CSSStyle or None

#### has_class(name: str) → bool
Checks if a class is registered.

```python
if stylesheet.has_class("btn-primary"):
    print("Class exists")
```

**Parameters:**
- `name`: str - Class name

**Returns:** bool

#### unregister(name: str) → bool
Removes a registered class.

```python
success = stylesheet.unregister("old-class")
```

**Parameters:**
- `name`: str - Class name to remove

**Returns:** bool - True if removed, False if not found

#### clear() → None
Removes all registered classes.

```python
stylesheet.clear()
```

#### set_breakpoint(name: str, value: str) → None
Sets or updates a breakpoint value.

```python
stylesheet.set_breakpoint("xl", "1440px")
```

**Parameters:**
- `name`: str - Breakpoint name (e.g., "sm", "md")
- `value`: str - CSS value (e.g., "640px")

#### render(pretty: bool = True) → str
Generates CSS output for all registered classes.

```python
css = stylesheet.render()
# Returns full CSS string with classes, pseudo-selectors, and media queries
```

**Parameters:**
- `pretty`: bool (default: True) - Format with newlines and indentation

**Returns:** str - CSS string

#### to_style_tag(pretty: bool = True) → str
Generates a complete `<style>` tag with all CSS.

```python
tag = stylesheet.to_style_tag()
# Returns: "<style>\n.btn-primary { ... }\n</style>"
```

**Parameters:**
- `pretty`: bool (default: True) - Format with newlines

**Returns:** str - HTML `<style>` tag with CSS

#### count_classes() → int
Gets the number of registered classes.

```python
count = stylesheet.count_classes()
```

**Returns:** int

#### get_all_class_names() → List[str]
Gets a list of all registered class names.

```python
names = stylesheet.get_all_class_names()
# Returns: ["btn-primary", "card", "card__header", ...]
```

**Returns:** List[str]

#### to_dict() → Dict
Serializes stylesheet to dictionary.

```python
data = stylesheet.to_dict()
# Returns: {"classes": {...}, "breakpoints": {...}}
```

**Returns:** Dict with keys:
- `classes`: Dict[str, Dict]
- `breakpoints`: Dict[str, str]

#### from_dict(data: Dict, theme: Optional[Theme] = None) → StyleSheet (classmethod)
Deserializes stylesheet from dictionary.

```python
stylesheet = StyleSheet.from_dict(data, theme=Theme.modern())
```

**Parameters:**
- `data`: Dict - Dictionary from to_dict()
- `theme`: Optional[Theme] - Theme to include

**Returns:** StyleSheet

---

## Theme Class

**Location:** `ydnatl.styles.Theme`

Represents a design theme with colors, typography, spacing, and component styles.

### Constructor

```python
Theme(
    name: str = "Default",
    colors: Optional[Dict[str, str]] = None,
    typography: Optional[Dict[str, Any]] = None,
    spacing: Optional[Dict[str, str]] = None,
    components: Optional[Dict[str, Any]] = None
)
```

**Parameters:**
- `name`: str - Theme name
- `colors`: Optional[Dict[str, str]] - Color palette
- `typography`: Optional[Dict[str, Any]] - Font settings
- `spacing`: Optional[Dict[str, str]] - Spacing scale
- `components`: Optional[Dict[str, Any]] - Pre-styled components

**Example:**
```python
theme = Theme(
    name="Custom",
    colors={
        "primary": "#007bff",
        "secondary": "#6c757d"
    },
    spacing={
        "sm": "8px",
        "md": "16px",
        "lg": "24px"
    }
)
```

### Preset Themes (Class Methods)

#### Theme.modern() → Theme
Modern theme with clean, contemporary design.

```python
theme = Theme.modern()
```

**Returns:** Theme with:
- Colors: Blue primary (#3b82f6), purple secondary
- Typography: Inter, system fonts
- Components: Modern buttons, cards

#### Theme.classic() → Theme
Classic theme with traditional, timeless design.

```python
theme = Theme.classic()
```

**Returns:** Theme with:
- Colors: Traditional blue (#0066cc)
- Typography: Georgia, serif fonts
- Components: Classic buttons with borders

#### Theme.minimal() → Theme
Minimal theme with clean, stripped-down design.

```python
theme = Theme.minimal()
```

**Returns:** Theme with:
- Colors: Black and white (#000000, #ffffff)
- Typography: System fonts
- Components: Minimal, flat buttons

### Methods

#### get_css_variables() → Dict[str, str]
Generates CSS variables from theme properties.

```python
theme = Theme(colors={"primary": "#007bff"}, spacing={"md": "16px"})
variables = theme.get_css_variables()
# Returns: {"--color-primary": "#007bff", "--spacing-md": "16px"}
```

**Returns:** Dict[str, str] - CSS variable names and values

#### get_component_style(component: str, variant: str = "default") → Optional[CSSStyle]
Gets a component style from the theme.

```python
theme = Theme.modern()
btn_style = theme.get_component_style("button", "primary")
```

**Parameters:**
- `component`: str - Component name (e.g., "button", "card")
- `variant`: str (default: "default") - Variant name (e.g., "primary", "secondary")

**Returns:** CSSStyle or None

#### to_dict() → Dict[str, Any]
Serializes theme to dictionary.

```python
data = theme.to_dict()
```

**Returns:** Dict with keys:
- `name`: str
- `colors`: Dict[str, str]
- `typography`: Dict[str, Any]
- `spacing`: Dict[str, str]
- `components`: Dict[str, Any]

#### from_dict(data: Dict[str, Any]) → Theme (classmethod)
Deserializes theme from dictionary.

```python
theme = Theme.from_dict(data)
```

**Parameters:**
- `data`: Dict - Dictionary from to_dict()

**Returns:** Theme

---

## Styling Patterns

### Pattern 1: Basic StyleSheet Usage

```python
from ydnatl import HTML, Head, Body, Button, Style
from ydnatl.styles import CSSStyle, StyleSheet

# Create stylesheet
stylesheet = StyleSheet()

# Register button styles
btn_primary = stylesheet.register("btn-primary", CSSStyle(
    background_color="#007bff",
    color="white",
    padding="10px 20px",
    border_radius="5px",
    border="none",
    cursor="pointer",
    _hover=CSSStyle(background_color="#0056b3")
))

# Use in HTML
page = HTML(
    Head(Style(stylesheet.render())),
    Body(
        Button("Click Me", class_name=btn_primary),
        Button("Another Button", class_name=btn_primary)
    )
)
```

### Pattern 2: Using Themes

```python
from ydnatl import HTML, Head, Body, Div, Button, Style
from ydnatl.styles import Theme, StyleSheet, CSSStyle

# Use preset theme
theme = Theme.modern()
stylesheet = StyleSheet(theme=theme)

# Register styles using theme variables
btn = stylesheet.register("btn", CSSStyle(
    background_color="var(--color-primary)",
    color="var(--color-white)",
    padding="var(--spacing-md)",
    border_radius="6px",
    _hover=CSSStyle(background_color="var(--color-primary-dark)")
))

card = stylesheet.register("card", CSSStyle(
    background_color="var(--color-white)",
    padding="var(--spacing-lg)",
    border_radius="8px"
))

# Use in HTML
page = HTML(
    Head(Style(stylesheet.render())),
    Body(
        Div(
            Button("Themed Button", class_name=btn),
            class_name=card
        )
    )
)
```

### Pattern 3: BEM Naming

```python
from ydnatl import Div
from ydnatl.styles import StyleSheet, CSSStyle

stylesheet = StyleSheet()

# Register BEM classes
card = stylesheet.register_bem("card", style=CSSStyle(
    background="white",
    padding="20px"
))

card_header = stylesheet.register_bem("card", element="header", style=CSSStyle(
    font_weight="bold",
    border_bottom="1px solid #ccc"
))

card_body = stylesheet.register_bem("card", element="body", style=CSSStyle(
    padding="15px"
))

card_featured = stylesheet.register_bem("card", modifier="featured", style=CSSStyle(
    border="2px solid blue"
))

# Use in HTML
html = Div(
    Div("Card Header", class_name=card_header),
    Div("Card Body", class_name=card_body),
    class_name=f"{card} {card_featured}"
)
```

### Pattern 4: Responsive Styles

```python
from ydnatl.styles import StyleSheet, CSSStyle

stylesheet = StyleSheet()

# Register responsive container
container = stylesheet.register("container", CSSStyle(
    padding="10px",
    margin="0 auto",
    _sm=CSSStyle(padding="15px", max_width="640px"),
    _md=CSSStyle(padding="20px", max_width="768px"),
    _lg=CSSStyle(padding="30px", max_width="1024px")
))

# Generates:
# .container { padding: 10px; margin: 0 auto; }
# @media (min-width: 640px) { .container { padding: 15px; max-width: 640px; } }
# @media (min-width: 768px) { .container { padding: 20px; max-width: 768px; } }
# @media (min-width: 1024px) { .container { padding: 30px; max-width: 1024px; } }
```

### Pattern 5: Combining with Inline Styles

```python
from ydnatl import Button
from ydnatl.styles import StyleSheet, CSSStyle

stylesheet = StyleSheet()

# Register base button style
btn = stylesheet.register("btn", CSSStyle(
    padding="10px 20px",
    border_radius="5px",
    border="none"
))

# Use base class + inline overrides
button1 = Button("Blue Button", class_name=btn).add_styles({
    "background-color": "#007bff",
    "color": "white"
})

button2 = Button("Green Button", class_name=btn).add_styles({
    "background-color": "#28a745",
    "color": "white"
})

# Both buttons share base styles but have different colors
```

### Pattern 6: Serialization for Website Builders

```python
from ydnatl.styles import StyleSheet, CSSStyle
import json

# Create and populate stylesheet
stylesheet = StyleSheet()
stylesheet.register("btn", CSSStyle(color="blue", padding="10px"))
stylesheet.register("card", CSSStyle(background="white", padding="20px"))

# Save to JSON
data = stylesheet.to_dict()
json_str = json.dumps(data, indent=2)
# Store in database, file, etc.

# Later... load from JSON
loaded_data = json.loads(json_str)
restored_stylesheet = StyleSheet.from_dict(loaded_data)

# Use restored stylesheet
css = restored_stylesheet.render()
```

### Pattern 7: Custom Component with Styles

```python
from ydnatl import HTMLElement, Div, H2, Paragraph
from ydnatl.styles import StyleSheet, CSSStyle

class StyledCard(HTMLElement):
    def __init__(self, title, content, stylesheet, **kwargs):
        super().__init__(tag="div", **kwargs)

        # Register card styles if not already registered
        if not stylesheet.has_class("card"):
            card_style = CSSStyle(
                background="white",
                padding="20px",
                border_radius="8px",
                box_shadow="0 2px 4px rgba(0,0,0,0.1)"
            )
            self.card_class = stylesheet.register("card", card_style)
        else:
            self.card_class = "card"

        # Set class and append children
        self.add_attribute("class_name", self.card_class)
        self.append(
            H2(title, class_name="card-title"),
            Paragraph(content, class_name="card-content")
        )

# Usage
stylesheet = StyleSheet()
card1 = StyledCard("Title 1", "Content 1", stylesheet)
card2 = StyledCard("Title 2", "Content 2", stylesheet)
```

---

## Common Patterns

### Pattern 1: Building a Complete Page

```python
from ydnatl import HTML, Head, Body, Title, Meta, Div, H1, Paragraph

page = HTML(
    Head(
        Title("My Page"),
        Meta(charset="utf-8"),
        Meta(name="viewport", content="width=device-width, initial-scale=1")
    ),
    Body(
        Div(
            H1("Welcome"),
            Paragraph("This is my page."),
            class_name="container"
        )
    )
)

html_string = page.render(pretty=True)
```

### Pattern 2: Dynamic Content with Conditionals

```python
from ydnatl import Div, H1, Paragraph

def create_section(title, content, show_header=True):
    section = Div(class_name="section")

    if show_header:
        section.append(H1(title))

    section.append(Paragraph(content))

    return section

# Usage
section = create_section("About", "Some content", show_header=True)
```

### Pattern 3: Lists with Iteration

```python
from ydnatl import UnorderedList, ListItem

items = ["Apple", "Banana", "Orange"]

ul = UnorderedList()
for item in items:
    ul.append(ListItem(item))

# Or using Fragment
from ydnatl import Fragment

fragment = Fragment()
for item in items:
    fragment.append(ListItem(item))

ul = UnorderedList(fragment)
```

### Pattern 4: Method Chaining

```python
from ydnatl import Div, H1, Paragraph

container = (Div()
    .add_attribute("id", "main")
    .add_attribute("class_name", "container")
    .add_style("padding", "20px")
    .add_style("margin", "0 auto")
    .append(H1("Title"))
    .append(Paragraph("Content"))
)
```

### Pattern 5: Context Managers

```python
from ydnatl import Div, Section, H1, Paragraph

with Div(id="container") as container:
    with Section(class_name="content") as section:
        section.append(H1("Title"))
        section.append(Paragraph("Content"))

    container.append(section)

html = container.render()
```

### Pattern 6: Forms

```python
from ydnatl import Form, Label, Input, Button

form = Form(action="/submit", method="post")
form.append(
    Label("Name:", for_="name"),
    Input(type="text", id="name", name="name", required=True),
    Button("Submit", type="submit")
)
```

### Pattern 7: Tables from Data

```python
from ydnatl import Table, TableHeader, TableBody, TableRow
from ydnatl import TableHeaderCell, TableDataCell

data = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25}
]

table = Table()

# Header
thead = TableHeader()
header_row = TableRow()
header_row.append(TableHeaderCell("Name"), TableHeaderCell("Age"))
thead.append(header_row)
table.append(thead)

# Body
tbody = TableBody()
for row in data:
    tr = TableRow()
    tr.append(TableDataCell(row["name"]), TableDataCell(str(row["age"])))
    tbody.append(tr)
table.append(tbody)
```

### Pattern 8: Parsing and Modifying HTML

```python
from ydnatl import from_html

# Parse existing HTML
html_str = '<div class="old"><h1>Title</h1></div>'
element = from_html(html_str)

# Modify it
element.add_attribute("class_name", "new")
element.add_style("padding", "20px")
element.append(Paragraph("New content"))

# Render modified version
new_html = element.render()
```

### Pattern 9: Serialization for Storage

```python
from ydnatl import Div, H1, Paragraph, HTMLElement

# Create element tree
page = Div(
    H1("Title"),
    Paragraph("Content"),
    id="page"
)

# Save to JSON
json_str = page.to_json(indent=2)
# Store in database, file, etc.

# Later... load from JSON
loaded_page = HTMLElement.from_json(json_str)

# Use it
html = loaded_page.render()
```

### Pattern 10: Custom Components

```python
from ydnatl import HTMLElement, Div, H2, Paragraph

class Card(HTMLElement):
    def __init__(self, title, content, **kwargs):
        super().__init__(
            tag="div",
            class_name="card",
            **kwargs
        )

        self.append(
            H2(title, class_name="card-title"),
            Paragraph(content, class_name="card-content")
        )

    def on_before_render(self):
        # Add shadow class if shadow attribute present
        if self.has_attribute("shadow"):
            current_class = self.get_attribute("class_name") or ""
            self.add_attribute("class_name", f"{current_class} shadow")

# Usage
card = Card("My Card", "Card content", shadow="true")
html = card.render()
```

---

## Type Hints Reference

When generating code with type hints:

```python
from typing import Optional, List, Dict, Union, Callable, Iterator, Tuple, Any

# Constructor
def __init__(
    self,
    *children: Union['HTMLElement', str],
    tag: str = "div",
    text: str = "",
    self_closing: bool = False,
    **attributes: str
) -> None: ...

# Element manipulation
def append(self, *children: Union['HTMLElement', str]) -> 'HTMLElement': ...
def prepend(self, *children: Union['HTMLElement', str]) -> 'HTMLElement': ...
def clear(self) -> 'HTMLElement': ...
def pop(self, index: int = -1) -> 'HTMLElement': ...
def remove_all(self, condition: Callable[['HTMLElement'], bool]) -> 'HTMLElement': ...

# Querying
def filter(self, condition: Callable[['HTMLElement'], bool]) -> Iterator['HTMLElement']: ...
def find_by_attribute(self, key: str, value: str) -> Optional['HTMLElement']: ...
def first(self) -> Optional['HTMLElement']: ...
def last(self) -> Optional['HTMLElement']: ...
def count_children(self) -> int: ...

# Attributes
def add_attribute(self, key: str, value: str) -> 'HTMLElement': ...
def add_attributes(self, attributes: List[Tuple[str, str]]) -> 'HTMLElement': ...
def remove_attribute(self, key: str) -> 'HTMLElement': ...
def get_attribute(self, key: str) -> Optional[str]: ...
def has_attribute(self, key: str) -> bool: ...
def get_attributes(self, *keys: str) -> Dict[str, str]: ...

# Styles
def add_style(self, key: str, value: str) -> 'HTMLElement': ...
def add_styles(self, styles: Dict[str, str]) -> 'HTMLElement': ...
def get_style(self, key: str) -> Optional[str]: ...
def remove_style(self, key: str) -> 'HTMLElement': ...

# Rendering
def render(self, pretty: bool = False, _indent: int = 0) -> str: ...
def __str__(self) -> str: ...

# Serialization
def to_dict(self) -> Dict[str, Any]: ...
def to_json(self, indent: Optional[int] = None) -> str: ...

@classmethod
def from_dict(cls, data: Dict[str, Any]) -> 'HTMLElement': ...

@classmethod
def from_json(cls, json_str: str) -> 'HTMLElement': ...

@classmethod
def from_html(cls, html_str: str, fragment: bool = False) -> Union['HTMLElement', List['HTMLElement'], None]: ...

# Utility
def clone(self) -> 'HTMLElement': ...
def replace_child(self, index: int, new_child: 'HTMLElement') -> 'HTMLElement': ...
def generate_id(self) -> str: ...

# Context manager
def __enter__(self) -> 'HTMLElement': ...
def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...
```

---

## Error Handling

### Common Errors and Solutions

**ValueError: Invalid JSON**
```python
try:
    element = HTMLElement.from_json(json_str)
except ValueError as e:
    print(f"Invalid JSON: {e}")
```

**ValueError: Missing required field in dict**
```python
try:
    element = HTMLElement.from_dict(data)
except ValueError as e:
    print(f"Invalid data: {e}")
```

**IndexError: pop from empty list**
```python
if div.count_children() > 0:
    child = div.pop()
else:
    print("No children to pop")
```

**KeyError: Attribute not found**
```python
# Don't do this:
value = div.attributes["missing"]  # KeyError

# Do this instead:
value = div.get_attribute("missing")  # Returns None
if value is None:
    print("Attribute not found")
```

---

## Performance Considerations

### Best Practices

1. **Use method chaining for multiple operations**
   ```python
   # Good
   div.add_attribute("id", "main").add_style("padding", "20px").append(child)

   # Less efficient (but still fine)
   div.add_attribute("id", "main")
   div.add_style("padding", "20px")
   div.append(child)
   ```

2. **Batch add children**
   ```python
   # Good
   div.append(child1, child2, child3)

   # Less efficient
   div.append(child1)
   div.append(child2)
   div.append(child3)
   ```

3. **Use compact rendering for production**
   ```python
   # Production (smaller output)
   html = element.render()

   # Development only (larger output)
   html = element.render(pretty=True)
   ```

4. **Reuse elements via cloning**
   ```python
   template = Div(H1("Title"), class_name="card")
   card1 = template.clone()
   card2 = template.clone()
   ```

---

## Security Considerations

### HTML Escaping

YDNATL automatically escapes HTML entities in:
- Text content
- Attribute values

```python
# Safe - automatically escaped
div = Div("<script>alert('xss')</script>")
# Renders as: <div>&lt;script&gt;alert('xss')&lt;/script&gt;</div>

# Safe - attribute values escaped
div = Div(data_value='<script>alert("xss")</script>')
# Renders as: <div data-value="&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;"></div>
```

### No Raw HTML Injection

YDNATL does not support raw HTML injection. All content is escaped. This prevents XSS attacks.

---

## Complete Example: Blog Post Page

```python
from ydnatl import (
    HTML, Head, Body, Title, Meta, HtmlLink,
    Div, Section, Article, Header, Footer, Nav,
    H1, H2, Paragraph, Link, UnorderedList, ListItem
)

def create_blog_post(title, author, date, content):
    return Article(
        Header(
            H1(title, class_name="post-title"),
            Paragraph(
                f"By {author} on {date}",
                class_name="post-meta"
            )
        ),
        Paragraph(content, class_name="post-content"),
        class_name="blog-post"
    )

def create_page(posts):
    page = HTML(
        Head(
            Title("My Blog"),
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            HtmlLink(rel="stylesheet", href="/style.css")
        ),
        Body(
            Header(
                H1("My Blog", class_name="site-title"),
                Nav(
                    UnorderedList(
                        ListItem(Link("Home", href="/")),
                        ListItem(Link("About", href="/about")),
                        ListItem(Link("Contact", href="/contact"))
                    )
                )
            ),
            Section(
                *[create_blog_post(
                    post["title"],
                    post["author"],
                    post["date"],
                    post["content"]
                ) for post in posts],
                class_name="posts"
            ),
            Footer(
                Paragraph("© 2024 My Blog. All rights reserved.")
            )
        )
    )

    return page.render(pretty=True)

# Usage
posts = [
    {
        "title": "First Post",
        "author": "Alice",
        "date": "2024-01-01",
        "content": "This is my first blog post!"
    },
    {
        "title": "Second Post",
        "author": "Bob",
        "date": "2024-01-02",
        "content": "Another interesting post."
    }
]

html = create_page(posts)
print(html)
```

---

## Quick Reference Cheat Sheet

### Creating Elements
```python
# Basic element
div = Div("text content")

# With attributes
div = Div("text", id="main", class_name="container")

# Nested
div = Div(
    H1("Title"),
    Paragraph("Content")
)
```

### Modifying Elements
```python
div.append(Paragraph("New"))           # Add child
div.prepend(H1("First"))               # Add at start
div.add_attribute("id", "main")        # Add attribute
div.add_style("color", "red")          # Add style
div.clear()                            # Remove all children
```

### Querying Elements
```python
count = div.count_children()           # Count children
first = div.first()                    # Get first child
elem = div.find_by_attribute("id", "x") # Find by attribute
filtered = list(div.filter(lambda e: e.tag == "p"))
```

### Rendering
```python
html = div.render()                    # Compact HTML
html = div.render(pretty=True)         # Pretty HTML
html = str(div)                        # Same as render()
```

### Serialization
```python
json_str = div.to_json(indent=2)       # To JSON
dict_data = div.to_dict()              # To dict
elem = HTMLElement.from_json(json_str) # From JSON
elem = HTMLElement.from_dict(dict_data) # From dict
elem = from_html("<div>...</div>")     # From HTML
```

### Common Tags
```python
# Text
H1("Heading"), Paragraph("Text"), Span("Inline")

# Layout
Div(), Section(), Article(), Header(), Footer()

# Forms
Form(), Input(type="text"), Button("Click"), Label("Name:")

# Lists
UnorderedList(), OrderedList(), ListItem("Item")

# Tables
Table(), TableRow(), TableDataCell("Data")

# Media
Image(src="pic.jpg"), Video(src="vid.mp4")
```

---

## End of LLM Guide

This guide provides complete technical specifications for the YDNATL library. When generating code:

1. Use the exact method signatures provided
2. Follow the patterns demonstrated
3. Remember that all modification methods return `self` for chaining
4. HTML escaping is automatic - don't manually escape
5. Use `from_html()` for parsing existing HTML
6. Use `to_json()` / `from_json()` for persistence
7. Use `Fragment` when you need multiple elements without wrapper
8. All tag classes work the same way: `TagName(*children, **attributes)`

For any edge cases not covered, refer to the core `HTMLElement` class - all tags inherit from it and work identically.