import unittest

from ydnatl.core.element import HTMLElement
from ydnatl.core.fragment import Fragment
from ydnatl.tags.layout import Div, Section
from ydnatl.tags.text import H1, Paragraph, Span


class TestFragment(unittest.TestCase):

    def test_fragment_basic(self):
        """Test basic Fragment rendering without wrapper tag."""
        fragment = Fragment(H1("Title"), Paragraph("Content"))

        rendered = str(fragment)
        self.assertEqual(rendered, "<h1>Title</h1><p>Content</p>")
        self.assertNotIn("<fragment>", rendered)
        self.assertNotIn("</fragment>", rendered)

    def test_fragment_empty(self):
        """Test empty Fragment renders nothing."""
        fragment = Fragment()
        rendered = str(fragment)
        self.assertEqual(rendered, "")

    def test_fragment_single_child(self):
        """Test Fragment with single child."""
        fragment = Fragment(Paragraph("Single child"))

        rendered = str(fragment)
        self.assertEqual(rendered, "<p>Single child</p>")

    def test_fragment_multiple_children(self):
        """Test Fragment with multiple children."""
        fragment = Fragment(
            H1("Header"),
            Paragraph("Paragraph 1"),
            Paragraph("Paragraph 2"),
            Span("Inline text"),
        )

        rendered = str(fragment)
        expected = "<h1>Header</h1><p>Paragraph 1</p><p>Paragraph 2</p><span>Inline text</span>"
        self.assertEqual(rendered, expected)

    def test_fragment_nested_elements(self):
        """Test Fragment with nested HTML elements."""
        fragment = Fragment(
            Div(H1("Title"), Paragraph("Content")), Section(Paragraph("More content"))
        )

        rendered = str(fragment)
        self.assertIn("<div>", rendered)
        self.assertIn("<h1>Title</h1>", rendered)
        self.assertIn("<section>", rendered)
        self.assertNotIn("<fragment>", rendered)

    def test_fragment_with_text(self):
        """Test Fragment with text content."""
        fragment = Fragment("Plain text")

        rendered = str(fragment)
        self.assertEqual(rendered, "Plain text")

    def test_fragment_mixed_text_and_elements(self):
        """Test Fragment with both text and elements."""
        fragment = Fragment("Text before", Paragraph("Middle"), "Text after")

        # Note: text is handled differently, need to test actual output
        rendered = str(fragment)
        self.assertIn("<p>Middle</p>", rendered)

    def test_fragment_pretty_printing(self):
        """Test Fragment with pretty printing enabled."""
        fragment = Fragment(
            Div(H1("Title"), Paragraph("Content")), Paragraph("Outside")
        )

        pretty = fragment.render(pretty=True)
        self.assertIn("\n", pretty)
        self.assertIn("  ", pretty)  # Should have indentation from children
        self.assertNotIn("<fragment>", pretty)

    def test_fragment_append_children(self):
        """Test appending children to Fragment after creation."""
        fragment = Fragment()
        fragment.append(H1("Added Title"))
        fragment.append(Paragraph("Added content"))

        rendered = str(fragment)
        self.assertEqual(rendered, "<h1>Added Title</h1><p>Added content</p>")

    def test_fragment_prepend_children(self):
        """Test prepending children to Fragment."""
        fragment = Fragment(Paragraph("Second"))
        fragment.prepend(H1("First"))

        rendered = str(fragment)
        self.assertEqual(rendered, "<h1>First</h1><p>Second</p>")

    def test_fragment_clear(self):
        """Test clearing Fragment children."""
        fragment = Fragment(H1("Title"), Paragraph("Content"))

        fragment.clear()
        rendered = str(fragment)
        self.assertEqual(rendered, "")

    def test_fragment_count_children(self):
        """Test counting Fragment children."""
        fragment = Fragment(H1("Title"), Paragraph("Content 1"), Paragraph("Content 2"))

        self.assertEqual(fragment.count_children(), 3)

    def test_fragment_nested_in_div(self):
        """Test using Fragment inside another element."""
        fragment = Fragment(H1("Title"), Paragraph("Content"))

        div = Div()
        div.append(fragment)

        rendered = str(div)
        # Fragment should render its children without wrapper
        self.assertEqual(rendered, "<div><h1>Title</h1><p>Content</p></div>")

    def test_fragment_conditional_rendering(self):
        """Test Fragment for conditional rendering use case."""
        show_header = True
        show_footer = False

        fragment = Fragment()

        if show_header:
            fragment.append(H1("Header"))

        fragment.append(Paragraph("Main content"))

        if show_footer:
            fragment.append(Paragraph("Footer"))

        rendered = str(fragment)
        self.assertIn("<h1>Header</h1>", rendered)
        self.assertIn("<p>Main content</p>", rendered)
        self.assertNotIn("Footer", rendered)

    def test_fragment_list_composition(self):
        """Test using Fragment to compose lists of elements."""
        items = ["Item 1", "Item 2", "Item 3"]

        fragment = Fragment()
        for item in items:
            fragment.append(Paragraph(item))

        rendered = str(fragment)
        self.assertEqual(rendered, "<p>Item 1</p><p>Item 2</p><p>Item 3</p>")

    def test_fragment_with_attributes(self):
        """Test that Fragment ignores attributes (doesn't render them)."""
        fragment = Fragment(H1("Title"), id="ignored", class_name="also-ignored")

        rendered = str(fragment)
        self.assertNotIn("id", rendered)
        self.assertNotIn("class", rendered)
        self.assertEqual(rendered, "<h1>Title</h1>")

    def test_fragment_method_chaining(self):
        """Test method chaining with Fragment."""
        fragment = (
            Fragment()
            .append(H1("Title"))
            .append(Paragraph("Content 1"))
            .append(Paragraph("Content 2"))
        )

        self.assertEqual(fragment.count_children(), 3)
        rendered = str(fragment)
        self.assertIn("<h1>Title</h1>", rendered)
        self.assertIn("<p>Content 1</p>", rendered)

    def test_fragment_inheritance(self):
        """Test that Fragment inherits from HTMLElement."""
        fragment = Fragment()
        self.assertIsInstance(fragment, HTMLElement)

    def test_fragment_context_manager(self):
        """Test using Fragment as a context manager."""
        with Fragment() as fragment:
            fragment.append(H1("Title"))
            fragment.append(Paragraph("Content"))

        rendered = str(fragment)
        self.assertEqual(rendered, "<h1>Title</h1><p>Content</p>")

    def test_fragment_clone(self):
        """Test cloning a Fragment."""
        original = Fragment(H1("Title"), Paragraph("Content"))

        cloned = original.clone()

        self.assertEqual(str(original), str(cloned))
        self.assertIsNot(original, cloned)
        self.assertIsNot(original.children[0], cloned.children[0])

    def test_fragment_filter(self):
        """Test filtering Fragment children."""
        fragment = Fragment(
            H1("Title"), Paragraph("Para 1"), Span("Span"), Paragraph("Para 2")
        )

        paragraphs = list(fragment.filter(lambda x: x.tag == "p"))
        self.assertEqual(len(paragraphs), 2)

    def test_fragment_find_by_attribute(self):
        """Test finding elements by attribute in Fragment."""
        fragment = Fragment(
            H1("Title", id="header"), Paragraph("Content", id="main"), Span("Text")
        )

        found = fragment.find_by_attribute("id", "main")
        self.assertIsNotNone(found)
        self.assertEqual(found.tag, "p")

    def test_fragment_compact_vs_pretty(self):
        """Test compact vs pretty rendering of Fragment."""
        fragment = Fragment(Div(H1("Title"), Paragraph("Content")))

        # Compact
        compact = fragment.render(pretty=False)
        self.assertNotIn("\n", compact)
        self.assertEqual(compact, "<div><h1>Title</h1><p>Content</p></div>")

        # Pretty
        pretty = fragment.render(pretty=True)
        self.assertIn("\n", pretty)


if __name__ == "__main__":
    unittest.main()
