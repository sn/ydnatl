import unittest

from ydnatl.core.element import HTMLElement
from ydnatl.tags.html import (
    HTML,
    Head,
    Body,
    Title,
    Meta,
    Base,
    Link,
    Script,
    Style,
    Noscript,
    IFrame,
)


class TestHTMLTags(unittest.TestCase):

    def test_head(self):
        """Test the creation of an empty head element."""
        head = Head()
        self.assertEqual(head.tag, "head")
        self.assertEqual(str(head), "<head></head>")

    def test_body(self):
        """Test the creation of an empty body element."""
        body = Body()
        self.assertEqual(body.tag, "body")
        self.assertEqual(str(body), "<body></body>")

    def test_title(self):
        """Test the creation of a title element with text content."""
        title = Title("My Page")
        self.assertEqual(title.tag, "title")
        self.assertEqual(str(title), "<title>My Page</title>")

    def test_meta(self):
        """Test the creation of an empty meta element."""
        meta = Meta()
        self.assertEqual(meta.tag, "meta")
        self.assertEqual(str(meta), "<meta />")

    def test_link(self):
        """Test the creation of an empty link element."""
        link = Link()
        self.assertEqual(link.tag, "link")
        self.assertEqual(str(link), "<link />")

    def test_script(self):
        """Test the creation of an empty script element."""
        script = Script()
        self.assertEqual(script.tag, "script")
        self.assertEqual(str(script), "<script></script>")

    def test_style(self):
        """Test the creation of an empty style element."""
        style = Style()
        self.assertEqual(style.tag, "style")
        self.assertEqual(str(style), "<style></style>")

    def test_iframe(self):
        """Test the creation of an empty iframe element."""
        iframe = IFrame()
        self.assertEqual(iframe.tag, "iframe")
        self.assertEqual(str(iframe), "<iframe></iframe>")

    def test_html(self):
        """Test the creation of an empty HTML document."""
        html = HTML()
        self.assertEqual(html.tag, "html")
        expected = '<!DOCTYPE html><html lang="en" dir="ltr"></html>'
        self.assertEqual(str(html), expected)

    def test_base(self):
        """Test the creation of a base element."""
        base = Base(href="https://www.example.com/", target="_blank")
        self.assertEqual(base.tag, "base")
        self.assertTrue(base.self_closing)
        self.assertIn('href="https://www.example.com/"', str(base))
        self.assertIn('target="_blank"', str(base))

    def test_noscript(self):
        """Test the creation of a noscript element."""
        noscript = Noscript("JavaScript is required to view this page.")
        self.assertEqual(noscript.tag, "noscript")
        self.assertEqual(
            str(noscript),
            "<noscript>JavaScript is required to view this page.</noscript>",
        )

    def test_head_with_base(self):
        """Test head element with base tag."""
        head = Head(Base(href="https://www.example.com/"), Title("My Page"))
        self.assertIn("<base", str(head))
        self.assertIn("https://www.example.com/", str(head))

    def test_inheritance(self):
        """Test that all HTML-related classes inherit from HTMLElement."""
        for cls in [
            HTML,
            Head,
            Body,
            Title,
            Meta,
            Base,
            Link,
            Script,
            Style,
            Noscript,
            IFrame,
        ]:
            self.assertTrue(issubclass(cls, HTMLElement))


if __name__ == "__main__":
    unittest.main()
