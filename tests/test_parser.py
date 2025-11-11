import unittest

from ydnatl.core.element import HTMLElement
from ydnatl.core.parser import from_html


class TestHTMLParser(unittest.TestCase):

    def test_parse_simple_element(self):
        """Test parsing a simple single element."""
        html = "<div>Hello World</div>"
        element = from_html(html)

        self.assertIsNotNone(element)
        self.assertEqual(element.tag, "div")
        self.assertEqual(element.text, "Hello World")
        self.assertEqual(len(element.children), 0)

    def test_parse_element_with_attributes(self):
        """Test parsing element with attributes."""
        html = '<div id="main" class="container" data-value="123">Content</div>'
        element = from_html(html)

        self.assertEqual(element.tag, "div")
        self.assertEqual(element.get_attribute("id"), "main")
        self.assertEqual(element.get_attribute("class_name"), "container")
        self.assertEqual(
            element.get_attribute("data-value"), "123"
        )  # Stored with hyphen
        self.assertEqual(element.text, "Content")

    def test_parse_nested_elements(self):
        """Test parsing nested HTML elements."""
        html = """
        <div class="outer">
            <h1>Title</h1>
            <p>Paragraph content</p>
        </div>
        """
        element = from_html(html)

        self.assertEqual(element.tag, "div")
        self.assertEqual(element.get_attribute("class_name"), "outer")
        self.assertEqual(len(element.children), 2)

        # Check first child (h1)
        h1 = element.children[0]
        self.assertEqual(h1.tag, "h1")
        self.assertEqual(h1.text, "Title")

        # Check second child (p)
        p = element.children[1]
        self.assertEqual(p.tag, "p")
        self.assertEqual(p.text, "Paragraph content")

    def test_parse_deeply_nested_elements(self):
        """Test parsing deeply nested structure."""
        html = """
        <div>
            <section>
                <article>
                    <h1>Deep Title</h1>
                    <p>Deep content</p>
                </article>
            </section>
        </div>
        """
        element = from_html(html)

        self.assertEqual(element.tag, "div")
        section = element.children[0]
        self.assertEqual(section.tag, "section")
        article = section.children[0]
        self.assertEqual(article.tag, "article")
        self.assertEqual(len(article.children), 2)

    def test_parse_self_closing_tags(self):
        """Test parsing self-closing/void elements."""
        html = '<div><br /><img src="test.jpg" alt="Test" /><hr /></div>'
        element = from_html(html)

        self.assertEqual(element.tag, "div")
        self.assertEqual(len(element.children), 3)

        # Check br
        br = element.children[0]
        self.assertEqual(br.tag, "br")
        self.assertTrue(br.self_closing)

        # Check img
        img = element.children[1]
        self.assertEqual(img.tag, "img")
        self.assertTrue(img.self_closing)
        self.assertEqual(img.get_attribute("src"), "test.jpg")
        self.assertEqual(img.get_attribute("alt"), "Test")

        # Check hr
        hr = element.children[2]
        self.assertEqual(hr.tag, "hr")
        self.assertTrue(hr.self_closing)

    def test_parse_mixed_content(self):
        """Test parsing elements with mixed text and child elements."""
        html = "<div>Before<span>Middle</span>After</div>"
        element = from_html(html)

        self.assertEqual(element.tag, "div")
        # Text before span
        self.assertIn("Before", element.text)
        # Check span child
        self.assertEqual(len(element.children), 1)
        span = element.children[0]
        self.assertEqual(span.tag, "span")
        self.assertEqual(span.text, "Middle")

    def test_parse_fragment_multiple_roots(self):
        """Test parsing HTML fragment with multiple root elements."""
        html = "<h1>Title</h1><p>Paragraph 1</p><p>Paragraph 2</p>"
        elements = from_html(html, fragment=True)

        self.assertEqual(len(elements), 3)

        # Check elements
        self.assertEqual(elements[0].tag, "h1")
        self.assertEqual(elements[0].text, "Title")

        self.assertEqual(elements[1].tag, "p")
        self.assertEqual(elements[1].text, "Paragraph 1")

        self.assertEqual(elements[2].tag, "p")
        self.assertEqual(elements[2].text, "Paragraph 2")

    def test_parse_empty_element(self):
        """Test parsing empty element."""
        html = "<div></div>"
        element = from_html(html)

        self.assertEqual(element.tag, "div")
        self.assertEqual(element.text, "")
        self.assertEqual(len(element.children), 0)

    def test_parse_complex_structure(self):
        """Test parsing complex HTML structure."""
        html = """
        <html>
            <head>
                <title>Test Page</title>
                <meta charset="utf-8" />
            </head>
            <body>
                <header>
                    <h1>Main Title</h1>
                    <nav>
                        <a href="/">Home</a>
                        <a href="/about">About</a>
                    </nav>
                </header>
                <main>
                    <article>
                        <h2>Article Title</h2>
                        <p>Article content.</p>
                    </article>
                </main>
                <footer>
                    <p>Copyright 2024</p>
                </footer>
            </body>
        </html>
        """
        element = from_html(html)

        self.assertEqual(element.tag, "html")
        self.assertEqual(len(element.children), 2)

        # Check head
        head = element.children[0]
        self.assertEqual(head.tag, "head")

        # Check body
        body = element.children[1]
        self.assertEqual(body.tag, "body")
        self.assertEqual(len(body.children), 3)

    def test_parse_special_characters(self):
        """Test parsing HTML with special characters."""
        html = "<div>Hello &amp; Goodbye</div>"
        element = from_html(html)

        self.assertEqual(element.tag, "div")
        # HTML entities should be decoded by the parser
        self.assertIn("&", element.text)

    def test_parse_attributes_without_values(self):
        """Test parsing boolean attributes."""
        html = '<input type="checkbox" checked disabled />'
        element = from_html(html)

        self.assertEqual(element.tag, "input")
        self.assertEqual(element.get_attribute("type"), "checkbox")
        self.assertTrue(element.has_attribute("checked"))
        self.assertTrue(element.has_attribute("disabled"))

    def test_parse_style_attribute(self):
        """Test parsing inline style attribute."""
        html = '<div style="color: red; font-size: 16px;">Styled</div>'
        element = from_html(html)

        self.assertEqual(element.tag, "div")
        self.assertEqual(element.get_attribute("style"), "color: red; font-size: 16px;")

    def test_parse_data_attributes(self):
        """Test parsing data-* attributes."""
        html = '<div data-id="123" data-name="test" data-active="true">Content</div>'
        element = from_html(html)

        # Attributes are stored with hyphens (kebab-case)
        self.assertEqual(element.get_attribute("data-id"), "123")
        self.assertEqual(element.get_attribute("data-name"), "test")
        self.assertEqual(element.get_attribute("data-active"), "true")

    def test_parse_and_render_roundtrip(self):
        """Test that parsing and rendering produces similar output."""
        html = '<div class="container"><h1>Title</h1><p>Content</p></div>'
        element = from_html(html)

        rendered = element.render()

        # Parse the rendered output
        element2 = from_html(rendered)

        # Should have same structure
        self.assertEqual(element.tag, element2.tag)
        self.assertEqual(
            element.get_attribute("class_name"), element2.get_attribute("class_name")
        )
        self.assertEqual(len(element.children), len(element2.children))

    def test_htmlelement_from_html_classmethod(self):
        """Test using HTMLElement.from_html() class method."""
        html = '<div id="test">Content</div>'
        element = HTMLElement.from_html(html)

        self.assertIsNotNone(element)
        self.assertEqual(element.tag, "div")
        self.assertEqual(element.get_attribute("id"), "test")
        self.assertEqual(element.text, "Content")

    def test_htmlelement_from_html_fragment(self):
        """Test using HTMLElement.from_html() with fragment=True."""
        html = "<h1>One</h1><h2>Two</h2>"
        elements = HTMLElement.from_html(html, fragment=True)

        self.assertEqual(len(elements), 2)
        self.assertEqual(elements[0].tag, "h1")
        self.assertEqual(elements[1].tag, "h2")

    def test_parse_form_elements(self):
        """Test parsing form elements."""
        html = """
        <form action="/submit" method="post">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required />
            <button type="submit">Submit</button>
        </form>
        """
        element = from_html(html)

        self.assertEqual(element.tag, "form")
        self.assertEqual(element.get_attribute("action"), "/submit")
        self.assertEqual(element.get_attribute("method"), "post")
        self.assertEqual(len(element.children), 3)

    def test_parse_table_structure(self):
        """Test parsing table elements."""
        html = """
        <table>
            <thead>
                <tr>
                    <th>Header 1</th>
                    <th>Header 2</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Cell 1</td>
                    <td>Cell 2</td>
                </tr>
            </tbody>
        </table>
        """
        element = from_html(html)

        self.assertEqual(element.tag, "table")
        self.assertEqual(len(element.children), 2)

        thead = element.children[0]
        self.assertEqual(thead.tag, "thead")

        tbody = element.children[1]
        self.assertEqual(tbody.tag, "tbody")

    def test_parse_list_elements(self):
        """Test parsing list elements."""
        html = """
        <ul class="list">
            <li>Item 1</li>
            <li>Item 2</li>
            <li>Item 3</li>
        </ul>
        """
        element = from_html(html)

        self.assertEqual(element.tag, "ul")
        self.assertEqual(element.get_attribute("class_name"), "list")
        self.assertEqual(len(element.children), 3)

        for i, child in enumerate(element.children, 1):
            self.assertEqual(child.tag, "li")
            self.assertEqual(child.text, f"Item {i}")

    def test_parse_whitespace_handling(self):
        """Test that whitespace-only text nodes are ignored."""
        html = """
        <div>
            <p>Paragraph 1</p>
            <p>Paragraph 2</p>
        </div>
        """
        element = from_html(html)

        # Should not have whitespace text nodes
        self.assertEqual(len(element.children), 2)
        self.assertEqual(element.children[0].tag, "p")
        self.assertEqual(element.children[1].tag, "p")

    def test_parse_script_and_style_tags(self):
        """Test parsing script and style tags."""
        html = """
        <head>
            <style>body { margin: 0; }</style>
            <script>console.log("test");</script>
        </head>
        """
        element = from_html(html)

        self.assertEqual(element.tag, "head")
        self.assertEqual(len(element.children), 2)

        style = element.children[0]
        self.assertEqual(style.tag, "style")

        script = element.children[1]
        self.assertEqual(script.tag, "script")


if __name__ == "__main__":
    unittest.main()
