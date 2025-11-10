import unittest

from ydnatl.core.element import HTMLElement
from ydnatl.tags.layout import (
    Div,
    Section,
    Article,
    Aside,
    Header,
    Nav,
    Footer,
    HorizontalRule,
    Main,
    Details,
    Summary,
    Dialog,
)
from ydnatl.tags.text import Paragraph


class TestLayoutTags(unittest.TestCase):

    def test_div(self):
        """Test the creation of a div element with text content."""
        div = Div("Hello, World!")
        self.assertEqual(div.tag, "div")
        self.assertEqual(str(div), "<div>Hello, World!</div>")

    def test_section(self):
        """Test the creation of a section element with text content."""
        section = Section("This is a section")
        self.assertEqual(section.tag, "section")
        self.assertEqual(str(section), "<section>This is a section</section>")

    def test_header(self):
        """Test the creation of a header element with text content."""
        header = Header("This is a header")
        self.assertEqual(header.tag, "header")
        self.assertEqual(str(header), "<header>This is a header</header>")

    def test_nav(self):
        """Test the creation of a nav element with text content."""
        nav = Nav("Navigation menu")
        self.assertEqual(nav.tag, "nav")
        self.assertEqual(str(nav), "<nav>Navigation menu</nav>")

    def test_footer(self):
        """Test the creation of a footer element with text content."""
        footer = Footer("This is a footer")
        self.assertEqual(footer.tag, "footer")
        self.assertEqual(str(footer), "<footer>This is a footer</footer>")

    def test_horizontal_rule(self):
        """Test the creation of a horizontal rule element."""
        hr = HorizontalRule()
        self.assertEqual(hr.tag, "hr")
        self.assertTrue(hr.self_closing)
        self.assertEqual(str(hr), "<hr />")

    def test_main(self):
        """Test the creation of a main element with text content."""
        main = Main("Main content")
        self.assertEqual(main.tag, "main")
        self.assertEqual(str(main), "<main>Main content</main>")

    def test_nested_elements(self):
        """Test the creation of nested layout elements."""
        layout = Div(
            Header("Header content"),
            Nav("Navigation"),
            Main(Section("Section 1"), Section("Section 2")),
            Footer("Footer content"),
        )
        expected = (
            "<div>"
            "<header>Header content</header>"
            "<nav>Navigation</nav>"
            "<main>"
            "<section>Section 1</section>"
            "<section>Section 2</section>"
            "</main>"
            "<footer>Footer content</footer>"
            "</div>"
        )
        self.assertEqual(str(layout), expected)

    def test_attributes(self):
        """Test the addition of attributes to a div element."""
        div = Div("Content", id="main", class_name="container")
        self.assertEqual(str(div), '<div id="main" class="container">Content</div>')

    def test_article(self):
        """Test the creation of an article element with text content."""
        article = Article("This is an article")
        self.assertEqual(article.tag, "article")
        self.assertEqual(str(article), "<article>This is an article</article>")

    def test_aside(self):
        """Test the creation of an aside element with text content."""
        aside = Aside("Sidebar content")
        self.assertEqual(aside.tag, "aside")
        self.assertEqual(str(aside), "<aside>Sidebar content</aside>")

    def test_details(self):
        """Test the creation of a details element."""
        details = Details("Hidden content")
        self.assertEqual(details.tag, "details")
        self.assertEqual(str(details), "<details>Hidden content</details>")

    def test_summary(self):
        """Test the creation of a summary element."""
        summary = Summary("Click to expand")
        self.assertEqual(summary.tag, "summary")
        self.assertEqual(str(summary), "<summary>Click to expand</summary>")

    def test_details_with_summary(self):
        """Test details element with nested summary."""
        details = Details(
            Summary("More information"), Paragraph("This is the hidden content")
        )
        expected = "<details><summary>More information</summary><p>This is the hidden content</p></details>"
        self.assertEqual(str(details), expected)

    def test_dialog(self):
        """Test the creation of a dialog element."""
        dialog = Dialog("Dialog content")
        self.assertEqual(dialog.tag, "dialog")
        self.assertEqual(str(dialog), "<dialog>Dialog content</dialog>")

    def test_dialog_with_open_attribute(self):
        """Test dialog element with open attribute."""
        dialog = Dialog("Dialog is open", open="open")
        self.assertIn('open="open"', str(dialog))

    def test_inheritance(self):
        """Test that all layout-related classes inherit from HTMLElement."""
        for cls in [
            Div,
            Section,
            Article,
            Aside,
            Header,
            Nav,
            Footer,
            HorizontalRule,
            Main,
            Details,
            Summary,
            Dialog,
        ]:
            self.assertTrue(issubclass(cls, HTMLElement))


if __name__ == "__main__":
    unittest.main()
