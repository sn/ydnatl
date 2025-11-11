# YDNATL

YDNATL (**Y**ou **D**on't **N**eed **A**nother **T**emplate **L**anguage) is a Python library that lets you build HTML using simple Python classes. It's great for apps that need HTML generation while skipping the hassle of writing it by hand or using a templating engine.

- ✓ Declarative syntax for building HTML documents (like Flutter)
- ✓ Easy to read and write
- ✓ Supports all HTML5 elements
- ✓ JSON serialization/deserialization for saving and loading UI structures
- ✓ Pretty printing with indentation for readable HTML
- ✓ CSS style helpers for easy inline styling
- ✓ External stylesheet system with theming and BEM support
- ✓ Method chaining for fluent interfaces
- ✓ Context manager support for clean nesting
- ✓ Fragment support for wrapper-free grouping
- ✓ HTML parsing to convert raw HTML strings into YDNATL elements
- ✓ Lightweight
- ✓ Extremely fast
- ✓ Fully customisable
- ✓ Compose HTML efficiently
- ✓ Lean & clean Python with no dependencies
- ✓ LLM Compatible

## Requirements

Python `3.8` or higher is required.

## Installation

```bash
pip install ydnatl
```

## Usage

```python
from ydnatl import *

# Create a simple HTML document
page = HTML(
    Head(
        Title("My Page")
    ),
    Body(
        Div(
            H1("Hello, World!"),
            Paragraph("This is a test document.")
        )
    )
)

print(page.render())
```

This code will produce:

```html
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <title>My Page</title>
  </head>
  <body>
    <div>
      <h1>Hello, World!</h1>
      <p>This is a test document.</p>
    </div>
  </body>
</html>
```

### Dynamic Composition 

```python
from ydnatl import *

# Dynamic content based on conditions
day_of_week = "Monday"  # Example variable

html = HTML()
header = Head()
body = Body()

body.append(
    Div(
        H1("My Headline"),
        Paragraph("Basic paragraph element"),
    )
)

if day_of_week == "Monday": 
    header.append(Title("Unfortunately, it's Monday!"))
else:
    header.append(Title("Great! It's no longer Monday!"))

html.append(header)
html.append(body)

print(html.render())
```

All element classes are subclasses of HTMLElement. The parent class provides all of the inherited functionality to generate the individual tags. Keyword arguments passed to element constructors will be converted to attributes on the HTML elements being generated.

### Working with Attributes

```python
from ydnatl import *

# Add attributes via constructor
div = Div(id="my-div", class_name="container", data_value="123")

# Add attributes after creation
div.add_attribute("role", "main")
div.add_attributes([("aria-label", "Main content"), ("tabindex", "0")])

# HTML output: <div id="my-div" class="container" data-value="123" role="main" aria-label="Main content" tabindex="0"></div>
```

### Pretty Printing

YDNATL supports pretty printing with automatic indentation for readable HTML output:

```python
from ydnatl import *

page = HTML(
    Head(Title("My Page")),
    Body(
        Div(
            H1("Hello, World!"),
            Paragraph("This is a paragraph.")
        )
    )
)

# Compact output (default)
print(page.render())
# Output: <!DOCTYPE html><html lang="en" dir="ltr"><head><title>My Page</title></head>...

# Pretty output with indentation
print(page.render(pretty=True))
# Output:
# <!DOCTYPE html>
# <html lang="en" dir="ltr">
#   <head>
#     <title>My Page</title>
#   </head>
#   <body>
#     <div>
#       <h1>Hello, World!</h1>
#       <p>This is a paragraph.</p>
#     </div>
#   </body>
# </html>
```

Pretty printing is perfect for:
- Development and debugging
- Generating human-readable HTML files
- Documentation and tutorials
- Inspecting complex structures

### CSS Style Helpers

YDNATL provides convenient methods for working with inline CSS styles:

```python
from ydnatl import *

# Create element and add styles
div = Div("Styled content")

# Add single style
div.add_style("color", "blue")
div.add_style("font-size", "16px")

# Add multiple styles at once
div.add_styles({
    "background-color": "#f0f0f0",
    "padding": "20px",
    "margin": "10px",
    "border-radius": "5px"
})

# Get a specific style value
color = div.get_style("color")  # Returns "blue"

# Remove a style
div.remove_style("margin")

# Result: <div style="color: blue; font-size: 16px; background-color: #f0f0f0; padding: 20px; border-radius: 5px">Styled content</div>
```

### External Stylesheet and Theming

YDNATL includes a powerful styling system for managing external stylesheets, themes, and reusable component styles. This is perfect for building larger applications where you want to separate styles from markup.

#### Basic StyleSheet Usage

```python
from ydnatl import *
from ydnatl.styles import CSSStyle, StyleSheet

# Create a stylesheet
stylesheet = StyleSheet()

# Register reusable styles
btn_primary = stylesheet.register("btn-primary", CSSStyle(
    background_color="#007bff",
    color="white",
    padding="10px 20px",
    border_radius="5px",
    border="none",
    cursor="pointer",
    _hover=CSSStyle(background_color="#0056b3")  # Pseudo-selector
))

# Use in HTML
page = HTML(
    Head(
        Title("My Page"),
        Style(stylesheet.render())  # Insert generated CSS
    ),
    Body(
        Button("Click Me", class_name=btn_primary)
    )
)
```

#### Theming Support

YDNATL includes three preset themes (Modern, Classic, Minimal) with full CSS variable support:

```python
from ydnatl.styles import Theme, StyleSheet, CSSStyle

# Use a preset theme
theme = Theme.modern()  # or Theme.classic() or Theme.minimal()

# Create stylesheet with theme
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
    border_radius="8px",
    box_shadow="0 1px 3px rgba(0, 0, 0, 0.1)"
))
```

#### BEM Naming Convention

Built-in support for BEM (Block Element Modifier) naming:

```python
from ydnatl.styles import StyleSheet, CSSStyle

stylesheet = StyleSheet()

# Register with BEM naming
card = stylesheet.register_bem("card", style=CSSStyle(
    background="white",
    padding="20px"
))

card_header = stylesheet.register_bem("card", element="header", style=CSSStyle(
    font_weight="bold"
))

card_featured = stylesheet.register_bem("card", modifier="featured", style=CSSStyle(
    border="2px solid blue"
))

# Generates: .card, .card__header, .card--featured
```

#### Responsive Breakpoints

Add responsive styles with breakpoint support:

```python
from ydnatl.styles import CSSStyle, StyleSheet

stylesheet = StyleSheet()

container = stylesheet.register("container", CSSStyle(
    padding="10px",
    _sm=CSSStyle(padding="15px", max_width="640px"),
    _md=CSSStyle(padding="20px", max_width="768px"),
    _lg=CSSStyle(padding="30px", max_width="1024px")
))

# Generates media queries automatically
```

#### Combining with Inline Styles

You can mix stylesheet classes with inline style overrides:

```python
# Register base style
btn = stylesheet.register("btn", CSSStyle(
    padding="10px 20px",
    border_radius="5px"
))

# Use base class + inline overrides
Button("Custom", class_name=btn).add_styles({
    "background-color": "#ff0000",
    "font-size": "18px"
})
```

**Key Features:**
- Snake_case to kebab-case conversion (background_color → background-color)
- Pseudo-selector support (:hover, :active, :focus, etc.)
- Responsive breakpoints with media queries
- Theme system with CSS variables
- BEM naming convention support
- JSON serialization for saving/loading styles
- Combines seamlessly with existing inline styles

See the [examples/stylesheet_example.py](examples/stylesheet_example.py) file for complete working examples.

### Method Chaining

All builder methods return `self`, enabling fluent method chaining:

```python
from ydnatl import *

# Chain multiple operations together
container = (Div()
    .add_attribute("id", "main-container")
    .add_attribute("class", "wrapper")
    .add_style("background", "#fff")
    .add_styles({"padding": "20px", "margin": "0 auto"})
    .append(H1("Welcome"))
    .append(Paragraph("This is the main content."))
    .append(Paragraph("Another paragraph here.")))

print(container.render())
```

Chainable methods:
- `append()` - Add children
- `prepend()` - Add children at the beginning
- `add_attribute()` - Add single attribute
- `add_attributes()` - Add multiple attributes
- `remove_attribute()` - Remove an attribute
- `add_style()` - Add single CSS style
- `add_styles()` - Add multiple CSS styles
- `remove_style()` - Remove a CSS style
- `clear()` - Remove all children
- `remove_all()` - Remove children matching a condition

### Context Manager Support

Use elements as context managers for cleaner, more intuitive nesting:

```python
from ydnatl import *

# Using context managers
with Div(id="container", class_name="main") as container:
    with Section(class_name="content") as section:
        section.append(H1("Title"))
        section.append(Paragraph("Content goes here"))

    container.append(section)
    container.append(Footer(Paragraph("Footer text")))

print(container.render())
```

### Fragment Support

Use `Fragment` to group elements without adding a wrapper tag:

```python
from ydnatl import *

# Without Fragment - adds extra div wrapper
content = Div(
    H1("Title"),
    Paragraph("Content")
)
# Output: <div><h1>Title</h1><p>Content</p></div>

# With Fragment - no wrapper tag
content = Fragment(
    H1("Title"),
    Paragraph("Content")
)
# Output: <h1>Title</h1><p>Content</p>

# Perfect for conditional rendering
def render_items(items, show_header=True):
    fragment = Fragment()

    if show_header:
        fragment.append(H2("Items List"))

    for item in items:
        fragment.append(Paragraph(item))

    return fragment

# Use in parent element
page = Div(
    render_items(["Item 1", "Item 2", "Item 3"], show_header=True)
)
# Output: <div><h2>Items List</h2><p>Item 1</p><p>Item 2</p><p>Item 3</p></div>
```

**Fragment use cases:**
- Conditional rendering without wrapper divs
- Returning multiple elements from functions
- List composition and iteration
- Cleaner component architecture

### HTML Parsing

YDNATL can parse raw HTML strings and convert them into YDNATL elements. This is useful for importing existing HTML, migrating from other tools, or working with HTML from external sources.

```python
from ydnatl import from_html, HTMLElement

# Parse a single HTML element
html_string = '<div class="container"><h1>Hello World</h1><p>Welcome to YDNATL</p></div>'
element = from_html(html_string)

# Now you can work with it like any YDNATL element
element.add_style("padding", "20px")
element.append(Paragraph("Added via YDNATL"))

print(element.render())
# Output: <div class="container" style="padding: 20px"><h1>Hello World</h1><p>Welcome to YDNATL</p><p>Added via YDNATL</p></div>

# Alternative: use the class method
element = HTMLElement.from_html(html_string)
```

**Parsing HTML fragments** (multiple root elements):

```python
from ydnatl import from_html

# HTML with multiple root elements
html_fragment = '''
<h1>Welcome</h1>
<p>First paragraph</p>
<p>Second paragraph</p>
'''

# Parse as fragment (returns list of elements)
elements = from_html(html_fragment, fragment=True)

# Work with each element
for el in elements:
    print(el.tag, el.text)
# Output:
# h1 Welcome
# p First paragraph
# p Second paragraph

# Combine with other YDNATL features
container = Div()
for el in elements:
    container.append(el)

print(container.render())
# Output: <div><h1>Welcome</h1><p>First paragraph</p><p>Second paragraph</p></div>
```

**Features:**
- Handles all HTML5 elements including self-closing tags (br, img, hr, etc.)
- Preserves attributes, including data-* attributes
- Converts `class` attribute to `class_name` automatically
- Supports nested structures of any depth
- Handles HTML entities and special characters
- No external dependencies (uses Python's built-in html.parser)

**Use cases:**
- Import existing HTML into your website builder
- Migrate from other HTML generation tools
- Parse HTML templates from external sources
- Convert HTML snippets to YDNATL for manipulation
- Testing and validation workflows
- Combining static HTML with dynamic YDNATL generation

### JSON Serialization

YDNATL supports JSON serialization and deserialization, making it perfect for drag-and-drop website builders, saving UI states, or transmitting page structures over APIs.

```python
from ydnatl import *

# Build a page structure
page = Div(id="page", class_name="container")
page.append(
    H1("Welcome"),
    Section(
        Paragraph("This is a paragraph"),
        Paragraph("Another paragraph", class_name="highlight")
    )
)

# Serialize to JSON (for saving/storing)
json_data = page.to_json(indent=2)
print(json_data)

# Later... deserialize from JSON (for loading)
from ydnatl.core.element import HTMLElement
restored_page = HTMLElement.from_json(json_data)

# Generate HTML (output will be identical)
print(str(restored_page))
```

The JSON format is simple and clean:

```json
{
  "tag": "div",
  "self_closing": false,
  "attributes": {
    "id": "page",
    "class": "container"
  },
  "text": "",
  "children": []
}
```

**Use cases:**
- Save/load website layouts to/from a database
- Implement undo/redo functionality
- Store pre-built templates as JSON
- Version control for page structures
- API communication between frontend and backend
- Drag-and-drop website builders

## Great For

- CLI tools
- Drag-and-drop website builders
- Site builders with save/load functionality
- Web frameworks
- Alternative to heavy template engines
- Static site generators
- Documentation generators
- LLM's and AI tooling that generate interfaces dynamically
- Creating frontends for headless platforms (CMS/CRM etc)
- Applications requiring UI state serialization

## LLM Guide

For AI assistants and code generation tools, we provide a comprehensive technical reference in [LLM_GUIDE.md](LLM_GUIDE.md) with:
- Complete API documentation with exact method signatures
- Type hints and return values for all methods
- 10 common patterns with code examples
- Error handling and security best practices
- Quick reference cheat sheet

## Examples

### FastAPI

```python
from fastapi import FastAPI
from ydnatl import *

app = FastAPI()

@app.get("/")
async def root():
    return HTML(
        Head(
            Title("My Page")
        ),
        Body(
            Section(
                H1("Hello, World!"),
                Paragraph("This is a test document.")
            )
        )
    )
```

### Django

```python
from django.http import HttpResponse
from ydnatl import *

def index(request):
    return HttpResponse(HTML(
        Head(
            Title("My Page"),
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            HtmlLink(rel="stylesheet", href="style.css"),
            Script(src="script.js")
        ),
        Body(
            Section(
                H1("Hello, World!"),
                Paragraph("This is a paragraph."),
                Paragraph("This is another paragraph.")
            )
        )
    ))
```

### Flask

```python
from flask import Flask
from ydnatl import *

app = Flask(__name__)

@app.route("/")
def index():
    return HTML(
        Head(
            Title("My Page")
        ),
        Body(
            Section(
                H1("Hello, World!"),
                Paragraph("This is a test document.")
            )
        )
    )
```

## Test Coverage

YDNATL has full test coverage. To run the tests locally, use:

```shell
pytest
```

## Element Methods:

**Element Manipulation:**
- `instance.prepend()` - Prepend children (returns self for chaining)
- `instance.append()` - Append children (returns self for chaining)
- `instance.filter()` - Filter children by condition
- `instance.remove_all()` - Remove children matching condition (returns self for chaining)
- `instance.clear()` - Remove all children (returns self for chaining)
- `instance.pop()` - Remove and return child at index
- `instance.first()` - Get first child
- `instance.last()` - Get last child
- `instance.replace_child()` - Replace child at index
- `instance.clone()` - Deep copy of element
- `instance.find_by_attribute()` - Find child by attribute value
- `instance.count_children()` - Count direct children

**Attribute Management:**
- `instance.add_attribute()` - Add single attribute (returns self for chaining)
- `instance.add_attributes()` - Add multiple attributes (returns self for chaining)
- `instance.remove_attribute()` - Remove attribute (returns self for chaining)
- `instance.get_attribute()` - Get attribute value
- `instance.has_attribute()` - Check if attribute exists
- `instance.get_attributes()` - Get all or specific attributes
- `instance.generate_id()` - Generate unique ID if not present

**CSS Style Management:**
- `instance.add_style()` - Add single CSS style (returns self for chaining)
- `instance.add_styles()` - Add multiple CSS styles (returns self for chaining)
- `instance.get_style()` - Get specific style value
- `instance.remove_style()` - Remove CSS style (returns self for chaining)

**Rendering:**
- `instance.render(pretty=False)` - Render to HTML string (pretty=True for indented output)
- `instance.to_dict()` - Convert to dictionary
- `instance.to_json(indent=None)` - Serialize to JSON string
- `HTMLElement.from_dict(data)` - Reconstruct from dictionary (class method)
- `HTMLElement.from_json(json_str)` - Reconstruct from JSON string (class method)
- `HTMLElement.from_html(html_str, fragment=False)` - Parse HTML string to YDNATL element(s) (class method)
- `from_html(html_str, fragment=False)` - Parse HTML string to YDNATL element(s) (function)

## Events

- `instance.on_load()`
- `instance.on_before_render()`
- `instance.on_after_render()`
- `instance.on_unload()`

## Element Properties

- `instance.tag`
- `instance.children`
- `instance.text`
- `instance.attributes`
- `instance.self_closing`

## Modules

| **Module**         | **Purpose**                       | **Key Elements**                                |
|--------------------|-----------------------------------|-------------------------------------------------|
| ydnatl.tags.form   | Common HTML form elements         | Form, Input, Button, Select, Textarea           |
| ydnatl.tags.html   | Structural HTML document elements | HTML, Head, Body, Title, Meta, Script           |
| ydnatl.tags.layout | Layout related HTML tags          | Div, Section, Header, Nav, Footer, Main         |
| ydnatl.tags.lists  | HTML list elements                | UnorderedList, OrderedList, ListItem            |
| ydnatl.tags.media  | Media related HTML elements       | Image, Video, Audio, Figure, Canvas             |
| ydnatl.tags.table  | HTML table elements               | Table, TableRow, TableHeaderCell, TableDataCell |
| ydnatl.tags.text   | HTML text elements                | H1-H6, Paragraph, Span, Strong, Em              |

## Importing

Instead of importing the entire module, you can selectively use only the elements you need like this:

```python
# Instead of importing everything
from ydnatl import *

# Import selectively for better performance and clarity
from ydnatl.tags.form import Form, Button, Input
from ydnatl.tags.html import HTML, Head, Body, Title
from ydnatl.tags.layout import Div, Section
from ydnatl.tags.text import H1, Paragraph
```

#### ydnatl.tags.form

- `Form()`
- `Input()`
- `Label()`
- `Textarea()`
- `Select()`
- `Option()`
- `Button()`
- `Fieldset()`
- `Legend()`
- `Optgroup()`
- `Output()`
- `Progress()`
- `Meter()`

#### ydnatl.tags.html

- `HTML()`
- `Head()`
- `Body()`
- `Title()`
- `Meta()`
- `Base()`
- `HtmlLink()` (use instead of `Link()` to avoid conflicts)
- `Script()`
- `Style()`
- `Noscript()`
- `IFrame()`

#### ydnatl.tags.layout

- `Div()`
- `Section()`
- `Article()`
- `Aside()`
- `Header()`
- `Nav()`
- `Footer()`
- `HorizontalRule()`
- `Main()`
- `Details()`
- `Summary()`
- `Dialog()`

#### ydnatl.tags.lists

- `UnorderedList()`
- `OrderedList()`
- `ListItem()`
- `Datalist()`
- `DescriptionDetails()`
- `DescriptionList()`
- `DescriptionTerm()`

#### ydnatl.tags.media

- `Image()`
- `Video()`
- `Audio()`
- `Source()`
- `Track()`
- `Picture()`
- `Figure()`
- `Figcaption()`
- `Canvas()`
- `Embed()`
- `Object()`
- `Param()`
- `Map()`
- `Area()`

#### ydnatl.tags.table

- `Table()`
- `TableFooter()`
- `TableHeaderCell()`
- `TableHeader()`
- `TableBody()`
- `TableDataCell()`
- `TableRow()`
- `Caption()`
- `Col()`
- `Colgroup()`

#### ydnatl.tags.text

- `H1()`
- `H2()`
- `H3()`
- `H4()`
- `H5()`
- `H6()`
- `Paragraph()`
- `Blockquote()`
- `Pre()`
- `Quote()`
- `Cite()`
- `Em()`
- `Italic()`
- `Span()`
- `Strong()`
- `Bold()`
- `Abbr()`
- `Link()`
- `Small()`
- `Superscript()`
- `Subscript()`
- `Time()`
- `Code()`
- `Del()`
- `Ins()`
- `Strikethrough()`
- `Underline()`
- `Kbd()`
- `Samp()`
- `Var()`
- `Mark()`
- `Dfn()`
- `Br()`
- `Wbr()`

## Creating your own elements or components

```python

from ydnatl import *

class MyTag(HTMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **{**kwargs, "tag": "mytag"})

        self.add_attributes([
            ("id", "mycustomid"),
            ("aria-controls", "menu"),
        ])

    def on_load(self) -> None:
        print("The on_load event has been called")

    def on_before_render(self) -> None:
        print("The on_before_render event has been called")

    def on_after_render(self) -> None:
        print("The on_after_render event has been called")


mytag = MyTag(
    Div(
        Paragraph("Hello World!")
    )
)

print(mytag.render())
```

This will produce:

```html
<mytag id="mycustomid" aria-controls="menu">
  <div>
    <p>Hello World!</p>
  </div>
</mytag>
```

You can use the event callbacks or properties/methods directly to load further child elements, fetch data or any other programmatic task to enrich or construct your tag on loading, render or even after render.

You can take this further and construct an entire page as a component where everything needed for the page is contained within the element class itself. This is a great way to build websites.

## Contributions

Contributions, suggestions and improvements are all welcome. 

#### Developing YDNATL

1. Create a virtual environment

```bash
python3 -m venv .venv 
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
```

2. Install the dev dependencies:

```bash
pip install ".[dev]"
```

3. Run the tests:

```bash
pytest
```

When you are happy with your changes, create a merge request.

## License

Please see [LICENSE](LICENSE) for licensing details.

## Author

[github.com/sn](https://github.com/sn)
